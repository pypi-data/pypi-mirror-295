from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Optional

import numpy as np

from aixd.data.domain import IntervalMasked, Options
from aixd.utils import logs

if TYPE_CHECKING:  # avoid circular imports, as the following is only used for type checking
    from aixd.data.data_objects import DataObject

_registered_transformations = {}

logger = logs.get_logger().get_child("transform")


def list_transformations():
    """Returns the list of registered transformations."""
    return list(_registered_transformations.keys())


def register_transformation(name):
    """Defines the decorator to register transformations. The decorator takes a name as argument and sets it as a static attribute on the class."""

    def decorator(transformation_class):
        if name in _registered_transformations:
            raise Exception(f"Transformation with name {name} already registered.")
        transformation_class.name = name
        _registered_transformations[name] = transformation_class
        return transformation_class

    return decorator


def resolve_transformation(name, *args, **kwargs) -> DataObjectTransform:
    """Simple resolver that returns the transformation by its name."""
    if name in _registered_transformations:
        transformation_class = _registered_transformations[name]
        return transformation_class(*args, **kwargs)
    else:
        raise ValueError(f"Transformation '{name}' is not registered. Use the decorator @register_transformation()")


class DataObjectTransform:
    """
    Abstract base class to implement DataObject transformation.

    Subclass this class to implement custom transformations, by implementing the following methods:

    - `transform`: Method to implement to transform input data
    - `inverse_transform`: Method to implement to inverse transform input data
    - `_fit_partial`: Method to implement to fit transformation
    - `is_fitted`: Method to implement to check if transformation is fitted

    and register the transformation using the decorator `@register_transformation("name")`.

    If the transformation requires no fitting, set the class attribute `requires_fitting` to `False`, so don't need to implement the `_fit_partial`, and `is_fitted` method.
    """

    name: str = None  # set by the decorator
    requires_fitting: bool = True

    def fit(self, data_mat: np.ndarray, dobj: Optional[DataObject]) -> DataObjectTransform:
        """
        Fits the transformation.

        Parameters
        ----------
        data_mat : np.ndarray
            The input data.
        dobj : Optional[DataObject]
            The data object.

        Returns
        -------
        DataObjectTransform
            The fitted transformation.

        """
        self.reset()
        self._fit_partial(data_mat, dobj)
        return self

    def _fit_partial(self, data_mat: np.ndarray, dobj: Optional[DataObject]) -> None:
        """Method to implement to fit transformation"""
        if self.requires_fitting:
            raise NotImplementedError()
        else:
            pass

    def is_fitted(self) -> bool:
        """Returns true if transformation strategy is fitted."""
        if self.requires_fitting:
            raise NotImplementedError()
        else:
            return True

    def reset(self):
        """Method to implement to reset fitted values."""
        return self

    def fit_transform(self, data_mat: np.ndarray, dobj: Optional[DataObject]) -> np.ndarray:
        """
        Fits and transforms the input.

        Parameters
        ----------
        data_mat : np.ndarray
            The input data.
        dobj : Optional[DataObject]
            The data object.

        Returns
        -------
        np.ndarray
            The transformed data.

        """
        return self.fit(data_mat, dobj).transform(data_mat, dobj)

    def transform(self, data_mat: np.ndarray, dobj: Optional[DataObject]) -> np.ndarray:
        """
        Transforms the input.

        Parameters
        ----------
        data_mat : np.ndarray
            The input data.
        dobj : Optional[DataObject]
            The data object.

        Returns
        -------
        np.ndarray
            The transformed data.

        """
        raise NotImplementedError()

    def inverse_transform(self, data_mat: np.ndarray, dobj: Optional[DataObject]) -> np.ndarray:
        """
        Inverse transform of the input.

        Parameters
        ----------
        data_mat : np.ndarray
            The input data.
        dobj : Optional[DataObject]
            The data object.

        Returns
        -------
        np.ndarray
            The inverse transformed data.

        """
        raise NotImplementedError()

    def copy(self, reset: bool = False):
        """
        Copies the transformation.

        Parameters
        ----------
        reset : bool, default=False
            If set, the transformation is reset. So the copy is not fitted.
        """
        obj_copy = copy.copy(self)
        if reset:
            obj_copy.reset()
        return obj_copy

    def __jsondump__(self):
        return {}

    @classmethod
    def __jsonload__(cls, data):
        return cls(**data)


@register_transformation("log10")
class Log10Transform(DataObjectTransform):
    """
    Implements a log10 transformation of the data.
    """

    requires_fitting = False

    def transform(self, data_mat: np.ndarray, dobj: Optional[DataObject] = None) -> np.ndarray:
        return np.log10(data_mat + 1)

    def inverse_transform(self, data_mat: np.ndarray, dobj: Optional[DataObject] = None) -> np.ndarray:
        return np.power(10, data_mat) - 1


@register_transformation("sigmoid")
class SigmoidTransform(DataObjectTransform):
    """
    Implements a scaled sigmoid transformation of the data.
    """

    def __init__(self):
        super().__init__()
        self.scale_factor = None

    def is_fitted(self) -> bool:
        return self.scale_factor is not None

    def reset(self):
        self.scale_factor = None

    def _fit_partial(self, data_mat: np.ndarray, dobj: Optional[DataObject] = None):
        self.scale_factor = np.abs([1 / np.min(data_mat), 1 / np.max(data_mat)]).max()

    def transform(self, data_mat: np.ndarray, dobj: Optional[DataObject] = None) -> np.ndarray:
        return 1 / (1 + np.exp(-data_mat * self.scale_factor))

    def inverse_transform(self, data_mat: np.ndarray, dobj: Optional[DataObject] = None) -> np.ndarray:
        return (1 / self.scale_factor) * np.log(data_mat / (1 - data_mat + 1e-16))


@register_transformation("standard_scaler")
class Standardization(DataObjectTransform):
    """
    Implements standardization as (x - mean) / std.

    Parameters
    ----------
    per_column : bool, default=True
        If set normalization is performed per column for multi-dim DataObjects.
    """

    def __init__(self, per_column: bool = True):
        super().__init__()
        self.mean = None
        self.std = None
        self.per_column = per_column

    def is_fitted(self) -> bool:
        return self.mean is not None and self.std is not None

    def reset(self):
        self.mean, self.std = None, None

    def _fit_partial(self, data_mat: np.ndarray, dobj: Optional[DataObject] = None) -> None:
        self.mean = np.mean(data_mat, axis=0) if self.per_column else np.mean(data_mat)
        self.std = np.std(data_mat, axis=0) if self.per_column else np.std(data_mat)

    def transform(self, data_mat: np.ndarray, dobj: Optional[DataObject] = None) -> np.ndarray:
        return (data_mat - self.mean) / (self.std + 1e-10)

    def inverse_transform(self, data_mat: np.ndarray, dobj: Optional[DataObject] = None) -> np.ndarray:
        return data_mat * self.std + self.mean


@register_transformation("min_max_scaler")
class MinMaxScaler(DataObjectTransform):
    """
    Implements a min-max scaling of the data.

    Parameters
    ----------
    target_range : tuple, default=(0, 1)
        The target range for the scaling.
    per_column : bool, default=True
        If set normalization is performed per column for multi-dim DataObjects.
    """

    def __init__(self, target_range: tuple = (0, 1), per_column: bool = True):
        super().__init__()
        self.target_range = target_range
        self.per_column = per_column
        self.min, self.max = None, None

    def is_fitted(self) -> bool:
        return self.min is not None and self.max is not None

    def reset(self):
        self.min, self.max = None, None

    def _fit_partial(self, data_mat: np.ndarray, dobj: Optional[DataObject] = None):
        self.min = np.min(data_mat, axis=0) if self.per_column else np.min(data_mat)
        self.max = np.max(data_mat, axis=0) if self.per_column else np.max(data_mat)

    def transform(self, data_mat: np.ndarray, dobj: Optional[DataObject] = None) -> np.ndarray:

        centered = data_mat - self.min
        span = self.max - self.min

        if np.allclose(span, 0):  # span is zero if all values are the same.
            data_mat_std = centered
        else:
            data_mat_std = centered / span

        return data_mat_std * (self.target_range[1] - self.target_range[0]) + self.target_range[0]  # scale to target range

    def inverse_transform(self, data_mat: np.ndarray, dobj: Optional[DataObject] = None) -> np.ndarray:
        data_mat = (data_mat - self.target_range[0]) / (self.target_range[1] - self.target_range[0])  # scale to 0-1
        return data_mat * (self.max - self.min) + self.min  # scale to original range


@register_transformation("norm_0to1")
class ZeroToOne(MinMaxScaler):
    """
    Implements the zero-to-one (or min-max) normalization as (x - min) / (max - min).

    Parameters
    ----------
    per_column : bool, default=True
        If set normalization is performed per column for multi-dim DataObjects.
    """

    def __init__(self, per_column: bool = True):
        super().__init__((0, 1), per_column)


@register_transformation("norm_m1to1")
class MinusOneToOne(MinMaxScaler):
    """
    Implements the minus-one-to-one normalization as (x - min) / (max - min).

    Parameters
    ----------
    per_column : bool, default=True
        If set normalization is performed per column for multi-dim DataObjects.
    """

    def __init__(self, per_column: bool = True):
        super().__init__((-1, 1), per_column)


@register_transformation("masked_min_max_scaler")
class MaskedMinMaxScaler(MinMaxScaler):
    """
    Implements min-max scaling of the data with a masked domain. I.e., the masked values are not considered in the min-max computation, and not scaled.

    Parameters
    ----------
    target_range : tuple, default=(0, 1)
        The target range for the scaling.
    per_column : bool, default=True
        If set normalization is performed per column for multi-dim DataObjects.
    scale_inverse_masked : bool, default=True
        If set, the inverse transformation will scale the masked values, otherwise they are kept as they are. See notes for more details.

    Notes
    -----
    Since masked values are not considered in the min-max computation, more than one value can be mapped to the same value in the target range, making the inverse
    transformation ambiguous. The argument `scale_inverse_masked` controls this behavior. If set, the inverse transformation will scale the masked values, otherwise they
    are kept as they are.
    """

    def __init__(self, target_range: tuple = (0, 1), per_column: bool = True, scale_inverse_masked: bool = True):
        super().__init__(target_range, per_column)
        self.scale_inverse_masked = scale_inverse_masked

    def _fit_partial(self, data_mat: np.ndarray, dobj: Optional[DataObject] = None) -> None:
        if dobj.domain is not None and isinstance(dobj.domain, IntervalMasked):
            if self.per_column:
                self.min = np.asarray([np.min(data_mat[:, o][~np.isin(data_mat[:, o], dobj.domain.options)]) for o in range(data_mat.shape[1])])
                self.max = np.asarray([np.max(data_mat[:, o][~np.isin(data_mat[:, o], dobj.domain.options)]) for o in range(data_mat.shape[1])])
            else:
                self.min = np.min(data_mat[~np.isin(data_mat, dobj.domain.options)])
                self.max = np.max(data_mat[~np.isin(data_mat, dobj.domain.options)])
        else:
            raise Exception("Expected DataObject with domain of type IntervalMasked.")

        if not all(self.target_range[0] <= o <= self.target_range[1] for o in dobj.domain.options):
            logger.warning(f"Target range {self.target_range} does not include all the masked values.")

    def transform(self, data_mat: np.ndarray, dobj: Optional[DataObject] = None) -> np.ndarray:
        if dobj.domain is not None and isinstance(dobj.domain, IntervalMasked):
            data_mat_transformed = super().transform(data_mat, dobj)
            data_mat_transformed[np.isin(data_mat, dobj.domain.options)] = data_mat[np.isin(data_mat, dobj.domain.options)]  # keep masked values

        else:
            raise Exception("Expected DataObject with domain of type IntervalMasked.")

        return data_mat_transformed

    def inverse_transform(self, data_mat: np.ndarray, dobj: Optional[DataObject] = None) -> np.ndarray:
        if dobj.domain is not None and isinstance(dobj.domain, IntervalMasked):
            data_mat_inverse = super().inverse_transform(data_mat, dobj)

            if not self.scale_inverse_masked:
                data_mat_inverse[np.isin(data_mat, dobj.domain.options)] = data_mat[np.isin(data_mat, dobj.domain.options)]  # keep masked values
        else:
            raise Exception("Expected DataObject with domain of type IntervalMasked.")

        return data_mat_inverse


@register_transformation("masked_norm_0to1")
class MaskedZeroToOne(MaskedMinMaxScaler):
    """
    Implements the zero-to-one (or min-max) normalization as (x - min) / (max - min) for DataObject's with a MaskedInterval domain.

    Parameters
    ----------
    per_column : bool, default=True
        If set normalization is performed per column for multi-dim DataObjects.
    """

    def __init__(self, per_column=True, scale_inverse_masked: bool = True):
        super().__init__((0, 1), per_column, scale_inverse_masked)


@register_transformation("masked_norm_m1to1")
class MaskedMinusOneToOne(MaskedMinMaxScaler):
    """
    Implements the minus-one-to-one normalization for DataObject's with a MaskedInterval domain.

    Parameters
    ----------
    per_column : bool, default=True
        If set normalization is performed per column for multi-dim DataObjects.
    """

    def __init__(self, per_column=True, scale_inverse_masked: bool = True):
        super().__init__((-1, 1), per_column, scale_inverse_masked)


@register_transformation("to_float")
class ToFloat(DataObjectTransform):
    """
    Implement a transformation to convert integers to floats. The inverse transforms ensures that values are not outside the domain.
    """

    requires_fitting = False

    def is_fitted(self) -> bool:
        return True

    def transform(self, data_mat: np.ndarray, dobj: Optional[DataObject] = None):
        return data_mat.astype(float)

    def inverse_transform(self, data_mat: np.ndarray, dobj: Optional[DataObject]):
        return np.round(data_mat).astype(int)


@register_transformation("label_encoder")
class LabelEncoder(DataObjectTransform):
    """
    Implements encoding for string to integers.
    """

    def __init__(self):
        super().__init__()
        self.mapping = None

    def is_fitted(self) -> bool:
        return self.mapping is not None

    def reset(self):
        self.mapping = None

    def fit(self, data_mat: np.ndarray, dobj: Optional[DataObject]):
        if not isinstance(dobj.domain, Options):
            raise Exception("Domain must be of type Options.")

        # This is required to reduce the dimensionality of the one-hot-encoding vector
        dobj.update_obj(data_mat)
        self.mapping = {cat: i for i, cat in enumerate(dobj.domain.array)}
        return self

    def transform(self, data_mat: np.ndarray, dobj: Optional[DataObject]):
        data_mat_id = np.zeros_like(data_mat, dtype=int)
        for cat, i in self.mapping.items():
            data_mat_id[data_mat == cat] = i
        return data_mat_id

    def inverse_transform(self, data_mat: np.ndarray, dobj: Optional[DataObject]):
        data_mat_cat = np.zeros_like(data_mat, dtype=dobj.dtype)
        data_mat = data_mat.astype(float)  # in case strings are passed
        for cat, i in self.mapping.items():
            data_mat_cat[data_mat == i] = cat
        return data_mat_cat
