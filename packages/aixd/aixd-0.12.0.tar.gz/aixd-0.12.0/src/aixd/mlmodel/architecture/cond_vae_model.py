from typing import Callable, Dict, List, Tuple

import torch

from aixd.data import InputML, OutputML
from aixd.mlmodel.architecture.cond_ae_model import CondAEModel
from aixd.mlmodel.architecture.encoders import VEncoder
from aixd.mlmodel.constants import SEP_LOSSES


class CondVAEModel(CondAEModel):
    """
    Class representing a Conditional Variational Autoencoder model.

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
        the values are a sequence of integers specifying the number of units in each hidden layer of the head.
    custom_losses : Dict[str, Callable[[torch.Tensor, torch.Tensor], torch.Tensor]], optional, default=None
        Dictionary containing custom losses to be computed on the outputs.
    loss_weights : Dict[str, float], optional, default=None
        Dictionary containing the weights with which each loss term should be multiplied before being added to the total loss used for backpropagation, including custom losses.
    activation : Union[torch.nn.Module, str], optional, default="leaky_relu"
        Activation function to be used in the latent layers of the autoencoder.
    optimizer : torch.optim.Optimizer, optional, default=None
        Optimizer to be used for updating the model's weights.
    name : str, optional, default="CondVAEModel"
        Name of the model.
    save_dir : str, optional, default=None
        Directory where the model related files will be saved, such as the models's checkpoint and logs.
    name_proj : str, optional, default=None
        Name of the project.
    **kwargs : dict
        Additional arguments passed to :class:`pytorch_lightning.core.module.LightningModule`.
    """

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
        name: str = "CondVAEModel",
        save_dir: str = None,
        name_proj: str = None,
        **kwargs,
    ):
        super().__init__(
            input_ml_dblock,
            output_ml_dblock,
            layer_widths,
            latent_dim,
            heads_layer_widths,
            custom_losses,
            loss_weights,
            activation,
            optimizer,
            name,
            save_dir,
            name_proj,
            **kwargs,
        )

        self.encoder = VEncoder(
            {x_key: x_heads[0] for x_key, x_heads in self.x_heads.items()},
            {y_key: y_heads[1] for y_key, y_heads in self.y_heads.items()},
            self.x_head_splits_in,
            layer_widths,
            latent_dim,
            activation,
        )

    def _step(self, batch: Tuple[torch.Tensor, torch.Tensor], batch_idx: int, mode: str, postprocess=False) -> Tuple[Dict[str, torch.Tensor], Dict[str, float]]:
        """
        Process a single batch of data. Extends the parent's `_step` function by adding a kl_loss.

        Parameters
        ----------
        batch : Tuple[torch.Tensor, torch.Tensor]
            A tuple of tensors containing the data for a single batch.
        batch_idx : int
            The index of the current batch.
        mode : str
            The mode in which the model is being run (either 'train' or 'val').

        Returns
        -------
        Tuple[Dict[str, torch.Tensor], Dict[str, float]]
            A tuple where the first element is a dictionary with predictions, and the second element a dictionary with losses for the batch.
        """
        pred, losses = super()._step(batch, batch_idx, mode, step_ae=False, postprocess=postprocess)

        z_mean, z_log_var = pred["z_mean"], pred["z_log_var"]
        kl_loss = ((-0.5 * (1 + z_log_var - z_mean**2 - torch.exp(z_log_var))).sum(dim=1)).mean()

        if mode in ["train", "training"]:
            losses["train" + SEP_LOSSES + "loss"] += self.loss_weights.get("kl", 1.0) * kl_loss

        losses[mode + SEP_LOSSES + "kl_loss"] = kl_loss
        return pred, losses
