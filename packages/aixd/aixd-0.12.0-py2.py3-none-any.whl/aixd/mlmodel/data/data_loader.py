import hashlib
import inspect
import warnings
from typing import Callable, List, Tuple, Union

import numpy as np
import pytorch_lightning as pl
import torch
from torch.utils.data import DataLoader
from torch.utils.data import Dataset as TorchDataset
from torch.utils.data import random_split

from aixd.data import Dataset, InputML, OutputML
from aixd.data.data_blocks import DataBlockTransformation
from aixd.mlmodel.constants import RANDOM_SEED_SPLIT
from aixd.mlmodel.utils_mlmodel import apply_numpy_func, to_numpy, to_torch


class XYZDataset(TorchDataset):
    """
    Torch dataset optimised for an encoder-decoder model. It is used to encapsulate x, y, and z data. I.e, x is the input data to the encoder, and y is the conditional
    data passed to the decoder. The optional z represents the latent representation, used for generating data with the decoder.
    """

    def __init__(self, x=None, y=None, z=None):
        if x is None and y is None:
            raise ValueError("Either x or y must be provided.")

        self.x = to_torch(x, dtype=torch.float32) if x is not None else None
        self.y = to_torch(y, dtype=torch.float32) if y is not None else None
        self.z = to_torch(z, dtype=torch.float32) if z is not None else None

    def __len__(self):
        return len(self.x) if self.x is not None else len(self.y)

    def __getitem__(self, idx):
        x = self.x[idx] if self.x is not None else torch.tensor([])
        y = self.y[idx] if self.y is not None else torch.tensor([])

        if self.z is not None:
            z = self.z[idx]
            return x, y, z
        else:
            return x, y

    def to_data_loader(self, batch_size: int = 64, **kwargs):
        """
        Returns a dataloader for the dataset.

        Parameters
        ----------
        batch_size : int, optional
            Batch size. The default is 64.
        **kwargs
            Additional keyword arguments to be passed to the dataloader.
        """
        return DataLoader(self, batch_size=batch_size, **kwargs)


class DataModule(pl.LightningDataModule):
    """
    Data module for the ML model. It takes care of splitting the data into train, val and test sets, normalizing the data.

    Parameters
    ----------
    input_ml_dblock : InputML
        Input data block, defining normalizations, the type of the input data, and the heads for the ML model.
    output_ml_dblock : OutputML
        Output data block, defining normalizations, the type of the output data, and the heads for the ML model.
    x : Union[np.ndarray, torch.Tensor]
        The input fata matrix.
    y : Union[np.ndarray, torch.Tensor]
        The output data matrix.
    batch_size : int, optional
        Batch size. The default is 512.
    split_ratios : List[Union[int, float]], optional
        List of ratios for splitting the data into train, val and test sets. The default is [0.8, 0.1, 0.1].
    random_seed : int, optional
        Random seed for splitting the data. The default is RANDOM_SEED_SPLIT.
    predict : bool, optional
        Whether to create a predict set. The default is False.

    """

    def __init__(
        self,
        input_ml_dblock: InputML,
        output_ml_dblock: OutputML,
        x: Union[np.ndarray, torch.Tensor] = None,
        y: Union[np.ndarray, torch.Tensor] = None,
        batch_size: int = 512,
        split_ratios: List[Union[int, float]] = None,
        random_seed: int = RANDOM_SEED_SPLIT,
        predict: bool = False,
    ):
        super().__init__()

        self.input_ml_dblock = input_ml_dblock
        self.output_ml_dblock = output_ml_dblock

        self.batch_size = batch_size
        self.split_ratios = split_ratios or [0.8, 0.1, 0.1]
        self.random_seed = random_seed

        if x is not None and y is not None:
            self._setup_data(x, y, predict)

    def _setup_data(self, x: Union[np.ndarray, torch.Tensor], y: Union[np.ndarray, torch.Tensor], predict: bool = False):
        """
        Splits the data into train, val and test sets. If predict is True, then only the predict set is created.
        Applies normalizations according to the input and output data blocks.
        """
        x, y = self._check_data_types(x), self._check_data_types(y)

        if predict and not (self.input_ml_dblock.transformation_is_fitted() and self.output_ml_dblock.transformation_is_fitted()):
            raise ValueError("The transformations of the input and output data blocks must be fitted when predict=True.")

        x = self.transform_x(x)
        y = self.transform_y(y)

        # Check that the input and output data have the correct number of columns
        self._check_input_output_ml_sizes(x, y)

        # Convert to np.float32
        x, y = x.astype(np.float32), y.astype(np.float32)

        if not predict:
            train_data, val_data, test_data = random_split(
                XYZDataset(x, y),
                self.split_ratios,
                generator=torch.Generator().manual_seed(self.random_seed),
            )

            # random split returns a Subset object, we need to convert it to XYZDataset object
            self._train_data = XYZDataset(*train_data[: len(train_data)])
            self._val_data = XYZDataset(*val_data[: len(val_data)])
            self._test_data = XYZDataset(*test_data[: len(test_data)])

        else:
            self._predict_data = XYZDataset(x, y)

    @staticmethod
    def _check_data_types(data: Union[np.ndarray, torch.Tensor]) -> np.ndarray:
        """Checks the type of the data."""
        if isinstance(data, (np.ndarray, np.generic)):
            return data
        elif isinstance(data, torch.Tensor):
            return data.float().cpu().detach().numpy()
        else:
            raise TypeError("Data must be of type torch.Tensor or np.ndarray")

    def _check_input_output_ml_sizes(self, x: np.ndarray, y: np.ndarray):
        """Checks that the input and output data have the correct number of columns."""
        expected_size_x = sum([dobj.dim for dobj in self.input_ml_dblock.dobj_list_transf])
        expected_size_y = sum([dobj.dim for dobj in self.output_ml_dblock.dobj_list_transf])

        size_x = x.shape[1]
        size_y = y.shape[1]

        if size_x != expected_size_x:
            raise ValueError(f"Input data has {size_x} columns, but {expected_size_x} were expected. ")
        if size_y != expected_size_y:
            raise ValueError(f"Output data has {size_y} columns, but {expected_size_y} were expected. ")

    @property
    def x(self) -> np.ndarray:
        """Returns the transformed input data, as expected by the ML model."""
        return np.concatenate([self.x_train, self.x_val, self.x_test], axis=0)

    @property
    def y(self) -> np.ndarray:
        """Returns the transformed output data, as expected by the ML model."""
        return np.concatenate([self.y_train, self.y_val, self.y_test], axis=0)

    @property
    def y_train(self) -> np.ndarray:
        """Returns the transformed and normalized training output data."""
        if not hasattr(self, "_train_data"):
            raise AttributeError("Training data is not available. You must set predict=False when creating the data module.")
        return to_numpy(self._train_data.y)

    @property
    def x_train(self) -> np.ndarray:
        """Returns the transformed and normalized training input data."""
        if not hasattr(self, "_train_data"):
            raise AttributeError("Training data is not available. You must set predict=False when creating the data module.")
        return to_numpy(self._train_data.x)

    @property
    def y_val(self) -> np.ndarray:
        """Returns the transformed and normalized validation output data."""
        if not hasattr(self, "_val_data"):
            raise AttributeError("Validation data is not available. You must set predict=False when creating the data module.")

        return to_numpy(self._val_data.y)

    @property
    def x_val(self) -> np.ndarray:
        """Returns the transformed and normalized validation input data."""
        if not hasattr(self, "_val_data"):
            raise AttributeError("Validation data is not available. You must set predict=False when creating the data module.")

        return to_numpy(self._val_data.x)

    @property
    def y_test(self) -> np.ndarray:
        """Returns the transformed and normalized test output data."""
        if not hasattr(self, "_test_data"):
            raise AttributeError("Test data is not available. You must set predict=False when creating the data module.")

        return to_numpy(self._test_data.y)

    @property
    def x_test(self) -> np.ndarray:
        """Returns the transformed and normalized test input data."""
        if not hasattr(self, "_test_data"):
            raise AttributeError("Test data is not available. You must set predict=False when creating the data module.")
        return to_numpy(self._test_data.x)

    def transform(
        self, x: Union[np.ndarray, torch.Tensor], y: Union[np.ndarray, torch.Tensor], out_type: str = "numpy"
    ) -> Tuple[Union[np.ndarray, torch.Tensor], Union[np.ndarray, torch.Tensor]]:
        """
        Transform the input and output data. Takes care of the case where x and y are numpy arrays or torch tensors.

        Parameters
        ----------
        x : Union[np.ndarray, torch.Tensor]
            Input data to be transformed, either a numpy array or a torch tensor.
        y : Union[np.ndarray, torch.Tensor]
            Output data to be transformed, either a numpy array or a torch tensor.
        out_type : str, optional
            The type of the output. Can be "numpy", "torch", or "same". The default is "numpy".

        Returns
        -------
        Tuple[Union[np.ndarray, torch.Tensor], Union[np.ndarray, torch.Tensor]]
            A tuple containing the transformed input and output data.

        """
        return self.transform_x(x, out_type=out_type), self.transform_y(y, out_type=out_type)

    def inverse_transform(
        self, x: Union[np.ndarray, torch.Tensor], y: Union[np.ndarray, torch.Tensor], out_type: str = "numpy"
    ) -> Tuple[Union[np.ndarray, torch.Tensor], Union[np.ndarray, torch.Tensor]]:
        """
        Unnormalize the input and output data. Takes care of the case where x and y are numpy arrays or torch tensors.

        Parameters
        ----------
        x : Union[np.ndarray, torch.Tensor]
            Input data to be un-transformed, either a numpy array or a torch tensor.
        y : Union[np.ndarray, torch.Tensor]
            Output data to be un-transformed, either a numpy array or a torch tensor.
        out_type : str, optional
            The type of the output. Can be "numpy", "torch", or "same". The default is "numpy".

        Returns
        -------
        Tuple[Union[np.ndarray, torch.Tensor], Union[np.ndarray, torch.Tensor]]
            A tuple containing the un-transformed input and output data.

        """
        return self.inverse_transform_x(x, out_type=out_type), self.inverse_transform_y(y, out_type=out_type)

    def transform_x(self, x: Union[torch.Tensor, np.ndarray], out_type: str = "numpy") -> Union[torch.Tensor, np.ndarray]:
        """
        Transform only the input data. Takes care of the case where x is a numpy array or a torch tensor.

        Parameters
        ----------
        x : Union[torch.Tensor, np.ndarray]
            A numpy array or a torch tensor to be transformed.
        out_type : str, optional
            The type of the output. Can be "numpy", "torch", or "same". The default is "numpy".

        Returns
        -------
        Union[torch.Tensor, np.ndarray]
            The transformed data.
        """
        func: Callable = lambda a: self.input_ml_dblock.transform(a)[0]
        return apply_numpy_func(x, func, out_type=out_type)

    def inverse_transform_x(self, x: Union[torch.Tensor, np.ndarray], out_type: str = "numpy") -> Union[torch.Tensor, np.ndarray]:
        """
        Unnormalize only the input data. Takes care of the case where x is a numpy array or a torch tensor.

        Parameters
        ----------
        x : Union[torch.Tensor, np.ndarray]
            A numpy array or a torch tensor to be unnormalized.
        out_type : str, optional
            The type of the output. Can be "numpy", "torch", or "same". The default is "numpy".

        Returns
        -------
        Union[torch.Tensor, np.ndarray]
            The unnormalized data.

        """
        func: Callable = lambda a: self.input_ml_dblock.inverse_transform(a)[0]
        return apply_numpy_func(x, func, out_type=out_type)

    def transform_y(self, y: Union[torch.Tensor, np.ndarray], out_type: str = "numpy") -> Union[torch.Tensor, np.ndarray]:
        """
        Transform only the output data. Takes care of the case where y is a numpy array or a torch tensor.

        Parameters
        ----------
        y : Union[torch.Tensor, np.ndarray]
            A numpy array or a torch tensor to be transformed.
        out_type : str, optional
            The type of the output. Can be "numpy", "torch", or "same". The default is "numpy".

        Returns
        -------
        Union[torch.Tensor, np.ndarray]
            The transformed data.

        """
        func: Callable = lambda a: self.output_ml_dblock.transform(a)[0]
        return apply_numpy_func(y, func, out_type=out_type)

    def inverse_transform_y(self, y: Union[torch.Tensor, np.ndarray], out_type: str = "numpy") -> Union[torch.Tensor, np.ndarray]:
        """
        Un-transform only the output data. Takes care of the case where y is a numpy array or a torch tensor.

        Parameters
        ----------
        y : Union[torch.Tensor, np.ndarray]
            A numpy array or a torch tensor to be un-transformed.
        out_type : str, optional
            The type of the output. Can be "numpy", "torch", or "same". The default is "numpy".

        Returns
        -------
        Union[torch.Tensor, np.ndarray]
            The un-transformed data.

        """
        func: Callable = lambda a: self.output_ml_dblock.inverse_transform(a)[0]
        return apply_numpy_func(y, func, out_type=out_type)

    def convert_to_dataloader(
        self,
        x: Union[np.ndarray, torch.Tensor, None] = None,
        y: Union[np.ndarray, torch.Tensor, None] = None,
        z: Union[np.ndarray, torch.Tensor, None] = None,
        requires_fitted: bool = True,
        **kwargs,
    ) -> DataLoader:
        """
        Converts input and output data to a dataloader.

        Parameters
        ----------
        x : Union[np.ndarray, torch.Tensor]
            The input data.
        y : Union[np.ndarray, torch.Tensor]
            The output data.
        z : Union[np.ndarray, torch.Tensor]
            The latent representation data. The default is None. This is used if one wants to generate data with the decoder.
        requires_fitted : bool
            Whether the transformations must be fitted. The default is True.
        **kwargs
            Additional keyword arguments to be passed to the dataloader.

        Returns
        -------
        DataLoader
            The dataloader containing the input and output data.

        """
        if requires_fitted and not (self.input_ml_dblock.transformation_is_fitted() and self.output_ml_dblock.transformation_is_fitted()):
            raise ValueError("The transformations must be fitted before converting to a dataloader.")

        x = self.transform_x(x) if x is not None else None
        y = self.transform_y(y) if y is not None else None

        data = XYZDataset(x, y, z)
        batch_size = kwargs.pop("batch_size", 64)
        return data.to_data_loader(batch_size=self._adjust_batch_size(data, batch_size=batch_size), **kwargs)

    def _adjust_batch_size(self, data: XYZDataset, mode: str = None, batch_size: int = None):
        batch_size = batch_size or self.batch_size
        if len(data) < batch_size:
            batch_size = len(data)
            warnings.warn(f"Batch size was adjusted from {self.batch_size} to {batch_size} for{' ' + mode + ' ' if mode is not None else ' '}dataloader.")
        return batch_size

    def train_dataloader(self):
        return DataLoader(
            self._train_data,
            batch_size=self._adjust_batch_size(self._train_data, "training"),
            shuffle=True,
            drop_last=True,
            pin_memory=True,
        )

    def val_dataloader(self):
        return DataLoader(
            self._val_data,
            batch_size=self._adjust_batch_size(self._val_data, "validation"),
            shuffle=False,
            drop_last=False,
            pin_memory=True,
        )

    def test_dataloader(self):
        return DataLoader(
            self._test_data,
            batch_size=self._adjust_batch_size(self._test_data, "testing"),
            shuffle=False,
            drop_last=True,
            pin_memory=True,
        )

    def predict_dataloader(self):
        return DataLoader(
            self._predict_data,
            batch_size=self._adjust_batch_size(self._predict_data, "prediction"),
            shuffle=False,
            drop_last=False,
        )

    def get_parameters(self):
        """Get parameters defining the data module."""
        params = {name: getattr(self, name) for name in inspect.signature(self.__class__.__init__).parameters.keys() if name not in ["x", "y", "self", "predict"]}
        return params

    def get_checksum(self):
        """Computes a checksum for the training/validation/test data."""
        md5 = hashlib.md5()
        for row in np.concatenate([self.x, self.y], axis=1):
            md5.update(row.tobytes())
        return md5.hexdigest()

    def summary_input_output_dimensions(self, print_summary: bool = True) -> Tuple[int, int, str]:
        """
        Calculates the dimensions of the input and output of the ML model.


        Parameters:
        -----------
        print_summary : bool
            Whether to print the summary text.

        Returns:
        --------
        input_ml_total : int
            Total number of dimensions of the input of the ML model.
        output_ml_total : int
            Total number of dimensions of the output of the ML model.
        summary : str
            Summary text.
        """

        dims_input_ml = {dobj.name: dobj.dim for dobj in self.input_ml_dblock.dobj_list_transf}
        dims_output_ml = {dobj.name: dobj.dim for dobj in self.output_ml_dblock.dobj_list_transf}

        input_ml_total = sum(dims_input_ml.values())
        output_ml_total = sum(dims_output_ml.values())

        summary = f"Dimension of the input to the model ({self.input_ml_dblock.display_name}): {input_ml_total} \n"
        for k, v in dims_input_ml.items():
            summary += f"   {k}: {v} \n"

        summary += f"Dimension of the output of the model ({self.output_ml_dblock.display_name}): {output_ml_total} \n"
        for k, v in dims_output_ml.items():
            summary += f"   {k}: {v} \n"

        if print_summary:
            print(summary)
        return input_ml_total, output_ml_total, summary

    @classmethod
    def from_parameters(cls, x: Union[np.ndarray, torch.Tensor, None] = None, y: Union[np.ndarray, torch.Tensor, None] = None, **datamodule_kwargs):
        """
        Creates a data module from parameters returned by the `get_parameters(...)` method.

        Parameters
        ----------
        x : Union[np.ndarray, torch.Tensor, None]
            The input data.
        y : Union[np.ndarray, torch.Tensor, None]
            The output data.
        **datamodule_kwargs
            Additional keyword arguments to be passed to the data module.

        Returns
        -------
        DataModule
            The data module created from the parameters.

        """
        return cls(x=x, y=y, **datamodule_kwargs)

    @classmethod
    def from_dataset(
        cls,
        dataset: Dataset,
        input_ml_names: List[str] = None,
        output_ml_names: List[str] = None,
        input_ml_transformation: DataBlockTransformation = None,
        output_ml_transformation: DataBlockTransformation = None,
        **kwargs,
    ):
        """
        Creates a data module from a dataset.

        Parameters
        ----------
        dataset : Dataset
            The dataset to be used to create the data module.
        input_ml_names : List[str], optional
            List of names of the input data to be used for the ML model. The default is None. If None, then all the design parameters are used.
        output_ml_names : List[str], optional
            List of names of the output data to be used for the ML model. The default is None. If None, then all the performance attributes are used.
        input_ml_transformation : DataBlockTransformation, optional
            Custom transformation to be used for the input data. The default is None.
        output_ml_transformation: DataBlockTransformation, optional
            Custom transformation to be used for the output data. The default is None.
        **kwargs
            Additional keyword arguments to be passed to the data module.

        Returns
        -------
        DataModule
            The data module created from the dataset.

        """
        # Set default input and output names
        input_ml_names = input_ml_names or dataset.design_par.names_list
        output_ml_names = output_ml_names or dataset.perf_attributes.names_list

        x, dobj_list_input = dataset.data_mat_with_dobjs(dobj_names=input_ml_names, flag_transf=False)
        y, dobj_list_output = dataset.data_mat_with_dobjs(dobj_names=output_ml_names, flag_transf=False)

        input_ml_dblock = InputML(dobj_list=dobj_list_input, transformation=input_ml_transformation)
        output_ml_dblock = OutputML(dobj_list=dobj_list_output, transformation=output_ml_transformation)

        return cls(input_ml_dblock, output_ml_dblock, x, y, **kwargs)
