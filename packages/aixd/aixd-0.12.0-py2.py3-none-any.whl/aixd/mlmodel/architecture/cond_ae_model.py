from __future__ import annotations

import copy
import logging
import os
import warnings
from datetime import datetime
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import pytorch_lightning as pl
import torch
from pytorch_lightning import Callback
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.loggers import Logger
from pytorch_lightning.utilities.model_summary import ModelSummary
from torch import nn
from torch.utils.data import DataLoader

import aixd.data.constants as constants
import aixd.mlmodel.utils_mlmodel as ut
from aixd.data import DataObject, InputML, OutputML
from aixd.data.utils_data import convert_to
from aixd.mlmodel.architecture import losses
from aixd.mlmodel.architecture.decoders import Decoder
from aixd.mlmodel.architecture.encoders import Encoder
from aixd.mlmodel.architecture.heads import CategoricalOutHead, InHead, OutHead
from aixd.mlmodel.constants import SEP_LOSSES
from aixd.mlmodel.data.data_loader import DataModule, XYZDataset
from aixd.mlmodel.utils_mlmodel import rec_concat_dict, to_torch
from aixd.utils import logs
from aixd.utils.logs import temporary_logger_level
from aixd.utils.utils import basename, dirname

FORMATS_IO = constants.formats_io

warnings.filterwarnings("ignore", ".*does not have many workers.*")
logger = logs.get_logger().get_child("cae-model")


class CondAEModel(pl.LightningModule):
    """
    Class representing a Conditional Autoencoder model.

    Parameters
    ----------
    input_ml_dblock : InputML
        A input ml data block defining the input heads of the model.
    output_ml_dblock : OutputML
        A output ml data block defining the output heads of the model.
    layer_widths : List[int]
        List of integers specifying the number of units in each hidden layer of the autoencoder's encoder and decoder (i.e., the "core" of the autoencoder).
        The first element of the list corresponds to the number of units in the first hidden layer of the encoder, the last element corresponds to the
        number of units in the last hidden layer of the decoder, and the elements in between correspond to the number of units in each hidden layer of
        the autoencoder in the order they appear (encoder followed by decoder).
    latent_dim : int
        Integer specifying the number of units in the latent (i.e., encoded) representation of the data.
    heads_layer_widths : Dict[str, List[int]], optional, default={}
        Dictionary specifying the number of units in the "head" layers that are added to the autoencoder. The keys of the dictionary are the names of the features,
        the values are a sequence of integers specifying the number of units in each hidden layer of the head. Default is an empty dictionary: {}.
    custom_losses : Dict[str, Callable[[torch.Tensor, torch.Tensor], torch.Tensor]], optional, default=None
        Dictionary containing custom losses to be computed on the outputs.
    loss_weights : Dict[str, float], optional, default=None
        Dictionary containing the weights with which each loss term should be multiplied before being added to the total loss used for backpropagation, including custom losses.
    activation : Union[torch.nn.Module, str], optional, default="leaky_relu"
        Activation function to be used in the latent layers of the autoencoder.
    optimizer : torch.optim.Optimizer, optional, default=None
        Optimizer to be used for updating the model's weights.
    name : str, optional, default="CondAEModel"
        Name of the model.
    save_dir : str, optional, default=None
        Directory where the model related files will be saved, such as the models's checkpoint and logs.
    name_proj : str, optional, default=None
        Name of the project. If None, the name of the project is inferred from the save_dir.
    **kwargs : dict
        Additional arguments passed to :class:`pytorch_lightning.core.module.LightningModule`.
    """

    CHECKPOINT_HYPER_PARAMS_EXTRA_KEY = "__hparams_extra__"  # key for extra hyperparameters in checkpoint

    CHECKPOINT_DIR = "checkpoints"

    def __init__(
        self,
        input_ml_dblock: InputML,
        output_ml_dblock: OutputML,
        layer_widths: List[int],
        latent_dim: int,
        heads_layer_widths: Dict[str, List[int]] = {},
        custom_losses: Dict[str, Callable[[torch.Tensor, torch.Tensor], torch.Tensor]] = None,
        loss_weights: Dict[str, float] = None,
        activation: str = "leaky_relu",
        optimizer: torch.optim.Optimizer = None,
        name: str = "CondAEModel",
        save_dir: str = None,
        name_proj: str = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        # Save the hyperparameters
        # Ignore the datapath, since it differs between machines
        self.save_hyperparameters(ignore=["save_dir"])

        # Dictionary mapping from input feature names to tuples, where the first element in the tuple is the encoding head to be prepended to the encoder,
        # and the second element is the decoding head to be appended to the decoder.
        self.x_heads = {
            x_dobj.name: x_dobj.get_ml_heads(heads_layer_widths.get(x_dobj.name, []), layer_widths[0], activation, **kwargs) for x_dobj in input_ml_dblock.dobj_list_transf
        }

        # Dictionary mapping from output feature names to tuples, where the first element in the tuple is the encoding head to be prepended to the decoder,
        # and the second element is the decoding head to be appended to the encoder.
        self.y_heads = {
            y_dobj.name: y_dobj.get_ml_heads(heads_layer_widths.get(y_dobj.name, []), layer_widths[-1], activation, **kwargs) for y_dobj in output_ml_dblock.dobj_list_transf
        }

        # Build the encoder based on the above head dictionaries. The encoder is a surrogate model predicting y and z.
        self.encoder = Encoder(
            {x_key: x_heads[0] for x_key, x_heads in self.x_heads.items()},
            {y_key: y_heads[1] for y_key, y_heads in self.y_heads.items()},
            self.x_head_splits_in,
            layer_widths,
            latent_dim,
            activation,
        )
        # Build the decoder based on the above head dictionaries.
        self.decoder = Decoder(
            {y_key: y_heads[0] for y_key, y_heads in self.y_heads.items()},
            {x_key: x_heads[1] for x_key, x_heads in self.x_heads.items()},
            self.y_head_splits_in,
            layer_widths[::-1],
            latent_dim,
            activation,
        )

        self.input_ml_dblock = input_ml_dblock
        self.output_ml_dblock = output_ml_dblock

        self.save_dir = save_dir or os.getcwd()
        self.name_proj = name_proj or basename(self.save_dir)

        self.name = name
        self.layer_widths = layer_widths
        self.latent_dim = latent_dim
        self.heads_layer_widths = heads_layer_widths

        self.custom_losses = custom_losses if custom_losses else {}
        self.loss_weights = loss_weights if loss_weights else {}
        self.feature_losses = {dobj.name: dobj.get_objective() for dobj in input_ml_dblock.dobj_list_transf + output_ml_dblock.dobj_list_transf}

        self.activation = activation
        self.optimizer = optimizer

        self.model_trainer = None  # Set in the fit method

        # Attributes to store extra parameters
        self.datamodule_parameters = None
        self.datamodule_checksum = None
        self._hparams_extra = getattr(self, "_hparams_extra", set())

        # Internal state variables
        self._predict_step_return_postprocessed = True  # Controls the predict_step method to return postprocessed data

    @property
    def x_head_splits_in(self) -> Dict[str, Tuple[int, int]]:
        """Get the input splits for the x heads."""
        return self._head_splits_helper(self.x_heads)[0]

    @property
    def x_head_splits_out(self) -> Dict[str, Tuple[int, int]]:
        """Get the output splits for the x heads."""
        return self._head_splits_helper(self.x_heads)[1]

    @property
    def y_head_splits_in(self) -> Dict[str, Tuple[int, int]]:
        """Get the input splits for the y heads."""
        return self._head_splits_helper(self.y_heads)[0]

    @property
    def y_head_splits_out(self) -> Dict[str, Tuple[int, int]]:
        """Get the output splits for the y heads."""
        return self._head_splits_helper(self.y_heads)[1]

    @staticmethod
    def _head_splits_helper(heads: Dict[str, Tuple[InHead, OutHead]]) -> Tuple[Dict[str, Tuple[int, int]], Dict[str, Tuple[int, int]]]:
        """Helper function to get the input and output splits for the heads."""
        splits_in = [0] + np.cumsum([head[0].in_channels for head in heads.values()]).tolist()
        splits_out = [0] + np.cumsum([head[1].out_channels for head in heads.values()]).tolist()

        splits_in = {key: (splits_in[i], splits_in[i + 1]) for i, key in enumerate(heads.keys())}
        splits_out = {key: (splits_out[i], splits_out[i + 1]) for i, key in enumerate(heads.keys())}
        return splits_in, splits_out

    def split_x_head_in(self, x: Union[np.ndarray, torch.Tensor]) -> Dict[str, Union[np.ndarray, torch.Tensor]]:
        """Helper function to split the input of the model into the different heads."""
        return self._split_head_helper(x, self.x_head_splits_in, self.encoder.in_heads)

    def split_x_head_out(self, x: Union[np.ndarray, torch.Tensor]) -> Dict[str, Union[np.ndarray, torch.Tensor]]:
        """Helper function to split the output of the model into the different heads."""
        return self._split_head_helper(x, self.x_head_splits_out, self.decoder.out_heads)

    def split_y_head_in(self, y: Union[np.ndarray, torch.Tensor]) -> Dict[str, Union[np.ndarray, torch.Tensor]]:
        """Helper function to split the input of the model into the different heads."""
        return self._split_head_helper(y, self.y_head_splits_in, self.decoder.in_heads)

    def split_y_head_out(self, y: Union[np.ndarray, torch.Tensor]) -> Dict[str, Union[np.ndarray, torch.Tensor]]:
        """Helper function to split the output of the model into the different heads."""
        return self._split_head_helper(y, self.y_head_splits_out, self.encoder.out_heads)

    def split_xy_out(
        self, x: Union[np.ndarray, torch.Tensor], y: Union[np.ndarray, torch.Tensor]
    ) -> Tuple[Dict[str, Union[np.ndarray, torch.Tensor]], Dict[str, Union[np.ndarray, torch.Tensor]]]:
        """Splits the output of the model according to the x and y heads."""
        return self.split_x_head_out(x), self.split_y_head_out(y)

    def split_xy_in(
        self, x: Union[np.ndarray, torch.Tensor], y: Union[np.ndarray, torch.Tensor]
    ) -> Tuple[Dict[str, Union[np.ndarray, torch.Tensor]], Dict[str, Union[np.ndarray, torch.Tensor]]]:
        """Splits the input of the model according to the x and y heads."""
        return self.split_x_head_in(x), self.split_y_head_in(y)

    @staticmethod
    def _split_head_helper(data, head_splits, heads):
        """Helper function to split the input of the model into the different heads."""
        return {key: data[:, head_splits[key][0] : head_splits[key][1]] for key in heads.keys()}

    def configure_optimizers(self):
        """
        Configure the optimizers for the model.

        Returns
        -------
        dict
            A dictionary containing the optimizer(s) and learning rate scheduler(s) to be used during training.
        """
        # Initialize the optimizer with Adam, using the model parameters as the input arguments
        optimizer = self.optimizer if self.optimizer is not None else torch.optim.Adam(self.parameters())

        # Initialize the learning rate scheduler with ReduceLROnPlateau
        # This scheduler reduces the learning rate when the validation loss stops improving
        lr_scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=6, verbose=True)

        return {
            "optimizer": optimizer,
            "lr_scheduler": {
                "scheduler": lr_scheduler,
                "monitor": "val" + SEP_LOSSES + "loss",
            },
        }

    def _step(
        self, batch: Tuple[torch.Tensor, torch.Tensor], batch_idx: int, mode: str, step_ae: bool = True, postprocess=False
    ) -> Tuple[Dict[str, torch.Tensor], Dict[str, float]]:
        """
        Process a single batch of data.

        Parameters
        ----------
        batch : Tuple[torch.Tensor, torch.Tensor]
            A tuple of tensors containing the data for a single batch.
        batch_idx : int
            The index of the current batch.
        mode: str
            The mode in which the model is being run (either 'train' or 'val').
        step_ae : bool, optional, default=True
            Just to specify if the step is for an AE model or not. If True, the z_loss is computed.

        Returns
        -------
        Tuple[Dict[str, torch.Tensor], Dict[str, float]]
            A tuple where the first element is a dictionary with predictions, and the second element a dictionary with losses for the batch.
        """
        x, y = batch
        pred = self(batch)

        x_pred, y_pred = self.split_xy_out(pred["x"], pred["y"])
        x_real, y_real = self.split_xy_in(x, y)

        # Calculate the losses for the features in the decoder
        x_losses = {key: self.feature_losses[key](x_pred[key], x_real[key]) for key in self.decoder.out_heads.keys()}
        x_loss = torch.stack(list(x_losses.values()), dim=0).sum()

        # Calculate the losses for the features in the encoder
        y_losses = {key: self.feature_losses[key](y_pred[key], y_real[key]) for key in self.encoder.out_heads.keys()}
        y_loss = torch.stack(list(y_losses.values()), dim=0).sum() if len(y_losses) > 0 else 0.0

        # calculate only if decorrelation weight is > 0 to avoid computing gradients for nothing
        if self.loss_weights.get("decorrelation", 0) > 0 and len(self.encoder.out_heads) > 0:
            # decorrelate by reducing the covariance: https://arxiv.org/abs/1904.01277v1
            decorrelation_loss = ((pred["z"].T @ ((y - y.mean(axis=0)) / y.std(axis=0))) ** 2).mean()
        else:
            # weight is zero, so decorrelation_loss is detached from the graph
            decorrelation_loss = 0.0

        custom_losses = {
            name: self.loss_weights.get(name, 1.0) * custom_loss(x_pred | y_pred | {key: pred[key] for key in pred.keys() if key not in ["x", "y"]}, x_real | y_real)
            for name, custom_loss in self.custom_losses.items()
        }

        total_loss = (
            self.loss_weights.get("x", 1.0) * x_loss
            + self.loss_weights.get("y", 1.0) * y_loss
            + self.loss_weights.get("decorrelation", 0.0) * decorrelation_loss
            + (torch.stack(list(custom_losses.values()), dim=0).sum() if len(self.custom_losses) > 0 else 0)
        )

        loss_dict = (
            {
                mode + SEP_LOSSES + "loss": total_loss,
                mode + SEP_LOSSES + "features_loss": x_loss + y_loss,
                mode + SEP_LOSSES + "decorrelation_loss": decorrelation_loss,
            }
            | {mode + SEP_LOSSES + key + "_loss": value for key, value in x_losses.items()}
            | {mode + SEP_LOSSES + key + "_loss": value for key, value in y_losses.items()}
            | {mode + SEP_LOSSES + key: value for key, value in custom_losses.items()}
        )

        # this could now be moved to custom losses which would restore proper inheritance with VAE (no more step_ae flag)
        if step_ae:
            z_loss = losses.LossStd()(pred["z"])
            total_loss += self.loss_weights.get("z", 1.0) * z_loss
            loss_dict[mode + SEP_LOSSES + "z_loss"] = z_loss

        if postprocess:
            pred["x"] = self._postprocess_x(x_pred)
            pred["y"] = self._postprocess_y(y_pred)

        return pred, loss_dict

    def forward(self, data: Tuple[torch.Tensor, torch.Tensor]) -> Dict[str, torch.Tensor]:
        """
        Forward pass of the model.

        Parameters
        ----------
        data : Tuple[torch.Tensor, torch.Tensor]
            A tuple containing input data tensors, where the first element is 'x' and the second element is the conditional part 'y'.

        Returns
        -------
        Dict[str, torch.Tensor]
            A dictionary containing the model's output tensors. This could include the latent representation 'z', the reconstructed 'y', and the reconstructed 'x'.
        """
        x, y = data

        pred = self.encoder(x)
        pred.update(self.decoder({"z": pred["z"], "y": y}))

        return pred

    def training_step(self, batch: Tuple[torch.Tensor, torch.Tensor], batch_idx: int) -> float:
        """
        Perform a single training step.

        Parameters
        ----------
        batch : Tuple[torch.Tensor, torch.Tensor]
            A tuple containing the data for a single batch.
        batch_idx : int
            The index of the current batch.

        Returns
        -------
        float
            The training loss.
        """
        # Process the batch and retrieve the loss dictionary
        _, loss_dict = self._step(batch, batch_idx, mode="train")

        # Log the loss values to various outputs
        self.log_dict(loss_dict, on_step=True, on_epoch=False, prog_bar=True, logger=True)
        return loss_dict["train" + SEP_LOSSES + "loss"]

    def validation_step(self, batch: Tuple[torch.Tensor, torch.Tensor], batch_idx: int) -> float:
        """
        Perform a single validation step.

        Parameters
        ----------
        batch : Tuple[torch.Tensor, torch.Tensor]
            A tuple containing the data for a single batch.
        batch_idx : int
            The index of the current batch.

        Returns
        -------
        float
            The validation loss.
        """
        # Process the batch and retrieve the loss dictionary
        _, loss_dict = self._step(batch, batch_idx, mode="val")

        # Log the loss values to various outputs
        self.log_dict(loss_dict, on_step=False, on_epoch=True, prog_bar=True, logger=True)
        return loss_dict["val" + SEP_LOSSES + "loss"]

    def test_step(self, batch: Tuple[torch.Tensor, torch.Tensor], batch_idx: int) -> float:
        """
        Perform a single test step.

        Parameters
        ----------
        batch : Tuple[torch.Tensor, torch.Tensor]
            A tuple containing the data for a single batch.
        batch_idx : int
            The index of the current batch.

        Returns
        -------
        float
            The test loss.
        """
        # Process the batch and retrieve the loss dictionary
        _, loss_dict = self._step(batch, batch_idx, mode="test")

        # Log the loss values to various outputs
        self.log_dict(loss_dict, on_step=False, on_epoch=True, prog_bar=True, logger=True)
        return loss_dict["test" + SEP_LOSSES + "loss"]

    def predict_step(self, batch: Union[Tuple[torch.Tensor, torch.Tensor], Tuple[torch.Tensor, torch.Tensor, torch.Tensor]], batch_idx: int) -> Dict[str, torch.Tensor]:
        """
        Perform a single prediction step. Depending on the input, the encoder, decoder, or the entire model is used.

        Parameters
        ----------
        batch : Tuple[torch.Tensor, torch.Tensor]
            A tuple containing the data for a single batch.
        batch_idx : int
            The index of the current batch.

        Returns
        -------
        Dict[str, torch.Tensor]
            A dictionary containing the model's output tensors. This could include the latent representation 'z', the reconstructed 'y', and the reconstructed 'x'.
        """
        if len(batch) > 2:
            x, y, z = batch
        else:
            x, y = batch
            z = None  # set to None, z is sampled in the decode method

        # If x and y are provided we pass them to the entire model (forward evaluation + inverse evaluation)
        if x.numel() > 0 and y.numel() > 0:
            pred = self(batch)
        elif x.numel() > 0:
            # If only x is provided we encode it (forward evaluation)
            pred = self.encode(x)
        elif y.numel() > 0:
            # If only y is provided we decode it (inverse evaluation), optionally with a given latent representation z
            pred = {"x": self.decode(y, z=z)}
        else:
            raise ValueError("Invalid batch format.")

        # Postprocess the predictions
        if "x" in pred.keys() and self._predict_step_return_postprocessed:
            pred["x"] = self._postprocess_x(pred["x"])
        if "y" in pred.keys() and self._predict_step_return_postprocessed:
            pred["y"] = self._postprocess_y(pred["y"])
        return pred

    def _postprocess_x(self, x: Union[torch.Tensor, Dict[str, torch.Tensor]], return_dict: bool = False) -> Union[torch.Tensor, Dict[str, torch.Tensor]]:
        """Helper method to postprocess the output from the x-heads"""
        if not isinstance(x, dict):
            x = self.split_x_head_out(x)

        x = {key: self.decoder.out_heads[key].postprocess(x[key]) for key in x.keys()}

        if return_dict:
            return x
        else:
            return torch.cat([x[key] for key in x.keys()], dim=-1)

    def _postprocess_y(self, y: Union[torch.Tensor, Dict[str, torch.Tensor]], return_dict: bool = False) -> Union[torch.Tensor, Dict[str, torch.Tensor]]:
        """Helper method to postprocess the output from the y-heads"""
        if not isinstance(y, dict):
            y = self.split_y_head_out(y)

        y = {key: self.encoder.out_heads[key].postprocess(y[key]) for key in y.keys()}

        if return_dict:
            return y
        else:
            return torch.cat([y[key] for key in y.keys()], dim=-1)

    def encode(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
        """
        Encode the input data into a latent representation.

        Parameters
        ----------
        x : torch.Tensor
            The input data.

        Returns
        -------
        Dict[str, torch.Tensor]
            A dictionary containing the latent representation 'z' and the conditional part 'y'.
        """
        return self.encoder(x)

    def decode(self, y: Union[np.ndarray, torch.Tensor], z: Union[np.ndarray, torch.Tensor, None] = None) -> torch.Tensor:
        """
        Decode the latent representation into the original data space.

        Parameters
        ----------
        y : torch.Tensor
            The conditional data.
        z : Union[np.ndarray, torch.Tensor]
            The latent representation to decode. If None, a latent representation is sampled from a normal distribution.

        Returns
        -------
        torch.Tensor
            A tensor containing the reconstructed (generated) data.
        """
        if z is None or z.numel() == 0:
            # Added self.device as it seems it cannot handle the passing to the device in the forward method
            z = torch.normal(mean=0.0, std=1.0, size=(len(y), self.latent_dim)).to(self.device)

        z = z.float() if torch.is_tensor(z) else torch.from_numpy(z).float()
        y = y.float() if torch.is_tensor(y) else torch.from_numpy(y).float()
        return self.decoder({"z": z, "y": y})["x"]

    def _check_datamodule(self, datamodule: DataModule, parameters_only: bool = True) -> DataModule:
        """Some basic checks to make sure that data module is compatible with the model and the corresponding stage."""
        params = datamodule.get_parameters()

        # Check general compatibility. We only check dimensions, so it is still possible that the training/validating/testing will fail.
        input_ml_dblock = params.pop("input_ml_dblock")
        input_ml_checks = (input_ml_dblock.get_dobj_dimensions(flag_transf=True) == self.input_ml_dblock.get_dobj_dimensions(flag_transf=True)) and (
            input_ml_dblock.get_dobj_dimensions(flag_transf=False) == self.input_ml_dblock.get_dobj_dimensions(flag_transf=False)
        )

        output_ml_dblock = params.pop("output_ml_dblock")
        output_ml_checks = (output_ml_dblock.get_dobj_dimensions(flag_transf=True) == self.output_ml_dblock.get_dobj_dimensions(flag_transf=True)) and (
            output_ml_dblock.get_dobj_dimensions(flag_transf=False) == self.output_ml_dblock.get_dobj_dimensions(flag_transf=False)
        )
        if not (input_ml_checks and output_ml_checks):
            raise ValueError(
                "The input_ml and output_ml of the model and the datamodule are not compatible. "
                "Make sure that the model was initialized with the same input_ml and output_ml as the datamodule e.g., with CondAEModel.from_datamodule(...)."
            )

        if self.datamodule_parameters is not None:
            # Check that the other datamodule parameters are the same as the ones used to initialize the model
            datamodule_params = copy.deepcopy(self.datamodule_parameters)
            datamodule_params.pop("input_ml_dblock")
            datamodule_params.pop("output_ml_dblock")

            # Check that the datamodule parameters are the same as the ones used to initialize the model
            if datamodule_params != params:
                raise ValueError(
                    "The datamodule parameters are not the same as the ones used to initialize the model. "
                    "Make sure that the model was initialized with the same parameters as the datamodule e.g., with CondAEModel.from_datamodule(...)."
                )

        # Check that the data of the datamodule has not changed since the model was initialized
        if self.datamodule_checksum is not None and not parameters_only and self.datamodule_checksum != datamodule.get_checksum():
            warnings.warn("The data of the DataModule has changed since the model was initialized. This may lead to inaccurate validation and test results.")

        return datamodule

    def fit(
        self,
        datamodule: DataModule,
        name_run: Optional[str] = "",
        max_epochs: int = 100,
        callbacks: Optional[Union[Callback, List[Callback]]] = None,
        loggers: Optional[Union[Logger, Iterable[Logger]]] = None,
        accelerator: str = "auto",
        flag_early_stop: bool = False,
        criteria: str = "train" + SEP_LOSSES + "loss",
        flag_wandb: bool = False,
        wandb_entity: Optional[str] = None,
        **kwargs,
    ) -> None:
        """
        Train the model on the provided data using PyTorch Lightning's Trainer.

        Parameters
        ----------
        datamodule : pl.LightningDataModule
            The data module object that provides the training, validation, and test data.
        name_run : str, optional, default="NoName"
            Name of the current run, used for logging and saving checkpoints. Not used if flag_wandb is True.
        max_epochs : int, optional, default=100
            The maximum number of epochs to train the model.
        callbacks : Union[Callback, List[Callback]], optional, default=None
            List of callbacks or a single callback to be used during training.
        loggers : Union[Logger, Iterable[Logger]], optional, default=None
            List of logger instances or a single logger for logging training progress and metrics.
        accelerator : str, optional, default="auto"
            Supports passing different accelerator types ("cpu", "gpu", "tpu", "ipu", "hpu", "mps", "auto").
        flag_early_stop : bool, optional, default=False
            If True, enable early stopping based on the provided criteria.
        criteria : str, optional, default="train{`aixd.mlmodel.constants.SEP_LOSSES`}loss"
            The criteria used for early stopping.
        flag_wandb : bool, optional, default=False
            If True, enable logging using Weights & Biases (wandb).
        wandb_entity : str, optional, default=None
            If flag_wandb is True, the entity (username or team) to which the run will be logged. If None, the default entity is used.
        **kwargs
            Additional keyword arguments that can be passed to the Trainer. Default is an empty dictionary.
        """
        datamodule = self._check_datamodule(datamodule, parameters_only=False)

        if isinstance(callbacks, Callback):
            callbacks = [callbacks]
        callbacks = callbacks or []  # if callbacks is None set to empty list

        # Save some extra parameters
        self.save_extra_parameters(**{"max_epochs": max_epochs, "flag_early_stop": flag_early_stop, "criteria": criteria})

        if loggers is not None and flag_wandb:
            warnings.warn("Both loggers and flag_wandb are set. flag_wandb is ignored.")
            flag_wandb = False

        from coolname import generate_slug

        if flag_wandb:
            from pytorch_lightning.loggers.wandb import WandbLogger

            # We add an extra string to differentiate the runs
            name_run = "" if name_run is None else name_run
            name_run += "_" + generate_slug(2)  # WandB defines the name of the run by the version number
            loggers = WandbLogger(project=self.name_proj, name=name_run, save_dir=self.save_dir, entity=wandb_entity)

            # Saving extra parameters to wandb
            loggers.log_hyperparams({key: getattr(self, key) for key in self._hparams_extra})
            loggers.log_hyperparams({"datamodule_parameters": datamodule.get_parameters()})

        name_run = generate_slug(2) if name_run is None or name_run == "" else name_run

        # Setup checkpoint callback
        checkpoint_filename = self._checkpoint_filename(name_run, n_samples=len(datamodule.x_train))

        # If there is already a last checkpoint, its name is changed
        if os.path.exists(os.path.join(self.save_dir, self.CHECKPOINT_DIR, "last.ckpt")):
            date_f = self._get_file_creation_date(os.path.join(self.save_dir, self.CHECKPOINT_DIR, "last.ckpt"))
            os.rename(os.path.join(self.save_dir, self.CHECKPOINT_DIR, "last.ckpt"), os.path.join(self.save_dir, self.CHECKPOINT_DIR, "last_" + date_f + ".ckpt"))

        callbacks.append(
            ModelCheckpoint(
                monitor=criteria,
                save_top_k=2,
                mode="min",
                auto_insert_metric_name=False,
                save_last=True,
                dirpath=os.path.join(self.save_dir, self.CHECKPOINT_DIR),
                filename=checkpoint_filename,
            )
        )

        # Setup early stopping callback
        if flag_early_stop:
            from pytorch_lightning.callbacks.early_stopping import EarlyStopping

            if any(isinstance(callback, EarlyStopping) for callback in callbacks):
                warnings.warn("EarlyStopping is already in callbacks, and is not added again.")
                pass
            else:
                callbacks.append(EarlyStopping(monitor=criteria, mode="min", patience=8))

        # Create a model_trainer object and fit the model
        self.model_trainer = pl.Trainer(
            accelerator=accelerator,
            max_epochs=max_epochs,
            callbacks=callbacks,
            logger=loggers if loggers else None,
            default_root_dir=self.save_dir,
            **kwargs,
        )
        self.model_trainer.fit(self, datamodule=datamodule)

        if flag_wandb:
            import wandb

            wandb.finish()

    def validate(self, datamodule: DataModule, accelerator: str = "auto", **kwargs) -> Dict[str, float]:
        """
        Evaluate the model on the validation data.

        Parameters
        ----------
        datamodule : DataModule
            The data module object that provides validation data.
        accelerator : str, optional, default="auto"
            Supports passing different accelerator types ("cpu", "gpu", "tpu", "ipu", "hpu", "mps", "auto").

        Returns
        -------
        Dict[str, float]
            A dictionary containing the validation loss and metrics.
        """
        datamodule = self._check_datamodule(datamodule, parameters_only=False)

        # Create a model_trainer object if one does not already exist
        if self.model_trainer is None:
            self.model_trainer = pl.Trainer(accelerator=accelerator, default_root_dir=self.save_dir, **kwargs)

        return rec_concat_dict(self.model_trainer.validate(self, datamodule=datamodule))

    def get_evaluation_losses(self, use_objective: bool = False) -> Dict[str, nn.Module]:
        return {
            dobj.name: dobj.get_objective(reduction="none") if use_objective else dobj.get_loss_evaluation()
            for dobj in self.input_ml_dblock.dobj_list_transf + self.output_ml_dblock.dobj_list_transf
        }

    def evaluate(
        self,
        data: Union[DataModule, Tuple[torch.Tensor, torch.Tensor], Tuple[np.ndarray, np.ndarray]],
        untransform: bool = False,
        use_objective: bool = False,
        losses_evaluate: Optional[Dict[str, nn.Module]] = None,
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Evaluate the model on the validation data. This method is similar to :meth:`CondAEModel.validate`, but allows to compute the losses in the untransformed space.

        Depending on the argument `untransform`, the losses computation is applied on the transformed or untransformed (and non post-processed) data. Hence, one has to be careful
        when providing the losses to be evaluated, as they should be consistent with the data space - or better work in both spaces.

        Parameters
        ----------
        data : Union[DataModule, Tuple[torch.Tensor, torch.Tensor], Tuple[np.ndarray, np.ndarray]]
            The data module object that provides validation data. Alternatively, a tuple of input and output tensors can be provided.
        untransform : bool, optional, default=False
            If True, the losses are computed in the untransformed space (i.e., the original space).
        use_objective : bool, optional, default=False
            If True, the losses are computed using the objective functions of the data objects. Requires untransform=False.
        losses_evaluate : Optional[Dict[str, nn.Module]], optional, default=None
            A dictionary containing the losses to be evaluated. If None, the losses are computed using loss defined by DataObject.get_loss_evaluation().

        Returns
        -------
        Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]
            A tuple containing the evaluation losses for the input and output features, as well as
            the values predicted for input and output features.
        """

        if isinstance(data, DataModule):
            datamodule = self._check_datamodule(data, parameters_only=False)
            dataloader = datamodule.val_dataloader()
        elif isinstance(data, tuple):
            x, y = data
            if self.datamodule_parameters is None:
                raise ValueError("The model was not initialized from a DataModule, so the data module can not be recovered.")
            datamodule = DataModule.from_parameters(x, y, predict=True, **self.datamodule_parameters)
            dataloader = datamodule.predict_dataloader()
        else:
            raise ValueError("The data should be a DataModule object or a tuple of torch tensors.")

        if untransform and use_objective:
            logger.warning("The use_objective flag is ignored when untransform=True, as the losses are computed in the untransformed space.")
            use_objective = False

        losses_evaluate = self.get_evaluation_losses(use_objective=use_objective) | (losses_evaluate or {})  # overwrite the losses if provided

        # Make the predictions, and split them according to the input and output heads
        # Remark: Un-transformed predictions are split according to the input splits, assuming that transformations do not change the dimensions
        pred, pred_untransformed = self.predict(dataloader, return_untransformed=True, return_postprocessed=False)
        x_pred, y_pred = self.split_x_head_out(pred["x"]), self.split_y_head_out(pred["y"])
        x_pred_untransformed, y_pred_untransformed = self.split_x_head_in(pred_untransformed["x"]), self.split_y_head_in(pred_untransformed["y"])

        # Get the true values, and split them according to the input and output heads
        x_true, y_true = torch.cat([xyz[0] for xyz in dataloader]), torch.cat([xyz[1] for xyz in dataloader])
        x_true_untransformed, y_true_untransformed = datamodule.inverse_transform(x_true, y_true)
        x_true_untransformed, y_true_untransformed = self.split_x_head_in(x_true_untransformed), self.split_y_head_in(y_true_untransformed)
        x_true, y_true = self.split_x_head_in(x_true), self.split_y_head_in(y_true)

        # Evaluate the losses for the input and output features
        y_eval_losses = self.calc_y_losses_calculation(y_pred, y_true, y_pred_untransformed, y_true_untransformed, untransform, use_objective, losses_evaluate)
        x_eval_losses = self.calc_x_losses_calculation(x_pred, x_true, x_pred_untransformed, x_true_untransformed, untransform, use_objective, losses_evaluate)

        # Convert the predictions to pandas DataFrames
        if untransform:
            x_pred = pd.DataFrame(ut.to_numpy(pred_untransformed["x"]), columns=self.input_ml_dblock.columns_df)
            y_pred = pd.DataFrame(ut.to_numpy(pred_untransformed["y"]), columns=self.output_ml_dblock.columns_df)
        else:
            x_pred = pd.DataFrame(ut.to_numpy(self._postprocess_x(pred["x"])), columns=self.input_ml_dblock.columns_df_transf)
            y_pred = pd.DataFrame(ut.to_numpy(self._postprocess_y(pred["y"])), columns=self.output_ml_dblock.columns_df_transf)

        return x_eval_losses, y_eval_losses, x_pred, y_pred

    def calc_y_losses_calculation(
        self,
        y_in: Dict[str, Union[torch.Tensor, np.ndarray]],
        y_target: Dict[str, Union[torch.Tensor, np.ndarray]],
        y_in_untransf: Dict[str, Union[torch.Tensor, np.ndarray]],
        y_target_untransf: Dict[str, Union[torch.Tensor, np.ndarray]],
        untransform: bool = False,
        use_objective: bool = False,
        losses_evaluate: Optional[Dict[str, nn.Module]] = None,
    ) -> pd.DataFrame:
        if losses_evaluate is None:
            losses_evaluate = self.get_evaluation_losses(use_objective=use_objective) | (losses_evaluate or {})  # overwrite the losses if provided

        y_eval_losses = {
            key: (
                losses_evaluate[key](to_torch(y_in[key]), to_torch(y_target[key]))
                if isinstance(self.encoder.out_heads[key], CategoricalOutHead) or not untransform
                else losses_evaluate[key](to_torch(y_in_untransf[key]), to_torch(y_target_untransf[key]))
            )
            for key in self.encoder.out_heads.keys()
        }
        # Concatenate the losses for all the batches, and convert to pandas DataFrame
        # For evaluation losses of data objects of dim n, we assume that the losses are of shape (*, n) or (*, 1)
        y_eval_losses = self._to_loss_dataframe(y_eval_losses, self.output_ml_dblock.dobj_list if untransform else self.output_ml_dblock.dobj_list_transf)

        return y_eval_losses

    def calc_x_losses_calculation(
        self,
        x_in: Dict[str, Union[torch.Tensor, np.ndarray]],
        x_target: Dict[str, Union[torch.Tensor, np.ndarray]],
        x_in_untransf: Dict[str, Union[torch.Tensor, np.ndarray]],
        x_target_untransf: Dict[str, Union[torch.Tensor, np.ndarray]],
        untransform: bool = False,
        use_objective: bool = False,
        losses_evaluate: Optional[Dict[str, nn.Module]] = None,
    ) -> pd.DataFrame:
        if losses_evaluate is None:
            losses_evaluate = self.get_evaluation_losses(use_objective=use_objective) | (losses_evaluate or {})  # overwrite the losses if provided

        x_eval_losses = {
            key: (
                losses_evaluate[key](to_torch(x_in[key]), to_torch(x_target[key]))
                if isinstance(self.decoder.out_heads[key], CategoricalOutHead) or not untransform
                else losses_evaluate[key](to_torch(x_in_untransf[key]), to_torch(x_target_untransf[key]))
            )
            for key in self.decoder.out_heads.keys()
        }
        # Concatenate the losses for all the batches, and convert to pandas DataFrame
        # For evaluation losses of data objects of dim n, we assume that the losses are of shape (*, n) or (*, 1)
        x_eval_losses = self._to_loss_dataframe(x_eval_losses, self.input_ml_dblock.dobj_list if untransform else self.input_ml_dblock.dobj_list_transf)

        return x_eval_losses

    @staticmethod
    def _to_loss_dataframe(loss_dict: Dict[str, torch.Tensor], dobj_list: List[DataObject]) -> pd.DataFrame:
        """Converts a dictionary of losses to a pandas DataFrame, by inferring the column names from the data objects."""
        dobj_dict = {dobj.name: dobj for dobj in dobj_list}
        loss_dict = {key: loss if len(loss.size()) > 1 else loss.unsqueeze(-1) for key, loss in loss_dict.items()}

        if set(dobj_dict.keys()) != set(loss_dict.keys()):
            raise ValueError(f"Losses dictionary keys do not match the data objects. Expected keys are {set(dobj_dict.keys())}, but got {set(loss_dict.keys())}.")

        columns = []
        for key, loss in loss_dict.items():
            if loss.size(1) == dobj_dict[key].dim:
                columns.extend(dobj_dict[key].columns_df)
            elif loss.size(1) == 1:
                columns.append(dobj_dict[key].name)
            else:
                raise ValueError(f"Loss tensor has wrong shape. Expected shape is (*, {dobj_dict[key].dim}) or (*, 1), but got (*, {loss.size(1)}).")

        return pd.DataFrame(torch.cat(list(loss_dict.values()), dim=1).cpu().detach().numpy(), columns=columns)

    def test(self, datamodule: DataModule, accelerator: str = "auto", **kwargs) -> Dict[str, float]:
        """
        Evaluate the model on the test data.

        Parameters
        ----------
        datamodule : DataModule
            A compatible data module object that provides test data.
        accelerator : str, optional, default="auto"
            Which accelerator should be used (e.g. cpu, gpu, mps, etc.).

        Returns
        -------
        Dict[str, float]
            A dictionary containing the test loss and metrics.
        """
        datamodule = self._check_datamodule(datamodule, parameters_only=False)

        # Create a model_trainer object if one does not already exist
        if self.model_trainer is None:
            self.model_trainer = pl.Trainer(accelerator=accelerator, default_root_dir=self.save_dir, **kwargs)

        return rec_concat_dict(self.model_trainer.test(self, datamodule=datamodule))

    def predict(
        self,
        data: Union[DataModule, DataLoader, tuple],
        return_untransformed: bool = False,
        return_postprocessed: bool = True,
        accelerator: str = "cpu",
        enable_progress_bar: bool = False,
        lightning_logger_level: int = logging.WARNING,
        disable_user_warnings: bool = False,
        **kwargs,
    ) -> Union[Dict[str, torch.Tensor], Tuple[Dict[str, torch.Tensor], Dict[str, torch.Tensor]]]:
        """
        Make predictions using the model.

        Parameters
        ----------
        data : Union[DataModule, DataLoader, tuple]
            A DataModule object, a PyTorch DataLoader object, or a tuple of two (or three) PyTorch Tensors or numpy arrays, containing data from which to make predictions.
        return_untransformed : bool, optional, default=False
            If True, the predictions are additionally returned in the original space, by applying the inverse transformation.
        return_postprocessed : bool, optional, default=True
            If True, the model predictions are returned in post-processed. For accessing the raw model outputs, e.g., class logits/probabilities for categorical data set this flag to False.
        accelerator : str, optional, default="cpu"
            Which accelerator should be used (e.g. cpu, gpu, mps, etc.).
        enable_progress_bar : bool, optional, default=False
            If True, enable the progress bar.
        lightning_logger_level : int, optional, default=logging.WARNING
            The logging level for PyTorch Lightning.
        disable_user_warnings : bool, optional, default=False
            If True, disable user warnings.
        **kwargs
            Additional keyword arguments that can be passed to the Trainer. Default is an empty dictionary.

        Returns
        -------
        Union[Dict[str, torch.Tensor], Tuple[Dict[str, torch.Tensor], Dict[str, torch.Tensor]]]
            A dictionary containing the model's output tensors. If return_untransformed is True, a tuple of the predicted output data in the transformed and original space
            is returned. Furthermore, if return_postprocessed=False, the predicted output data in the transformed space is returned without post-processing.
        """

        with warnings.catch_warnings():
            if disable_user_warnings:
                warnings.filterwarnings("ignore", category=UserWarning)

            if isinstance(data, DataModule):
                datamodule = data
                self._check_datamodule(datamodule)
                dataloader = datamodule.predict_dataloader()
            elif isinstance(data, DataLoader):
                dataloader = data
            elif isinstance(data, tuple):
                if self.datamodule_parameters is None:
                    raise ValueError("The model was not initialized from a DataModule, so the data module can not be recovered.")
                datamodule = DataModule.from_parameters(**self.datamodule_parameters)
                dataloader = datamodule.convert_to_dataloader(*data)
            else:
                raise ValueError("The data argument must be a DataModule or a tuple of two (or three) tensors or numpy arrays.")

            # Temporary set the logger level to the desired level, by default it is set to WARNING, to disable the GPU warnings
            with temporary_logger_level(logging.getLogger("pytorch_lightning"), lightning_logger_level):
                self._predict_step_return_postprocessed = return_postprocessed  # set the flag for the predict_step method
                pred = pl.Trainer(accelerator=accelerator, enable_progress_bar=enable_progress_bar, logger=False, **kwargs).predict(self, dataloaders=dataloader)
                self._predict_step_return_postprocessed = True  # reset the flag

            pred = rec_concat_dict(pred)

            if return_untransformed:
                return pred, self.to_untransformed_pred(pred, requires_postprocessing=not return_postprocessed)

        return pred

    def predict_y(
        self,
        x: Union[np.ndarray, torch.Tensor],
        return_untransformed: bool = False,
        accelerator: str = "cpu",
        enable_progress_bar: bool = False,
        lightning_logger_level: int = logging.WARNING,
        disable_user_warnings: bool = True,
        **kwargs,
    ) -> Union[np.ndarray, torch.Tensor, Tuple[np.ndarray, torch.Tensor]]:
        """
        Predict the output data given the input data.

        Parameters
        ----------
        x : Union[np.ndarray, torch.Tensor]
            The input data.
        return_untransformed : bool, optional, default=False
            If True, the predictions are also returned in the original space, by applying the inverse transformation.
        accelerator : str, optional, default="cpu"
            Which accelerator should be used (e.g. cpu, gpu, mps, etc.).
        enable_progress_bar : bool, optional, default=False
            If True, enable the progress bar.
        lightning_logger_level : int, optional, default=logging.WARNING
            The logging level for PyTorch Lightning.
        disable_user_warnings : bool, optional, default=True
            If True, disable user warnings.
        **kwargs
            Additional keyword arguments that can be passed to the predict method.

        Returns
        -------
        Union[np.ndarray, torch.Tensor, Tuple[np.ndarray, torch.Tensor]]
            The predicted output data. If return_untransformed is True, a tuple of the predicted output data in the transformed and original space is returned.
        """
        pred = self.predict(
            data=(x, None),
            return_untransformed=return_untransformed,
            accelerator=accelerator,
            enable_progress_bar=enable_progress_bar,
            lightning_logger_level=lightning_logger_level,
            disable_user_warnings=disable_user_warnings,
            **kwargs,
        )

        if return_untransformed:
            pred, pred_untransformed = pred
            return pred["y"], pred_untransformed["y"]
        else:
            return pred["y"]

    def generate(
        self,
        y: Union[np.ndarray, torch.Tensor],
        z: Union[np.ndarray, torch.Tensor, None] = None,
        return_untransformed: bool = False,
        accelerator: str = "cpu",
        enable_progress_bar: bool = False,
        lightning_logger_level: int = logging.WARNING,
        disable_user_warnings: bool = True,
        **kwargs,
    ) -> Union[Dict[str, torch.Tensor], Tuple[Dict[str, torch.Tensor], Dict[str, torch.Tensor]]]:
        """
        Generate samples from the model.

        Parameters
        ----------
        y : torch.Tensor
            The conditional data.
        z : Union[np.ndarray, torch.Tensor, None], optional, default=None
            The latent representation to decode. If None, a latent representation is sampled from a normal distribution.
        return_untransformed : bool, optional, default=False
            If True, the generated data is additionally returned in the original space, by applying the inverse transformation.
        accelerator : str, optional, default="cpu"
            Which accelerator should be used (e.g. cpu, gpu, mps, etc.).
        enable_progress_bar : bool, optional, default=False
            If True, enable the progress bar.
        lightning_logger_level : int, optional, default=logging.WARNING
            The logging level for PyTorch Lightning.
        disable_user_warnings : bool, optional, default=True
            If True, disable user warnings.
        **kwargs
            Additional keyword arguments that can be passed to the Trainer. Default is an empty dictionary.

        Returns
        -------
        Union[Dict[str, torch.Tensor], Tuple[Dict[str, torch.Tensor], Dict[str, torch.Tensor]]]
            A dictionary containing the generated data. If inverse_transform is True, a tuple of the generated data in the transformed and original space is returned.
        """

        data = (None, y, z) if z is not None else (None, y)

        pred = self.predict(
            data=data,
            return_untransformed=return_untransformed,
            accelerator=accelerator,
            enable_progress_bar=enable_progress_bar,
            lightning_logger_level=lightning_logger_level,
            disable_user_warnings=disable_user_warnings,
            **kwargs,
        )

        if return_untransformed:
            pred, pred_untransformed = pred
            return pred["x"], pred_untransformed["x"]
        else:
            return pred["y"]

    def to_untransformed_pred(self, pred: Dict[str, torch.Tensor], requires_postprocessing: bool = False) -> Dict[str, Any]:
        """Convert the model's predictions to the original data space. If requires_postprocessing=True, the predictions are post-processed before un-transforming."""
        pred_untransf = {}
        if "x" in pred.keys():
            pred_untransf["x"] = self.input_ml_dblock.inverse_transform(ut.to_numpy(pred["x"] if not requires_postprocessing else self._postprocess_x(pred["x"])))[0]
        if "y" in pred.keys():
            pred_untransf["y"] = self.output_ml_dblock.inverse_transform(ut.to_numpy(pred["y"] if not requires_postprocessing else self._postprocess_y(pred["y"])))[0]

        return pred_untransf

    def forward_evaluation(
        self,
        data: Union[np.ndarray, torch.Tensor],
        format_out: str = "df",
        input_transformed: bool = False,
        return_untransformed: bool = False,
    ) -> Union[pd.DataFrame, np.ndarray, List[List], Dict, List[Dict], torch.Tensor]:
        """
        Wrapper function of CondAEModel.predict_y() to evaluate the model on the provided data, and return the output in the desired format.

        Parameters
        ----------
        data : Union[pd.DataFrame, np.ndarray, List[List], Dict, List[Dict], torch.Tensor]
            Input data to evaluate in the surrogate model
        format_out : str, optional, default="df"
            The format for the returned output. The possible formats are ["dict", "dict_list", "df_per_obj", "df", "array", "torch", "list"], and default is "df".
        input_transformed : bool, optional, default=False
            If True, the input data is assumed to be already transformed, and no transformation is applied before evaluating the model
        return_untransformed : bool, optional, default=False
            If True, the output is returned in the original space, by applying the inverse transformation.

        Returns
        -------
        Union[pd.DataFrame, np.ndarray, List[List], Dict, List[Dict], torch.Tensor]
            The predictions in the desired format, based on the format_out argument, transformed or in original space based on the return_untransformed argument.
        """
        if format_out not in FORMATS_IO:
            raise ValueError("The format is not valid. Valid format are: {}".format(", ".join(FORMATS_IO)))

        if isinstance(data, pd.DataFrame):
            data = data.drop(["uid"], axis=1) if "uid" in data.columns else data

        if input_transformed:
            # If the input data is already transformed, we just pass the dataset directly to the model
            data = XYZDataset(data).to_data_loader()
        else:
            pass  # do nothing as self.predict_y() will handle the transformation

        pred = self.predict_y(data, return_untransformed=return_untransformed)

        if return_untransformed:
            _, pred_untransf = pred
            return convert_to(pred_untransf, format=format_out, dataobjects=self.output_ml_dblock.dobj_list)
        else:
            return convert_to(pred, format=format_out, dataobjects=self.output_ml_dblock.dobj_list_transf)

    def summary(self, max_depth: int = 1, flag_print: bool = True) -> Union[str, None]:
        """
        Prints a summary of the encoder and decoder, including the number of parameters, the layers,
        their names, and the dimensionality.

        Parameters
        ----------
        max_depth : int, optional, default=1
            Maximum depth of modules to show. Use -1 to show all modules or 0 to show no summary.
        flag_print : bool, optional, default=True
            If True, print the summary to the console. Otherwise, return the summary as a string.
        """
        # Register example input array such that ModelSummary can print data shapes
        self.example_input_array = (
            (
                torch.zeros(1, max([x_dobj.position_index + x_dobj.dim for x_dobj in self.input_ml_dblock.dobj_list_transf])),
                torch.zeros(1, max([y_dobj.position_index + y_dobj.dim for y_dobj in self.output_ml_dblock.dobj_list_transf])),
            ),
        )
        if flag_print:
            print(ModelSummary(self, max_depth=max_depth))
        else:
            return str(ModelSummary(self, max_depth=max_depth))

    @classmethod
    def from_datamodule(cls, datamodule: DataModule, **kwargs) -> CondAEModel:
        """
        Create a model from a data module.

        Parameters
        ----------
        datamodule : DataModule
            The data module object that provides the training, validation, and test data.
        **kwargs
            Additional keyword arguments that can be passed to the model. See CondAEModel.__init__() for more details.

        Returns
        -------
        CondAEModel
            The model object.

        """
        model = cls(input_ml_dblock=datamodule.input_ml_dblock, output_ml_dblock=datamodule.output_ml_dblock, **kwargs)
        model.datamodule_parameters = datamodule.get_parameters()
        model.datamodule_checksum = datamodule.get_checksum()
        return model

    def save_extra_parameters(self, *args: Any, **kwargs) -> None:
        """
        Extra parameters that are saved as part of the model checkpoint. All extra parameters need to be in self.
        One can save extra parameters not yet in self by passing them in kwargs, which will be added to self and self._extra_hparams.

        Parameters
        ----------
        **args : Any
            Extra parameters passed in args need to be in self.
        **kwargs
            Extra parameters passed in kwargs, does not need to be in self.
        """

        for arg in args:
            # Hyperparameters passed in args need to be in self
            if isinstance(arg, str) and hasattr(self, arg):
                self._hparams_extra.add(arg)
            else:
                raise ValueError("Argument {} is not a valid attribute of the model".format(arg))

        # Save kwargs, does not need to be in self, but will be added to self and self._extra_hparams
        for key, value in kwargs.items():
            setattr(self, key, value)
            self._hparams_extra.add(key)

    def on_save_checkpoint(self, checkpoint: Dict[str, Any]) -> None:
        """
        Save the extra hyperparameters to the model checkpoint.

        Parameters
        ----------
        checkpoint : Dict[str, Any]
            The full checkpoint dictionary before it gets dumped to a file.
        """
        checkpoint["datamodule_parameters"] = getattr(self, "datamodule_parameters", None)
        checkpoint["datamodule_checksum"] = getattr(self, "datamodule_checksum", None)  # This is neither a datamodule parameter nor a hyperparameter of the model
        checkpoint[self.CHECKPOINT_HYPER_PARAMS_EXTRA_KEY] = {k: getattr(self, k) for k in self._hparams_extra}

        super().on_save_checkpoint(checkpoint)

    def on_load_checkpoint(self, checkpoint: Dict[str, Any]) -> None:
        """
        Load the extra hyperparameters from the model checkpoint. The data module parameters are also loaded, if they exist.

        Parameters
        ----------
        checkpoint : Dict[str, Any]
            Loaded checkpoint.
        """
        self.datamodule_parameters = checkpoint.get("datamodule_parameters", None)
        self.datamodule_checksum = checkpoint.get("datamodule_checksum", None)
        for k, v in checkpoint[self.CHECKPOINT_HYPER_PARAMS_EXTRA_KEY].items():
            setattr(self, k, v)

        super().on_load_checkpoint(checkpoint)

    @classmethod
    def load_model_from_checkpoint(cls, path: str, **model_kwargs) -> CondAEModel:
        """
        Load a model from a checkpoint file. If the checkpoint is in the default checkpoint directory, then the data path is restored.

        Parameters
        ----------
        path : str
            The path to the checkpoint file.
        **model_kwargs
            Additional keyword arguments that can be passed to the model. See CondAEModel.__init__() for more details.

        Returns
        -------
        CondAEModel
            The loaded model object.

        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Checkpoint file {path} does not exist.")

        if "save_dir" in model_kwargs:
            save_dir = model_kwargs.pop("save_dir")
        elif basename(dirname(path)) == cls.CHECKPOINT_DIR:
            # If the checkpoint is in the default checkpoint directory, then the data path is the parent directory
            save_dir = dirname(dirname(path))
        else:
            save_dir = os.getcwd()
            warnings.warn(f"Checkpoint file {path} is not in the default checkpoint directory. The data path can not be restored, so it will be set to os.getcwd().")

        return cls.load_from_checkpoint(path, save_dir=save_dir, **model_kwargs)

    @staticmethod
    def _checkpoint_filename(name_run: str, n_samples: int, timestamp=True) -> str:
        """
        Generate a checkpoint filename based on the given name and an optional timestamp.

        Parameters
        ----------
        name_run : str
            The name of the run.
        n_samples : int
            The number of samples used for training.
        timestamp : bool, optional, default=True
            If True, append a timestamp to the filename.

        Returns
        -------
        str
            The checkpoint filename.
        """
        filename = f"{name_run}_{ut.timestamp_to_string()}" if timestamp else name_run
        filename += f"_NSamples_{n_samples}"

        return ut.check_filename(filename) + "_epoch_{epoch}_val_loss_{val/loss:.3E}"

    @staticmethod
    def _get_file_creation_date(file_path, time_fmt="%Y-%m-%d_%H-%M"):
        """Auxiliary function to check the creation date of a file."""
        # Get the file creation time in seconds since the epoch
        creation_time = os.path.getmtime(file_path)

        # Convert the creation time to a datetime object
        creation_date = datetime.fromtimestamp(creation_time)

        # Format the datetime object as a string in the desired format
        formatted_date = creation_date.strftime(time_fmt)

        return formatted_date
