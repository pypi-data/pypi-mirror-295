import warnings
from typing import List, Tuple, Union

import numpy as np

from aixd.utils.utils import float_ceil, float_floor


class Domain:
    """
    Abstract base class for domains used by DataObjects.
    """

    def __init__(self):
        self.type = "any"

    def __jsondump__(self):
        return {"type": self.type}

    @classmethod
    def __jsonload__(cls, data):
        obj = cls()
        obj.type = data["type"]
        return obj

    @property
    def domain_type(self) -> str:
        """Returns the type of the domain. By default, it is the name of the class."""
        return self.__class__.__name__

    def random_samples(self, size: Union[int, Tuple[int, int]] = 1) -> np.ndarray:
        """
        Returns samples chosen with random sampling from the domain.

        Parameters
        ----------
        size : Union[int, Tuple[int, int]], optional, default=1
            Output shape. If the given shape is, e.g., (m, n), then m * n samples are drawn.

        Returns
        -------
        np.ndarray
            The generated random samples from the domain.
        """
        raise NotImplementedError

    def grid_samples(self, size: Union[int, Tuple[int, int]] = 1) -> np.ndarray:
        """
        Returns samples chosen with grid sampling from the domain.

        Parameters
        ----------
        size : Union[int, Tuple[int, int]], optional, default=1
            Output shape. If the given shape is, e.g., (m, n), then m * n samples are drawn.
        """
        raise NotImplementedError

    def sample_around(self, centroids: Union[float, int, List, np.ndarray], size: Union[int, Tuple[int, int]], percentage: int, **kwargs) -> np.ndarray:
        """
        Returns samples chosen with a sample around strategy from the domain.

        Parameters
        ----------
        centroids : np.ndarray
            The values at each dimension to sample around.
        size : Tuple[int, int]
            A tuple indicating the number of samples and the dimension, i.e. (number_sample, dim).
        percentage : float
            Controls the sampling.
        kwargs
            Additional arguments depending on the domain.

        Returns
        -------
        np.ndarray
            The generated samples from the domain.
        """
        raise NotImplementedError

    def normalised_to_domain(self, values: np.ndarray) -> np.ndarray:
        """
        Maps from a distribution in [0, 1] to the domain.

        Parameters
        ----------
        values : np.ndarray
            Values in [0, 1] to map to the domain.

        Returns
        -------
        np.ndarray
            The mapped values in the domain.
        """
        raise NotImplementedError

    def domain_to_normalised(self, values: np.ndarray) -> np.ndarray:
        """
        Maps from the domain to a distribution in [0, 1].

        Parameters
        ----------
        values : np.ndarray
            The domain values to map to [0, 1].

        Returns
        -------
        np.ndarray
            The mapped/normalised values in [0, 1].
        """
        raise NotImplementedError

    def update_domain(self, data: Union[List, np.ndarray], type: str = None, strict: bool = True, **kwargs) -> Union[None, str]:
        """
        Updates the domain according to the given data.

        Parameters
        ----------
        data : Union[List, np.ndarray]
            The data to update the domain.
        type : str, optional, default=None
            The type of the domain.
        strict : bool, optional, default=False
            If True, the domain is updated to match the data exactly. Otherwise, the domain is updated to include the data.

        Returns
        -------
        Union[None, str]
            A message indicating if the domain was updated. If None, the domain was not updated.

        """
        raise NotImplementedError

    def check_domain_consistency(self, data: Union[List, np.ndarray], strict: bool = True) -> Union[None, str]:
        """
        Checks if the data is within the domain.

        Parameters
        ----------
        data : Union[List, np.ndarray]
            The data to check.
        strict : bool, optional, default=False
            If True, the domain is checked to match the data exactly. Otherwise, the domain is checked to include the data.

        Returns
        -------
        Union[None, str]
            A message indicating if the domain is consistent with the data. If None, the domain is consistent.
        """
        raise NotImplementedError

    def copy(self):
        """Returns a copy of the instance."""
        raise NotImplementedError

    def __repr__(self):
        """
        Returns a representation of the Domain.
        """
        raise NotImplementedError


class Options(Domain):
    """
    Defines a set of options, e.g., for categorical variables.

    Parameters
    ----------
    array : List
        The list of options.
    type : str, optional, default="categorical"
        The type of the domain. Can be "categorical", "ordinal", "integer", "any".
    """

    def __init__(self, array: List, type: str = "categorical"):
        super(Options, self).__init__()

        self.type = self._check_type_arg(type)
        self.array = array

    def __jsondump__(self):
        return {"type": self.type, "array": self.array}

    @classmethod
    def __jsonload__(cls, data):
        return cls(**data)

    @property
    def array(self):
        return self._array

    @array.setter
    def array(self, array):
        self._array = self._check_options_arg(array)
        self._option_to_idx = {c: i for i, c in enumerate(self.array)}

    @property
    def option_to_idx(self):
        return self._option_to_idx

    def _check_options_arg(self, options: List) -> List:
        """Checks if the options are valid. They must be unique, and sorted in ascending order if the type is integer."""

        if len(options) == 0:
            raise ValueError("The list of options cannot be empty.")

        # Options must be unique
        indexes = np.unique(options, return_index=True)[1]
        options_unique = [options[index] for index in sorted(indexes)]

        # For integer options, they must be sorted in ascending order, so we can sample around them.
        if self.type == "integer":
            options_unique = sorted(options_unique)
        return options_unique

    @staticmethod
    def _check_type_arg(type_: str) -> str:
        """Checks if the type is valid. It can be categorical, ordinal, integer, any"""
        if type_ not in ["categorical", "ordinal", "integer", "any"]:
            raise ValueError(f"The type of the domain is not valid. It can be categorical, ordinal, integer or any, but got {type_}.")
        return type_

    def random_samples(self, size: Union[int, Tuple[int, int]] = None) -> np.ndarray:
        return np.random.choice(self.array, size=size)

    def grid_samples(self, size: Union[int, Tuple[int, int]] = None) -> np.ndarray:
        n_samples = 1 if isinstance(size, int) else size[0]
        dim = size if isinstance(size, int) else size[1]

        if dim > len(self.array):
            n_rep = np.ceil(dim / len(self.array))
            samples = np.repeat(np.repeat(self.array, n_rep)[None], n_samples, axis=0)
            samples = np.apply_along_axis(np.random.permutation, axis=1, arr=samples)[:, :dim]  # Shuffles each row independently
        elif dim < len(self.array):
            samples = np.random.choice(self.array, size=(n_samples, dim))
        else:  # This case covers dim == len(self.array)
            samples = np.repeat(self.array, n_samples, axis=0)  # TODO: maisseal - do we really want that when dim == len(self.array) we repeat the same sample n_samples times?

        return samples.flatten() if isinstance(size, int) else samples

    def sample_around(self, centroids: Union[float, int, str, List, np.ndarray], size: Union[int, Tuple[int, int]] = 1, percentage: int = 10, **kwargs):
        if not isinstance(centroids, list) and not isinstance(centroids, np.ndarray):
            return self._sample_around_single(centroids, size, percentage)  # centroids is a single value

        if isinstance(size, tuple):
            raise ValueError("The size argument must be an integer when sampling around multiple centroids.")

        samples = np.column_stack([self._sample_around_single(centroid, size, percentage) for centroid in centroids])

        if self.type == "integer":
            samples = samples.astype(int)

        return samples

    def _sample_around_single(self, centroid: Union[float, int], size: Union[int, Tuple[int, int]] = 1, percentage: int = 10):
        """Helper function for sampling around a single centroid value."""
        if self.type == "categorical":
            raise Exception("Categorical variables are not supported for sampling around.")

        # Find value in array
        idx = [idx for idx, val in enumerate(self.array) if val == centroid]  # self.array is a unique list
        if len(idx) == 0:
            raise Exception(f"The option {centroid} is not in the domain. Failed to sample around it.")
        else:
            idx = idx[0]

        span = len(self.array) * 0.5 * percentage / 100.0
        min_idx = np.max([0, idx - int(np.round(span))])
        max_idx = np.min([len(self.array), idx + int(np.round(span + 1))])

        return np.random.choice(self.array[min_idx:max_idx], size=size)

    def normalised_to_domain(self, values: np.ndarray) -> np.ndarray:
        """
        Maps from a distribution in [0, 1] to [0, len(self.array)] and is then rounded to serve as indices for discretisation.

        Parameters
        ----------
        values : np.ndarray
            Values in [0, 1] to map to the domain.

        Returns
        -------
        np.ndarray
            The discretised values.
        """
        ixs = np.clip(values * len(self.array), a_min=None, a_max=len(self.array) - 1e-8).astype(int).flatten()
        disc_values = np.array(self.array)[ixs]
        return disc_values.reshape(values.shape)

    def domain_to_normalised(self, values: np.ndarray) -> np.ndarray:
        """
        Maps from discrete values to a range [0, 1] by attributing an equal share of the range to each of the possible options of the domain.

        Parameters
        ----------
        values : np.ndarray
            The domain values to map to [0, 1].

        Returns
        -------
        np.ndarray
            The mapped/normalised values in [0, 1].
        """
        from operator import itemgetter

        ixs = np.array([itemgetter(*list(values[:, i]))(self.option_to_idx) for i in range(values.shape[1])]).reshape(values.shape)

        return ixs / len(self.array)

    def update_domain(self, data: Union[List, np.ndarray], type: str = None, strict=True, **kwargs) -> Union[None, str]:
        self.type = self._check_type_arg(type) if type is not None else self.type
        return self._check_domain_consistency(data, flag_update=True, strict=strict)

    def check_domain_consistency(self, data: Union[List, np.ndarray], strict=True) -> Union[None, str]:
        return self._check_domain_consistency(data, strict=strict)

    def _check_domain_consistency(self, data: Union[List, np.ndarray], flag_update=False, strict=True) -> Union[None, str]:
        data = np.asarray(data)

        unique_vals = np.unique(data.flatten())
        invalid_data_options = np.setdiff1d(unique_vals, np.asarray(self.array))
        unused_domain_options = np.setdiff1d(np.asarray(self.array), unique_vals)

        msg = ""
        if len(invalid_data_options) > 0:
            msg += f"The data contains options that are not in the domain: {invalid_data_options}. "

        if len(unused_domain_options) > 0 and strict:  # if strict, we want to make sure that all options are used
            msg += "The data does not cover the entire domain. "

        if len(invalid_data_options) > 0 and flag_update and not strict:
            self.array = np.unique(np.concatenate([self.array, invalid_data_options.tolist()])).tolist()  # Add the invalid options to the domain
            msg += f"Updating the domain to match the data. The new domain is now {self}. "
        elif (len(unused_domain_options) > 0 or len(invalid_data_options)) and flag_update and strict:  # if strict, only add the options that are in the data
            self.array = unique_vals.tolist()
            msg += f"Updating the domain to match the data. The new domain is now {self}. "
        else:
            pass  # do nothing

        return msg if len(msg) > 0 else None

    def copy(self):
        return Options([a for a in self.array], self.type)

    def __repr__(self):
        if len(self.array) <= 10:
            return self.__class__.__name__ + "([{}])".format(", ".join([str(o) for o in self.array]))
        else:
            aux_str = ", ".join([str(o) for o in self.array[:5]]) + ", ...," + ", ".join([str(o) for o in self.array[-5:]])
            return self.__class__.__name__ + "([{}])".format(aux_str)


class Interval(Domain):
    """Defines a closed interval [a, b], for a <= b. The interval can either be defined on the real or integer numbers.

    Parameters
    ----------
    min_value : Union[float, int], optional, default=0
        The minimum value of the interval. If None, there is no minimum value.
    max_value : Union[float, int], optional, default=1
        The maximum value of the interval. If None, there is no maximum value.
    type : str, optional, default="real"
        The type of the domain. Can be "real" or "integer", defining whether the interval is defined on the real or integer numbers.
    """

    def __init__(self, min_value: Union[float, int] = 0, max_value: Union[float, int] = 1, type: str = "real"):
        super(Interval, self).__init__()

        self.type = self._check_type_arg(type)
        self.min_value, self.max_value = self._check_range(min_value, max_value)

    def __jsondump__(self):
        return {"type": self.type, "min_value": self.min_value, "max_value": self.max_value}

    @classmethod
    def __jsonload__(cls, data):
        return cls(**data)

    @staticmethod
    def _check_type_arg(type_: str) -> str:
        """Checks if the type is valid. It can be real, or integer"""
        if type_ not in ["real", "integer", "any"]:
            raise ValueError(f"The type of the domain is not valid. It can be real or integer, but got {type_}.")
        return type_

    def _check_range(self, min_value: Union[float, int], max_value: Union[float, int]) -> tuple:
        """Checks if the given range is valid. Raises an error if not."""
        if min_value > max_value:
            raise ValueError("The min value must be smaller than the max value")

        if self.type == "integer":
            min_value, max_value = int(min_value), int(max_value)
        elif self.type == "real":
            min_value, max_value = float(min_value), float(max_value)
        else:
            pass

        return min_value, max_value

    def random_samples(self, size: Union[int, Tuple[int, int]] = 1) -> np.ndarray:
        return self._random_samples(size)

    def _random_samples(self, size: Union[int, Tuple[int, int]] = 1, min_value: Union[float, int] = None, max_value: Union[float, int] = None) -> np.ndarray:
        """Helper function for random sampling. It also checks if the given range is valid."""
        min_value = self.min_value if min_value is None else min_value
        max_value = self.max_value if max_value is None else max_value
        min_value, max_value = self._check_range(min_value, max_value)

        if self.type == "integer":
            min_value, max_value = int(round(min_value)), int(round(max_value)) + 1
            return np.random.randint(low=min_value, high=max_value, size=size)
        elif self.type == "real":
            return np.random.uniform(low=min_value, high=max_value, size=size)
        else:
            raise Exception("The type of the domain is not valid. It can be real or integer.")

    def grid_samples(self, size: Union[int, Tuple[int, int]] = 1) -> np.ndarray:
        n_samples = 1 if isinstance(size, int) else size[0]
        dim = size if isinstance(size, int) else size[1]

        samples = np.linspace(self.min_value, self.max_value, dim)
        samples = np.repeat(samples, n_samples, axis=0)

        if self.type == "integer":
            samples = samples.astype(int)

        return samples.flatten() if isinstance(size, int) else samples

    def sample_around(
        self,
        centroids: Union[float, int, List, np.ndarray],
        size: Union[int, Tuple[int, int]] = 1,
        percentage: int = 10,
        min_value: Union[float, int] = None,
        max_value: Union[float, int] = None,
    ) -> np.ndarray:
        if not isinstance(centroids, list) and not isinstance(centroids, np.ndarray):
            return self._sample_around_single(centroids, size, percentage, min_value, max_value)  # centroids is a single value

        if isinstance(size, tuple):
            raise ValueError("The size argument must be an integer when sampling around multiple centroids.")

        samples = np.column_stack([self._sample_around_single(centroid, size, percentage, min_value, max_value) for centroid in centroids])

        if self.type == "integer":
            samples = samples.astype(int)

        return samples

    def _sample_around_single(
        self,
        centroid: Union[float, int],
        size: Union[int, Tuple[int, int]] = 1,
        percentage: int = 10,
        min_value: Union[float, int] = None,
        max_value: Union[float, int] = None,
    ) -> np.ndarray:
        """
        Helper function to samples around a centroid value, while the span around the centroid is defined by the percentage of the range of the
        domain (or by the passed min and max values).
        """
        min_value = self.min_value if min_value is None else min_value
        max_value = self.max_value if max_value is None else max_value

        span = (max_value - min_value) * 0.5 * percentage / 100.0
        minv = max(centroid - span, min_value)
        maxv = min(centroid + span, max_value)

        return self._random_samples(size, minv, maxv)

    def normalised_to_domain(self, values: np.ndarray) -> np.ndarray:
        """Maps from a distribution in [0, 1] to [self.min_val, self.max_val]"""
        values = values * (self.max_value - self.min_value) + self.min_value
        if self.type == "integer":
            values = np.clip(np.round(values), a_min=self.min_value, a_max=self.max_value).astype(int)
        return values

    def domain_to_normalised(self, values: np.ndarray) -> np.ndarray:
        """Maps from a distribution in [self.min_val, self.max_val] to [0, 1]. If the domain is a single point, the normalised value is 0."""

        centered = values - self.min_value
        span = self.max_value - self.min_value
        if np.isclose([span], [0]):
            return centered
        else:
            return centered / span

    def update_domain(self, data, type: str = None, strict=True, precision: int = 3) -> Union[None, str]:
        self.type = self._check_type_arg(type) if type is not None else self.type
        return self._check_domain_consistency(data, flag_update=True, strict=strict, precision=precision)

    def check_domain_consistency(self, data: Union[List, np.ndarray], strict: bool = True) -> Union[None, str]:
        return self._check_domain_consistency(data, strict=strict)

    def _check_domain_consistency(self, data: Union[List, np.ndarray], flag_update: bool = False, strict: bool = True, precision: int = 3) -> Union[None, str]:
        data = np.asarray(data)
        data_min, data_max = np.min(data), np.max(data)
        data_min, data_max = float_floor(data_min, digits=precision), float_ceil(data_max, digits=precision)

        new_min = self.min_value if self.min_value <= data_min and not strict else data_min  # if strict, we only update the minimum if the data is outside the current domain
        new_max = self.max_value if self.max_value >= data_max and not strict else data_max  # if strict, we only update the maximum if the data is outside the current domain

        min_max_changed = new_min != self.min_value or new_max != self.max_value

        if min_max_changed:
            msg = f"The domain spans the interval [{self.min_value}, {self.max_value}], but the data spans the interval [{data_min}, {data_max}] (floored/ceiled to {precision} decimal)."
            if flag_update:
                self.min_value, self.max_value = self._check_range(new_min, new_max)
                msg += f" Updating the domain to match the data. The new domain is {self}."
        else:
            msg = None

        return msg

    def copy(self):
        return Interval(self.min_value, self.max_value, self.type)

    def __repr__(self):
        min_value = int(self.min_value) if self.type == "integer" else float(self.min_value)
        max_value = int(self.max_value) if self.type == "integer" else float(self.max_value)
        return f"{self.__class__.__name__}({min_value}, {max_value})"


class IntervalMasked(Interval):
    """
    A domain that allows to define an interval with several options/masks, not in the interval. Can be used to define a masked interval, e.g., [1.2, 2.2] with 0 as options/mask.

    For an example usage of this domain, refer to the Semiramis example in the documentation.

    Parameters
    ----------
    min_value : Union[float, int], optional, default=0
        The minimum value of the interval.
    max_value : Union[float, int], optional, default=1
        The maximum value of the interval.
    type : str, optional, default="real"
        The type of the domain. Can be "real" or "integer", defining whether the interval is defined on the real or integer numbers.
    options : List, optional, default=None
        The list of options/masks, not in the interval.
    """

    def __init__(self, min_value: Union[float, int] = 0, max_value: Union[float, int] = 1, type: str = "real", options: Union[List[int], List[float]] = None):
        super().__init__(min_value, max_value, type)
        self.options = options if options is not None else []

    def __jsondump__(self):
        return {"type": self.type, "min_value": self.min_value, "max_value": self.max_value, "options": self.options}

    @classmethod
    def __jsonload__(cls, data):
        return cls(**data)

    def _check_domain_consistency(self, data: Union[List, np.ndarray], flag_update: bool = False, strict: bool = True, precision: int = 3) -> Union[None, str]:
        data = np.asarray(data)
        mask_options = np.isin(data, self.options)
        data_masked = data[~mask_options]
        return super()._check_domain_consistency(data_masked, flag_update, strict=strict, precision=precision)

    def copy(self):
        return IntervalMasked(self.min_value, self.max_value, self.type, self.options)

    def __repr__(self):
        str_opt = ", ".join([str(o) for o in self.options])
        return f"{self.__class__.__name__}({self.min_value}, {self.max_value}, options=[{str_opt}])"


def check_domain_interval(interval: Domain, expected_type: str = None):
    """Checks if the domain is an object of class Interval, and converts it if necessary. It also checks if the type of the domain is the expected one."""
    if isinstance(interval, Options):
        warnings.warn("Expected to get an object of class <Interval> as a domain, got <Options> instead. It will now be converted for you, but check if it works as expected.")
        interval = Interval(min(interval.array), max(interval.array), type=interval.type if interval.type in ["real", "integer"] else "any")

    expected_type = expected_type if expected_type is not None else interval.type
    if interval.type != expected_type:
        warnings.warn(
            f"Expected to get an object of class <Interval> with type {expected_type}, but got type {interval.type} instead. Creating a new domain object with type to {expected_type}."
        )
        interval = Interval(interval.min_value, interval.max_value, type=expected_type)

    return interval


def check_domain_options(options: Domain, expected_type: str = None):
    """Checks if the domain is an object of class Options, and converts it if necessary. It also checks if the type of the domain is the expected one."""
    if isinstance(options, Interval):
        warnings.warn("Expected to get an object of class <Options> as a domain, got <Interval> instead. It will now be converted for you, but check if it works as expected.")
        options = Options(list(range(int(options.min_value), int(options.max_value))), type=options.type if options.type in ["integer"] else "any")

    expected_type = expected_type if expected_type is not None else options.type
    if options.type != expected_type:
        warnings.warn(
            f"Expected to get an object of class <Options> with type {expected_type}, but got type {options.type} instead. Creating a new domain object with type to {expected_type}."
        )
        options = Options(options.array, type=expected_type)

    return options
