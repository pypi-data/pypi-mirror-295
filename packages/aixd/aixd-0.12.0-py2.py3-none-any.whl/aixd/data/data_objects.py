from __future__ import annotations

import inspect
import warnings
from typing import List, Optional, Tuple, TypeVar, Union

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import torch
from torch import nn

import aixd.data.domain as dd
import aixd.data.utils_data as ud
import aixd.visualisation.utils_plots as up
from aixd.data.transform import DataObjectTransform, LabelEncoder, MaskedZeroToOne, MinMaxScaler, ZeroToOne, resolve_transformation
from aixd.mlmodel.architecture.heads import CategoricalInHead, CategoricalOutHead, InHead, InHeadConv2D, InHeadFC, OutHead, OutHeadConv2D, OutHeadFC
from aixd.mlmodel.architecture.losses import CrossEntropyLoss
from aixd.utils import logs

logger = logs.get_logger().get_child("data-objects")


class DataObject:
    """
    Master data object, to define each of the different building blocks
    that are going to be used to form the design parameters and performance
    attributes vectors.

    Parameters
    ----------
    name : str
        Name of the data object.
    dim : int
        Dimensionality of the data object, or different columns to perform the split on.
    domain : Domain, optional
        Domain of the data object.
    unit : str, optional, default=None
        Unit of the data object (e.g. m, kg. m^2, m/s^2 etc.). Use ^ to indicate powers (e.g. m^2), and _ to indicate subscripts (e.g. m_1).
    position : int, optional, default=None
        Position of the data object in the vector.
    position_index : int, optional, default=None
        Index of the data object in the vector.
    transformations : Union[List[str], List[DataObjectTransform]], optional, default=None
        List of transformations to be applied to the data object.
    type : str, optional, default="any"
        Name of the type of data object. Either real, categorical, integer, ordinal or any.
    dtype : str, optional, default=None
        The dtype of the numpy array that is expected.
    flag_split_perdim : bool, optional, default=False
        If True, object is split across dimensions in a DataBlock.

    """

    def __init__(
        self,
        name: str,
        dim: int,
        domain: dd.Domain,
        unit: str = None,
        position: Optional[int] = None,
        position_index: Optional[int] = None,
        transformations: Union[List[str], List[DataObjectTransform]] = None,
        type: str = "any",
        dtype: str = None,
        flag_split_perdim: bool = False,
    ):
        self.name = name  # Descriptor to understand the DataObject
        self.dim = dim  # Dimensionality of the data
        self.domain = domain  # The domain of data, either an interval or options
        self.unit = unit  # The unit of the data

        self.position = position  # Initially not specified as is defined with DataBlock
        # Relative position, incrementally from 0
        self.position_index = position_index  # Initially not specified as is defined with DataBlock

        self.transformations = transformations

        self.type = type  # The type of the data block, either real, categorical, integer, ordinal or any
        self.dtype = dtype  # The dtype of the numpy array that is expected

        self.flag_split_perdim = flag_split_perdim

    def __jsondump__(self):
        return {
            "name": self.name,
            "dim": self.dim,
            "domain": self.domain,
            "unit": self.unit,
            "position": self.position,
            "position_index": self.position_index,
            "transformations": self.transformations,
            "dtype": self.dtype,
            "flag_split_perdim": self.flag_split_perdim,
        }

    @classmethod
    def __jsonload__(cls, data):
        return cls(**data)

    @property
    def name(self) -> str:
        """Getter method for the name of the DataObject."""
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of the DataObject and handles the transformation to replace spaces by underscores."""
        self._name_org = name  # store original name
        self._name = name.replace(" ", "_")

    @property
    def columns_df(self) -> List[str]:
        """Getter method for the names of columns of the DataObject, if it has more than one dimension. Otherwise, returns the name of the DataObject."""
        if self.dim > 1:
            return [f"{self.name}_{i}" for i in range(self.dim)]
        else:
            return [self.name]

    @property
    def name_org(self) -> str:
        """Getter method for the original name of the DataObject."""
        return self._name_org

    def has_name(self, name: str) -> bool:
        """Returns if the passed name match with the name of the DataObject."""
        return self.name == name or self.name_org

    @property
    def transformations(self) -> List[DataObjectTransform]:
        """Getter for the transformations."""
        return self._transformations

    @transformations.setter
    def transformations(self, ts: Union[List[str], List[DataObjectTransform]]):
        """Setter for the transformations that calls resolver if a strings are passed."""
        self._transformations = [(resolve_transformation(t) if isinstance(t, str) else t) for t in ts] if ts is not None else []

    def append_transformation(self, t: Union[str, DataObjectTransform]):
        """Adds the transformation at the end."""
        self._transformations.append(resolve_transformation(t) if isinstance(t, str) else t)

    def prepend_transformation(self, t: Union[str, DataObjectTransform]):
        """Adds the transformation at the start."""
        self._transformations = [resolve_transformation(t) if isinstance(t, str) else t] + self.transformations

    def __repr__(self) -> str:
        """Returns a representation of the DataObject."""
        if self.position is not None and self.position_index is not None:
            return f'{self.__class__.__name__}(name="{self.name}", dim={self.dim}, domain={repr(self.domain)}, position={self.position}, position_index={self.position_index})'
        else:
            return f'{self.__class__.__name__}(name="{self.name}", dim={self.dim}, domain={repr(self.domain)})'

    def random_samples(self, n_samples: int) -> np.ndarray:
        """
        Returns random samples from the domain of the data object.

        Parameters
        ----------
        n_samples : int
            Number of samples to return.

        Returns
        -------
        np.ndarray
            Random samples (number, dim) from the domain of the data object.
        """
        return self.domain.random_samples((n_samples, self.dim))

    def grid_samples(self, n_samples: int) -> np.ndarray:
        """
        Returns grid samples from the domain of the data object.

        Parameters
        ----------
        n_samples : int
            Number of samples to return.

        Returns
        -------
        np.ndarray
            Grid samples (number, dim) from the domain of the data object.
        """
        return self.domain.grid_samples((n_samples, self.dim))

    def sample_around(self, centroid: np.ndarray, n_samples: int, percentage: int, **kwargs) -> np.ndarray:
        """
        Returns samples from the domain of the data object around the given centroid.

        Parameters
        ----------
        centroid : np.ndarray
            Centroid around which to sample.
        n_samples : int
            Number of samples to return.
        percentage : int
            Controls the range of the samples. If 100, the samples are drawn from the whole domain. If 50, the samples are drawn from the half of the domain around the centroid.
        """
        return self.domain.sample_around(centroid, n_samples, percentage, **kwargs)

    def transform_is_fitted(self) -> bool:
        """Check if all transformations are fitted."""
        return all(t.is_fitted() for t in self.transformations)

    def transform(self, data_mat: np.ndarray, refit: bool = False):
        """
        Transforms the data matrix according to specification DataObject.transformations. Be aware that transformations can change the dimensionality of the data.

        Parameters
        ----------
        data_mat : np.ndarray
            Data matrix to transform.
        refit : bool, optional, default=False
            If True, the transformations are refitted.

        Returns
        -------
        np.ndarray
            Transformed data matrix.
        """
        for t in self.transformations:
            if t.is_fitted() and not refit:
                data_mat = t.transform(data_mat, self)
            else:
                data_mat = t.fit_transform(data_mat, self)

        return data_mat

    def inverse_transform(self, data_mat: np.ndarray) -> np.ndarray:
        """
        Inverse transformation of the data matrix according to specification DataObject.transformations. Be aware that transformations can change the dimensionality of the data.

        Parameters
        ----------
        data_mat : np.ndarray
            Data matrix to transform.

        Returns
        -------
        np.ndarray
            Inverse transformed data matrix.
        """
        for t in self.transformations[::-1]:
            data_mat = t.inverse_transform(data_mat, self)

        return data_mat

    def print_transf_norm(self):
        """
        Prints an overview of the defined transformations.
        """
        if len(self.transformations) > 0:
            str_transf = "transformed with " + " - > ".join([t.name for t in self.transformations]) + ","
        else:
            str_transf = "is not transformed,"

        print("* Attribute {} {}".format(self.name, str_transf))

    def check_data_consistency(self, data_mat: np.ndarray, **kwargs):
        """Check if the data is consistent with the defined domain."""
        msg = self.domain.check_domain_consistency(data_mat, **kwargs)
        logger.info(f"* Checking data consistency for {self.name}: {msg if msg is not None else 'OK'}")

    def update_obj(self, data_mat: np.ndarray, **kwargs):
        """Updates the domain of the data object with the passed data."""
        msg = self.domain.update_domain(data_mat, **kwargs)
        logger.info(f"* Updating domain for {self.name}: {msg if msg is not None else 'OK (no update)'}")

    def update_dobj_types(self, data, flag_update=True):
        # TODO: maisseal, revise
        curr_types = [self.type, self.dtype]
        # Perhaps this is too simplistic, but we just take the first
        # element to assess the type. We assume all are similar
        new_types = ud.data_types(data)
        if new_types[1] != curr_types[1]:
            if flag_update:
                logger.info("Updating data types")
                # self.type = new_types[2]
                self.dtype = new_types[2]
                return 1
            else:
                return "class type {} , dtypes: class {}/data {}".format(self.type, self.dtype, new_types[2])

    def get_activation_outhead(self) -> Optional[Union[str, nn.Module]]:
        """
        Returns the activation function for approximating this feature.
        """
        raise NotImplementedError()

    def get_objective(self, **kwargs) -> nn.Module:
        """
        Returns the loss function for approximating this feature.
        """
        raise NotImplementedError()

    def get_loss_evaluation(self, **kwargs) -> nn.Module:
        """
        Returns the evaluation loss function for this feature.
        """
        # TODO: maisseal, document this better, since these should be a per-sample loss that works for the transformed and untransformed data
        raise NotImplementedError()

    def get_ml_heads(self, head_layer_widths: List[int], last_core_layer_width: int, activation: nn.Module, **kwargs) -> Tuple[InHead, OutHead]:
        """
        Returns two ML heads necessary for encoding and decoding the given data object.

        Parameters
        ----------
        head_layer_widths : List[int]
            List of integers where the length denotes number of layers and values the width of the layers in the head.
        last_core_layer_width : int
            Dimensionality of autoencoder output to be decoded by this feature head.
        activation : nn.Module
            Activation function to be used in this head.
        kwargs
            Additional keyword arguments passed to the head constructors.

        Returns
        -------
        Tuple[nn.Module, nn.Module]
            Tuple containing the input and output head.
        """
        raise NotImplementedError()

    def plot_distrib(
        self,
        fig: go.Figure,
        data: Union[np.ndarray, pd.DataFrame],
        cols: Union[str, List[str]] = None,
        name_plot: str = "",
        pos: Tuple[int, int] = (1, 1),
        downsamp: float = 2,
        **kwargs,
    ) -> go.Figure:
        """
        Plots the distribution of the passed data.

        Parameters
        ----------
        fig : go.Figure
            Plotly figure to plot on.
        data : Union[np.ndarray, pd.DataFrame]
            Data to plot. If a DataFrame is passed, the columns specified by `cols` are plotted.
        cols : List[str], optional, default=None
            Columns of the DataFrame to plot. Only used if `data` is a DataFrame.
        name_plot : str, optional, default=""
            Name of the plot.
        pos : Tuple[int, int], optional, default=(1, 1)
            Position of the plot in the figure.
        downsamp : float, optional, default=2
            Downsampling factor of the data.
        kwargs
            Additional keyword arguments passed to `plotly.graph_objects.Histogram`.

        Returns
        -------
        go.Figure
            Plotly figure with the histogram.

        """
        raise NotImplementedError()

    def copy(self, reset: bool = False, **kwargs) -> DataObject:
        """
        Returns a copy of the data object. If reset is True, the state of transformations are reset.
        Additional keyword arguments can be passed to overwrite attributes of the copy, or to pass additional attributes not in the signature of the DataObject constructor,
        but in the signature of the constructor of the specific DataObject subclass.

        Parameters
        ----------
        reset : bool
            If True, the state of transformations, i.e, fitted values are reset.
        kwargs
            Can be used to overwrite attributes passed to the constructor, and hence allows partial copying of the object.

        Returns
        -------
        DataObject
            Copy of the data object.
        """
        init_signature = inspect.signature(DataObject.__init__)
        init_params = {param.name: getattr(self, param.name) for param in init_signature.parameters.values() if param.name not in ["self", "type"]}

        init_params["domain"] = init_params["domain"].copy()
        init_params["transformations"] = [t.copy(reset=reset) for t in init_params["transformations"]]

        init_params.update(kwargs)  # Update the parameters with the passed kwargs
        return type(self)(**init_params)


class DataReal(DataObject):
    """
    Real data type.

    Parameters
    ----------
    name : str
        Name of the data object.
    dim : int, optional, default=1
        Dimensionality of the data object, or different columns to perform the split on.
    domain : Interval, optional, default=None
        Domain of the data object.
    unit : str, optional, default=None
        Unit of the data object (e.g. m, kg. m^2, m/s^2 etc.). Use ^ to indicate powers (e.g. m^2), and _ to indicate subscripts (e.g. m_1).
    position : int, optional, default=None
        Position of the data object in the vector.
    position_index : int, optional, default=None
        Index of the data object in the vector.
    transformations: Union[List[str], List[DataObjectTransform]], optional, default=None
        List of transformations to be applied to the data object.
    dtype: str, optional, default="float64"
        The dtype of the numpy are of the expected data matrix.
    flag_split_perdim : bool, optional, default=False
        If True, object is split across dimensions in a DataBlock.
    """

    def __init__(
        self,
        name: str,
        dim: int = 1,
        domain: Optional[dd.Interval] = None,
        unit: str = None,
        position: int = None,
        position_index: int = None,
        transformations: Union[List[str], List[DataObjectTransform]] = None,
        dtype: str = "float64",
        flag_split_perdim: bool = False,
    ):
        type = "real"
        if domain is not None:
            domain = dd.check_domain_interval(domain, expected_type=type)
        else:
            warnings.warn("Expected to get an object of class <Interval> as a domain. One created automatically with range 0 to 100")
            domain = dd.Interval(0, 1)

        if transformations is None:
            transformations = [MaskedZeroToOne(per_column=True)] if isinstance(domain, dd.IntervalMasked) else [ZeroToOne(per_column=True)]

        super().__init__(name, dim, domain, unit, position, position_index, transformations, type, dtype, flag_split_perdim)

    @classmethod
    def from_range(
        cls,
        name: str,
        vmin: Union[int, float],
        vmax: Union[int, float],
        dim: int = 1,
        unit: str = None,
        transformations: Union[List[str], List[DataObjectTransform]] = None,
        dtype: str = "float64",
        flag_split_perdim: bool = False,
    ) -> DataReal:
        """
        Class method to initialization a DataReal from a range defined by vmin and vmax.

        Parameters
        ----------

        name : str
            Name of the data object.
        vmin : Union[int, float]
            Lower bound of the interval domain.
        vmax : Union[int, float]
            Upper bound of the interval domain.
        dim : int, optional, default=1
            Dimensionality of the data object, or different columns to perform the split on.
        unit : str, optional, default=None
            Unit of the data object (e.g. m, kg. m^2, m/s^2 etc.). Use ^ to indicate powers (e.g. m^2), and _ to indicate subscripts (e.g. m_1).
        transformations: Union[List[str], List[DataObjectTransform]], optional, default=None
            List of transformations to be applied to the data object.
        dtype: str, optional, default="float64"
            The dtype of the numpy are of the expected data matrix.
        flag_split_perdim : bool, optional, default=False
            If True, object is split across dimensions in a DataBlock.

        Returns
        -------
        DataReal
            A DataReal object.
        """
        domain = dd.Interval(vmin, vmax)
        return cls(
            name=name,
            dim=dim,
            domain=domain,
            unit=unit,
            transformations=transformations,
            dtype=dtype,
            flag_split_perdim=flag_split_perdim,
        )

    def get_objective(self, **kwargs):
        """
        Returns the loss function for approximating this feature.
        """
        return nn.MSELoss(**kwargs)

    def get_loss_evaluation(self, **kwargs) -> nn.Module:
        """
        Returns the evaluation loss function for this feature.
        """
        return nn.L1Loss(reduction="none")

    def get_activation_outhead(self) -> Optional[Union[str, nn.Module]]:
        """
        Tries to interfere the activation function for the output head, based on the last transformation. It follows the following rules:

        - If the last transformation is a MinMaxScaler with a target range of (0, 1), the activation function is sigmoid.
        - If the last transformation is a MinMaxScaler with a target range of (-1, 1), the activation function is tanh.
        - Otherwise, no activation function is inferred. None is returned.

        Returns
        -------
        Optional[Union[str, nn.Module]]
            Activation function for the output head.
        """
        last_transf = self.transformations[-1] if len(self.transformations) > 0 else None
        if isinstance(last_transf, MinMaxScaler) and last_transf.target_range == (0, 1):
            return "sigmoid"
        elif isinstance(last_transf, MinMaxScaler) and last_transf.target_range == (-1, 1):
            return "tanh"
        else:
            # Activation function can not be inferred, choosing no activation function for the output head
            return None

    def get_ml_heads(self, head_layer_widths: List[int], last_core_layer_width: int, activation: nn.Module, **kwargs) -> Tuple[nn.Module, nn.Module]:
        """
        Returns a fully-connected head for encoding and decoding this feature.

        Parameters
        ----------
        head_layer_widths : List[int]
            List of integers where the length denotes number of layers and values the width of the layers in the head.
        last_core_layer_width : int
            Dimensionality of autoencoder output to be decoded by this feature head.
        activation : nn.Module
            Activation function to be used in this head.

        Returns
        -------
        Tuple[nn.Module, nn.Module]
            Tuple containing the input and output head.
        """
        out_activation = self.get_activation_outhead()
        return InHeadFC(self.dim, head_layer_widths, activation), OutHeadFC(last_core_layer_width, head_layer_widths[::-1] + [self.dim], activation, out_activation, **kwargs)

    def plot_distrib(
        self,
        fig: go.Figure,
        data: Union[np.ndarray, pd.DataFrame],
        cols: Union[str, List[str]] = None,
        name_plot: str = "",
        pos: Tuple[int, int] = (1, 1),
        downsamp: float = 2,
        **kwargs,
    ) -> go.Figure:
        """
        Plots the distribution of the passed data as a Histogram. If the data is multidimensional, the data is flattened before plotting.

        Parameters
        ----------
        fig : go.Figure
            Plotly figure to plot on.
        data : Union[np.ndarray, pd.DataFrame]
            Data to plot. If a DataFrame is passed, the columns specified by `cols` are plotted.
        cols : List[str], optional, default=None
            Columns of the DataFrame to plot, by default None. Only used if `data` is a DataFrame.
        name_plot : str, optional, default=""
            Name of the plot.
        pos : Tuple[int, int], optional, default=(1, 1)
            Position of the plot in the figure.
        downsamp : float, optional, default=2
            Downsampling factor of the data.
        kwargs
            Additional keyword arguments passed to `plotly.graph_objects.Histogram`.

        Returns
        -------
        go.Figure
            Plotly figure with the histogram.

        """
        if isinstance(data, pd.DataFrame):
            data = data[cols] if cols is not None else data

        data_mat = np.asarray(data)[::downsamp]

        return up.hist1d(fig, data_mat.flatten(), name_plot, pos, **kwargs)


class DataDiscrete(DataObject):
    """
    Base class for the discrete type.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def plot_distrib(
        self,
        fig: go.Figure,
        data: Union[np.ndarray, pd.DataFrame],
        cols: Union[str, List[str]] = None,
        name_plot: str = "",
        pos: Tuple[int, int] = (1, 1),
        downsamp: float = 2,
        **kwargs,
    ) -> go.Figure:
        """
        Plots the distribution of the passed data as a Barplot. If the data is multidimensional, the data is flattened before plotting.

        Parameters
        ----------
        fig : go.Figure
            Plotly figure to plot on.
        data : Union[np.ndarray, pd.DataFrame]
            Data to plot. If a DataFrame is passed, the columns specified by `cols` are plotted.
        cols : List[str], optional, default=None
            Columns of the DataFrame to plot, by default None. Only used if `data` is a DataFrame.
        name_plot : str, optional, default=""
            Name of the plot.
        pos : Tuple[int, int], optional, default=(1, 1)
            Position of the plot in the figure.
        downsamp : float, optional, default=2
            Downsampling factor of the data.
        kwargs
            Additional keyword arguments passed to `plotly.graph_objects.Bar`.

        Returns
        -------
        go.Figure
            Plotly figure with the barplot.
        """
        if isinstance(data, pd.DataFrame):
            data = data[cols] if cols is not None else data

        data_mat = np.asarray(data)[::downsamp]

        if isinstance(self.domain, dd.Interval):
            return up.hist1d(fig, data_mat.flatten(), name_plot, pos, **kwargs)
        elif isinstance(self.domain, dd.Options):
            is_transformed = self.is_data_transformed(data_mat)
            options = self.transform(np.asarray(self.domain.array).reshape(-1, 1)).flatten() if is_transformed else self.domain.array
            return up.barplot(fig, data_mat.flatten(), name_plot, pos, options=options, **kwargs)
        else:
            raise ValueError("Expected domain to be of type Interval or Options")

    def is_data_transformed(self, data_mat: np.ndarray):
        """
        Simple heuristic to determine if the data is transformed. Only works for categorical and ordinal data, as the domain is of type Options.

        Parameters
        ----------
        data_mat : np.ndarray
            Data matrix to check if transformed.

        Returns
        -------
        bool
            True if the data is transformed, False otherwise.
        """

        # Indentify if the data is transformed, or in original form, not nice but works!
        if self.type in ["categorical", "ordinal"]:
            assert isinstance(self.domain, dd.Options)
            try:
                return self.domain.check_domain_consistency(data_mat, strict=False) is not None
            except:  # noqa
                return True
        else:
            raise ValueError("Can not determine if data is transformed for this type of data object! Only categorical and ordinal are supported.")


class DataInt(DataDiscrete):
    """
    Integer data type.

    Parameters
    ----------
    name : str
        Name of the data object.
    dim : int, optional, default=1
        Dimensionality of the data object, or different columns to perform the split on.
    domain : Interval, optional, default=None
        Domain of the data object.
    unit : str, optional, default=None
        Unit of the data object (e.g. m, kg. m^2, m/s^2 etc.). Use ^ to indicate powers (e.g. m^2), and _ to indicate subscripts (e.g. m_1).
    position : int, optional, default=None
        Position of the data object in the vector.
    position_index : int, optional, default=None
        Index of the data object in the vector.
    transformations: Union[List[str], List[DataObjectTransform]], optional, default=None
        List of transformations to be applied to the data object.
    dtype: str, optional, default="int64"
        The dtype of the numpy are of the expected data matrix.
    flag_split_perdim : bool, optional, default=False
        If True, object is split across dimensions in a DataBlock.
    """

    def __init__(
        self,
        name: str,
        dim: int = 1,
        domain: dd.Interval = None,
        unit: str = None,
        position: int = None,
        position_index: int = None,
        transformations: Union[List[str], List[DataObjectTransform]] = None,
        dtype: str = "int64",
        flag_split_perdim: bool = False,
    ):
        type = "integer"
        if isinstance(domain, dd.Interval):
            domain = dd.check_domain_interval(domain, expected_type=type)
        else:
            warnings.warn("Expected to get an object of class <Interval> as a domain. One created automatically with entries 0 to 9")
            domain = dd.Interval(0, 10, type="integer")

        transformations = transformations if transformations is not None else [ZeroToOne(per_column=True)]
        if "to_float" not in [(t.name if isinstance(t, DataObjectTransform) else t) for t in transformations]:
            transformations = ["to_float"] + transformations
        super().__init__(name, dim, domain, unit, position, position_index, transformations, type, dtype, flag_split_perdim)

    @classmethod
    def from_range(
        cls,
        name: str,
        vmin: int,
        vmax: int,
        dim: int = 1,
        unit: str = None,
        transformations: Union[List[str], List[DataObjectTransform]] = None,
        dtype: str = "int64",
        flag_split_perdim: bool = False,
    ) -> DataInt:
        """
        Class method to initialization a DataInt from a list of integers.

        Parameters
        ----------
        name : str
            Name of the data object.
        vmin : int
            Lower bound of the interval domain.
        vmax : int
            Upper bound of the interval domain.
        dim : int, optional, default=1
            Dimensionality of the data object, or different columns to perform the split on.
        unit : str, optional, default=None
            Unit of the data object (e.g. m, kg. m^2, m/s^2 etc.). Use ^ to indicate powers (e.g. m^2), and _ to indicate subscripts (e.g. m_1).
        transformations: Union[List[str], List[DataObjectTransform]], optional, default=None
            List of transformations to be applied to the data object.
        dtype: str, optional, default="int64"
            The dtype of the numpy are of the expected data matrix.
        flag_split_perdim : bool, optional, default=False
            If True, object is split across dimensions in a DataBlock.

        Returns
        -------
        DataInt
            A DataInt object.
        """
        domain = dd.Interval(vmin, vmax, type="integer")
        return cls(
            name=name,
            dim=dim,
            domain=domain,
            unit=unit,
            transformations=transformations,
            dtype=dtype,
            flag_split_perdim=flag_split_perdim,
        )

    def get_objective(self, **kwargs) -> nn.Module:
        """
        Returns the loss function for approximating this feature.
        """
        return nn.MSELoss(**kwargs)

    def get_loss_evaluation(self, **kwargs) -> nn.Module:
        """
        Returns the loss function for approximating this feature.
        """
        return nn.L1Loss(reduction="none")

    def get_activation_outhead(self) -> Optional[Union[str, nn.Module]]:
        """
        Tries to interfere the activation function for the output head, based on the last transformation. It follows the following rules:

        - If the last transformation is a MinMaxScaler with a target range of (0, 1), the activation function is sigmoid.
        - If the last transformation is a MinMaxScaler with a target range of (-1, 1), the activation function is tanh.
        - Otherwise, no activation function is inferred. None is returned.

        Returns
        -------
        Optional[Union[str, nn.Module]]
            Activation function for the output head.
        """
        last_transf = self.transformations[-1] if len(self.transformations) > 0 else None
        if isinstance(last_transf, MinMaxScaler) and last_transf.target_range == (0, 1):
            return "sigmoid"
        elif isinstance(last_transf, MinMaxScaler) and last_transf.target_range == (-1, 1):
            return "tanh"
        else:
            # Activation function can not be inferred, choosing no activation function for the output head
            return None

    def get_ml_heads(self, head_layer_widths: List[int], last_core_layer_width: int, activation: nn.Module, **kwargs) -> Tuple[nn.Module, nn.Module]:
        """
        Returns a fully-connected head for encoding and decoding this feature

        Parameters
        ----------
        head_layer_widths : List[int]
            List of integers where the length denotes number of layers and values the width of the layers in the head
        last_core_layer_width : int
            Dimensionality of autoencoder output to be decoded by this feature head
        activation : nn.Module
            Activation function to be used in this head

        Returns
        -------
        Tuple[nn.Module, nn.Module]
            Tuple containing the input and output head.
        """
        out_activation = self.get_activation_outhead()
        return InHeadFC(self.dim, head_layer_widths, activation), OutHeadFC(last_core_layer_width, head_layer_widths[::-1] + [self.dim], activation, out_activation, **kwargs)


class DataCategorical(DataDiscrete):
    """
    Categorical data type.

    Parameters
    ----------
    name : str
        Name of the data object.
    dim : int
        Dimensionality of the data object, or different columns to perform the split on.
    domain : Options, optional
        Domain of the data object.
    position : int, optional
        Position of the data object in the vector.
    position_index : int, optional
        Index of the data object in the vector.
    dtype: str, optional
        The dtype of the numpy are of the expected data matrix.
    flag_split_perdim : bool, optional
        If True, object is split across dimensions in a DataBlock.
    """

    def __init__(
        self, name: str, dim: int = 1, domain: dd.Options = None, position: int = None, position_index: int = None, dtype: str = None, flag_split_perdim: bool = False, **kwargs
    ):
        type = "categorical"

        if domain is not None:
            domain = dd.check_domain_options(domain, expected_type=type)
        else:
            warnings.warn("Expected to get an object of class <Option> as a domain. One created automatically with entries 0 to 9")
            domain = dd.Options(list(range(0, 10)), type)

        if dtype is None:
            dtype = ud.data_types(domain.array)[1]

        transformations = [LabelEncoder()]
        super().__init__(
            name,
            dim,
            domain,
            position=position,
            position_index=position_index,
            transformations=transformations,
            type=type,
            dtype=dtype,
            flag_split_perdim=flag_split_perdim,
        )

    @classmethod
    def from_options(cls, name: str, option_list: list, dim: int = 1, dtype: str = None, flag_split_perdim: bool = False) -> DataCategorical:
        """
        Class method to for initialization from list of integers

        Parameters
        ----------
        name : str
            Name of the data object.
        option_list : list
            List of integers to be used as domain.
        dim : int, optional
            Dimensionality of the data object, or different columns to perform the split on.
        dtype: str, optional
            The dtype of the numpy are of the expected data matrix.
        flag_split_perdim : bool, optional
            If True, object is split across dimensions in a DataBlock.

        Returns
        -------
        DataCategorical
            A DataCategorical object.
        """
        domain = dd.Options(option_list, type="categorical")
        return cls(name=name, dim=dim, domain=domain, dtype=dtype, flag_split_perdim=flag_split_perdim)

    def get_objective(self, **kwargs) -> nn.Module:
        """
        Returns the loss function for approximating this feature.
        We use the benefit of combining the loss and activation function in one function. This avoids numerical instabilities.
        """
        if len(self.domain.array) <= 2:
            return nn.BCEWithLogitsLoss(**kwargs)
        else:
            return CrossEntropyLoss(class_indices=True, **kwargs)

    def get_loss_evaluation(self, **kwargs) -> nn.Module:
        """
        Returns the loss function for approximating this feature.
        """

        def cat_err(input, target):
            # Target is expected to be class indices in the range [0, num_classes-1], where num_classes=len(self.domain.array)
            if not target.shape[1] == 1:
                raise ValueError("The target must be of the form (*, 1)")
            if not target.trunc().equal(target):
                raise ValueError("The target must contain class indices (integers)")

            if len(self.domain.array) <= 2:
                # Binary classification, note if we get class indices (i.e., 0 or 1's) the following statement has no effect,
                # otherwise it converts the probabilities/logits to class indices
                input = torch.where(input <= 0, 0, 1)
            elif input.shape[1] == 1:  # Multi-class classification with class indices
                pass
            else:  # Multi-class classification with class probabilities
                input = torch.argmax(input, dim=1).reshape(-1, 1)

            return torch.ne(input, target).to(torch.int)

        return cat_err

    def get_activation_outhead(self):
        """
        Returns the activation function for approximating this feature.
        The feature is approximated by unnormalized logits, which is enforced by the self.get_objective() function.
        """
        return None

    def get_ml_heads(self, head_layer_widths: List[int], last_core_layer_width: int, activation: nn.Module, **kwargs) -> Tuple[nn.Module, nn.Module]:
        """
        Returns a fully-connected head with the appropriate number of in / out channels for encoding / decoding this feature

        Parameters
        ----------
        head_layer_widths : List[int]
            List of integers where the length denotes number of layers and values the width of the layers in the head
        last_core_layer_width : int
            Dimensionality of autoencoder output to be decoded by this feature head
        activation : nn.Module
            Activation function to be used in this head

        Returns
        -------
        Tuple[nn.Module, nn.Module]
            Tuple containing the input and output head.
        """
        out_activation = self.get_activation_outhead()

        num_classes = max(len(self.domain.array), 2)  # We allow domains with single classes
        in_head = CategoricalInHead(num_classes, head_layer_widths, activation)
        out_head = CategoricalOutHead(num_classes, last_core_layer_width, head_layer_widths[::-1], activation, out_activation)

        return in_head, out_head

    def copy(self, reset: bool = False, **kwargs) -> DataCategorical:
        transformations = kwargs.pop("transformations") if "transformations" in kwargs else [t.copy(reset=reset) for t in self.transformations]

        # Categoricals can not have a unit, so we remove it from the kwargs
        if "unit" in kwargs:
            kwargs.pop("unit")

        dobj_copy = type(self)(
            name=kwargs.pop("name", self.name),
            dim=kwargs.pop("dim", self.dim),
            domain=kwargs.pop("domain", self.domain.copy()),
            dtype=kwargs.pop("dtype", self.dtype),
            flag_split_perdim=kwargs.pop("flag_split_perdim", self.flag_split_perdim),
            **kwargs,
        )  # use the constructor based on the type of the object, so that we can copy subclasses of DataCategorical

        # Transformations cannot be set through the constructor of DataCategorical, as it is restricted to LabelEncoder()
        # However we need to copy the state of the transformations, so we do it after the object is created
        dobj_copy.transformations = transformations
        return dobj_copy


class DataBool(DataCategorical):
    """
    Boolean type, i.e., categorical type with options 'True', 'False'

    Parameters
    ----------
    name : str
        Name of the data object.
    dim : int
        Dimensionality of the data object, or different columns to perform the split on.
    kwargs
        Additional keyword arguments passed to `DataCategorical`.
    """

    def __init__(self, name: str, dim: int = 1, **kwargs):
        domain = kwargs.pop("domain", dd.Options(["True", "False"], type="categorical"))
        super().__init__(name, dim, domain, **kwargs)


class DataOrdinal(DataDiscrete):
    """
    Ordinal data type

    Parameters
    ----------
    name : str
        Name of the data object.
    dim : int, optional, default=1
        Dimensionality of the data object, or different columns to perform the split on.
    domain : Options, optional, default=None
        Domain of the data object.
    unit : str, optional, default=None
        Unit of the data object (e.g. m, kg. m^2, m/s^2 etc.). Use ^ to indicate powers (e.g. m^2), and _ to indicate subscripts (e.g. m_1).
    position : int, optional, default=None
        Position of the data object in the vector.
    position_index : int, optional, default=None
        Index of the data object in the vector.
    transformations: Union[List[str], List[DataObjectTransform]], optional, default=None
        List of transformations to be applied to the data object.
    dtype: str, optional, default=None
        The dtype of the numpy are of the expected data matrix.
    flag_split_perdim : bool, optional, default=False
        If True, object is split across dimensions in a DataBlock.
    """

    def __init__(
        self,
        name: str,
        dim: int = 1,
        domain: dd.Options = None,
        unit: str = None,
        position: int = None,
        position_index: int = None,
        transformations: Union[List[str], List[DataObjectTransform]] = None,
        dtype: str = None,
        flag_split_perdim: bool = False,
    ):
        # TODO: This class will be implemented correctly with https://gitlab.renkulab.io/ai-augmented-design/aixd/-/issues/111
        warnings.warn("The data object DataOrdinal is not yet in a stable state, and should not be used. It will be implemented in a future release.")

        type = "ordinal"

        if domain is not None:
            domain = dd.check_domain_options(domain, expected_type=type)
        else:
            warnings.warn("Expected to get an object of class <Option> as a domain. One created automatically with entries 0 to 9")
            domain = dd.Options(list(range(0, 10)), type)

        if dtype is None:
            dtype = ud.data_types(domain.array)[1]

        transformations = transformations if transformations is not None else []
        if "cat_to_one_hot" not in [(t.name if isinstance(t, DataObjectTransform) else t) for t in transformations]:
            transformations = ["cat_to_one_hot"] + transformations

        super().__init__(
            name,
            dim,
            domain,
            unit,
            position,
            position_index,
            transformations,
            type,
            dtype,
            flag_split_perdim,
        )

    @classmethod
    def from_options(
        cls,
        name: str,
        option_list: list,
        dim: int = 1,
        unit: str = None,
        transformations: Union[List[str], List[DataObjectTransform]] = None,
        dtype: str = None,
        flag_split_perdim: bool = False,
    ):
        domain = dd.Options(option_list, type="ordinal")
        cls(
            name,
            dim,
            domain,
            unit=unit,
            transformations=transformations,
            dtype=dtype,
            flag_split_perdim=flag_split_perdim,
        )

    def get_objective(self, **kwargs):
        """
        Returns the loss function for approximating this feature.
        """
        # TODO This is not the correct loss function for ordinal data
        if len(self.domain.array) <= 2:
            return nn.BCEWithLogitsLoss(**kwargs)
        else:
            return nn.CrossEntropyLoss(**kwargs)

    def get_loss_evaluation(self, **kwargs) -> nn.Module:
        """
        Returns the loss function for approximating this feature.
        """

        def ord_err(a, b):
            ind_a = torch.argmax(a, dim=1)
            ind_b = torch.argmax(b, dim=1)
            return torch.sub(ind_a, ind_b).abs().reshape(-1, 1)

        return ord_err

    def get_activation_outhead(self):
        """
        Returns the loss function for approximating this feature.
        """
        raise NotImplementedError()

    def get_ml_heads(self, head_layer_widths: List[int], last_core_layer_width: int, activation: nn.Module, **kwargs) -> tuple:
        """
        Returns a fully-connected head for encoding and decoding this feature

        Parameters
        ----------
        head_layer_widths : List[int]
            List of integers where the length denotes number of layers and values the width of the layers in the head
        last_core_layer_width : int
            Dimensionality of autoencoder output to be decoded by this feature head
        activation : nn.Module
            Activation function to be used in this head
        """
        out_activation = self.get_activation_outhead()
        return InHeadFC(self.dim, head_layer_widths, activation), OutHeadFC(last_core_layer_width, head_layer_widths[::-1] + [self.dim], activation, out_activation, **kwargs)


SelfDataMatrix = TypeVar("SelfDataMatrix", bound="DataObject")  # this is the same as typing.Self, but that is only available in python 3.10


class DataMatrix(DataObject):
    """
    Matrix type, e.g., to represent image data.

    Parameters
    ----------
    name : str
        Name of the data object.
    shape: tuple
        The shape of the underling matrix
    dim : int, optional, default=1
        Dimensionality of the data object (i.e., size of the flattened matrix), or different columns to perform the split on.
    domain : Interval, optional, default=None
        Domain of the data object.
    position : int, optional, default=None
        Position of the data object in the vector.
    position_index : int, optional, default=None
        Index of the data object in the vector.
    transformations: Union[List[str], List[DataObjectTransform]], optional, default=None
        List of transformations to be applied to the data object.
    dtype: str, optional, default="float64"
        The dtype of the numpy are of the expected data matrix.
    flag_split_perdim : bool, optional, default=False
        If True, object is split across dimensions in a DataBlock.
    """

    def __init__(
        self,
        name: str,
        shape: Tuple[int, int],
        dim: int = 1,
        domain: dd.Interval = None,
        position: int = None,
        position_index: int = None,
        transformations: Union[List[str], List[DataObjectTransform]] = None,
        dtype: str = "float64",
        flag_split_perdim: bool = False,
    ):
        # TODO: This class is not yet in a stable state, and should not be used. It will be implemented in a future release.
        # Once this class is stabilized, the implementation of __jsondump__ / __jsonload__
        # will need to be revised, and probably an overload of them will need to be added
        # in which the self.shape property is de/serialized.
        warnings.warn("The data object DataMatrix is not yet in a stable state, and should not be used. It will be implemented in a future release.")

        type = "real"

        if domain is not None:
            domain = dd.check_domain_interval(domain, expected_type=type)
        else:
            warnings.warn("Expected to get an object of class <Interval> as a domain. One created automatically with range 0 to 254")
            domain = dd.Interval(0, 254, type)

        if transformations is None:
            transformations = [ZeroToOne(per_column=False)]

        super().__init__(name, dim, domain, None, position, position_index, transformations, type, dtype, flag_split_perdim)
        self.shape = shape

    @classmethod
    def from_range(
        cls,
        name: str,
        shape: Tuple[int, int],
        vmin: int,
        vmax: int,
        dim: int = 1,
        transformations: Union[List[str], List[DataObjectTransform]] = None,
        dtype: str = "float64",
        flag_split_perdim: bool = False,
    ):
        """
        Class method for initialization from range defined by vmin and vmax.

        Parameters
        ----------
        name : str
            Name of the data object.
        shape: tuple
            The shape of the underling matrix
        vmin : int
            Lower bound of the interval domain.
        vmax : int
            Upper bound of the interval domain.
        dim : int, optional, default=1
            Dimensionality of the data object (i.e., size of the flattened matrix), or different columns to perform the split on.
        transformations: Union[List[str], List[DataObjectTransform]], optional, default=None
            List of transformations to be applied to the data object.
        dtype: str, optional, default="float64"
            The dtype of the numpy are of the expected data matrix.
        flag_split_perdim : bool, optional, default=False
            If True, object is split across dimensions in a DataBlock.

        Returns
        -------
        DataMatrix
            A DataMatrix object.
        """
        domain = dd.Interval(vmin, vmax)
        return cls(
            name,
            shape,
            dim,
            domain,
            transformations=transformations,
            dtype=dtype,
            flag_split_perdim=flag_split_perdim,
        )

    def get_objective(self, **kwargs) -> nn.Module:
        """
        Returns the loss function for approximating this feature.
        """
        return nn.MSELoss(**kwargs)

    def get_loss_evaluation(self, **kwargs) -> nn.Module:
        """
        Returns the loss function for approximating this feature.
        """
        return nn.L1Loss(reduction="none")

    def get_activation_outhead(self) -> Optional[Union[str, nn.Module]]:
        """
        Tries to interfere the activation function for the output head, based on the last transformation. It follows the following rules:

        - If the last transformation is a MinMaxScaler with a target range of (0, 1), the activation function is sigmoid.
        - If the last transformation is a MinMaxScaler with a target range of (-1, 1), the activation function is tanh.
        - Otherwise, no activation function is inferred. None is returned.

        Returns
        -------
        Optional[Union[str, nn.Module]]
            Activation function for the output head.
        """
        last_transf = self.transformations[-1] if len(self.transformations) > 0 else None
        if isinstance(last_transf, MinMaxScaler) and last_transf.target_range == (0, 1):
            return "sigmoid"
        elif isinstance(last_transf, MinMaxScaler) and last_transf.target_range == (-1, 1):
            return "tanh"
        else:
            # Activation function can not be inferred, choosing no activation function for the output head
            return None

    def get_ml_heads(self, head_layer_widths: List[int], last_core_layer_width: int, activation: nn.Module, **kwargs) -> tuple:
        # TODO: Add support for matrices with other than 2 dimensions.
        out_activation = self.get_activation_outhead()
        return InHeadConv2D(
            self.shape,
            head_layer_widths,
            activation,
            attn_block_indices=[len(head_layer_widths) // 2] if len(head_layer_widths) > 0 else [],
        ), OutHeadConv2D(
            last_core_layer_width,
            self.shape,
            head_layer_widths[::-1],
            activation,
            out_activation,
            attn_block_indices=[len(head_layer_widths) // 2] if len(head_layer_widths) > 0 else [],
        )

    def copy(self, reset: bool = False, **kwargs) -> SelfDataMatrix:
        kwargs = {"shape": self.shape} | kwargs
        return super().copy(**kwargs)


class DataOther(DataObject):
    """
    This is intended for DesignRepresentations that cannot be loaded, or in principle
    are not intended to be loaded, such as images of rendered. So no domain or anything related
    is provided.
    """

    def __init__(self, name: str, dim: int = 0):
        # This class is just for the outputs that are probably not to be used by the ML model, such as renders
        super().__init__(name, dim, domain=dd.Domain(), type="other")
