"""
This module has been copied and modified from the COMPAS framework (``compas.data.encoders`` and ``compas.data.data``).

It preserves the same programming interface of the COMPAS data framework, so it would be data compatible with it.

There are some subtle differences that are worth highlighting:
 - This module will check for the existance of both dtype and data before assuming the object is a serialized
   AIXD/COMPAS object, to avoid clashes with existing AIXD data objects and also to be more robust in general
 - The dtype is COMPAS is defined as the first 2 levels of the module name, a ``/``, and the class name, but this module
   does not limit the module name to two levels, and will serialize any level of the class name.
"""

from __future__ import absolute_import, division, print_function

try:
    from typing import Type  # noqa: F401
except ImportError:
    pass

import json

import numpy as np


class DecoderError(Exception):
    """Exception that is raised when the decoder fails at reconstructing an object that has been identified as an AIXD data object."""


def obj_to_dtype(obj):
    return "{}/{}".format(".".join(obj.__class__.__module__.split(".")), obj.__class__.__name__)


def cls_from_dtype(dtype):
    """Get the class object corresponding to a COMPAS/AIXD data type specification.

    Parameters
    ----------
    dtype : str
        The data type of the COMPAS/AIXD object in the following format:
        '{}/{}'.format(o.__class__.__module__, o.__class__.__name__).

    Raises
    ------
    ValueError
        If the data type is not in the correct format.
    ImportError
        If the module can't be imported.
    AttributeError
        If the module doesn't contain the specified data type.

    """
    mod_name, attr_name = dtype.split("/")
    module = __import__(mod_name, fromlist=[attr_name])
    return getattr(module, attr_name)


class DataEncoder(json.JSONEncoder):
    """Data encoder for custom JSON serialization with support for COMPAS/AIXD objects.

    The encoder adds the following conversions to the JSON serialization process:

    * Numpy objects to their Python equivalents;
    * iterables to lists; and
    * objects complying with the data protocol of COMPAS/AIXD,
      such as geometric primitives and shapes, data structures, etc,
      to a dict with the following structure: ``{'dtype': o.__dtype__, 'data': o.__data__}``

    Examples
    --------
    >>> from aixd.data.encoders import json_dump
    >>> from aixd.data import Dataset
    >>> ds = Dataset("test_dataset")
    >>> serialized_dataset = json_dumps(ds)

    """

    def default(self, o):
        """Return an object in serialized form.

        Parameters
        ----------
        o : object
            The object to serialize.

        Returns
        -------
        str
            The serialized object.

        """

        if hasattr(o, "__jsondump__"):
            return {
                "dtype": obj_to_dtype(o),
                "data": o.__jsondump__(),
            }

        if hasattr(o, "__next__"):
            return list(o)

        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(
            o,
            (
                np.int_,
                np.intc,
                np.intp,
                np.int8,
                np.int16,
                np.int32,
                np.int64,
                np.uint8,
                np.uint16,
                np.uint32,
                np.uint64,
            ),  # type: ignore
        ):
            return int(o)
        if isinstance(o, (np.float_, np.float16, np.float32, np.float64)):  # type: ignore
            return float(o)
        if isinstance(o, np.bool_):
            return bool(o)
        if isinstance(o, np.void):
            return None

        return super(DataEncoder, self).default(o)


class DataDecoder(json.JSONDecoder):
    """Data decoder for custom JSON serialization with support for COMPAS/AIXD objects.

    The decoder hooks into the JSON deserialization process
    to reconstruct objects complying to the data protocol of COMPAS/AIXD.

    The reconstruction is possible if

    * the serialized data has the following structure: ``{"dtype": "...", 'data': {...}}``;
    * a class can be imported into the current scope from the info in ``o["dtype"]``; and
    * the imported class has a method ``__from_data__``.

    Examples
    --------
    >>> from aixd.data.encoders import json_load
    >>> ds = json_loads(serialized_dataset)  # doctest: +SKIP

    """

    def __init__(self, *args, **kwargs):
        super(DataDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, o):
        """Reconstruct a deserialized object.

        Parameters
        ----------
        o : object

        Returns
        -------
        object
            A (reconstructed), deserialized object.

        """
        if "dtype" not in o or "data" not in o:
            return o

        try:
            cls = cls_from_dtype(o["dtype"])

        except ValueError:
            raise DecoderError(
                "The data type of the object should be in the following format: '{}/{}'".format(
                    o.__class__.__module__,
                    o.__class__.__name__,
                )
            )

        except ImportError:
            raise DecoderError("The module of the data type can't be found: {}.".format(o["dtype"]))

        except AttributeError:
            raise DecoderError("The data type can't be found in the specified module: {}.".format(o["dtype"]))

        data = o["data"]
        obj = cls.__jsonload__(data)

        return obj


def json_dump(data, fp, pretty=False, compact=False):
    """Write a collection of AIXD object data to a JSON file.

    Parameters
    ----------
    data : object
        Any JSON serializable object.
        This includes any (combination of) AIXD object(s).
    fp : path string or file-like object
        A writeable file-like object or the path to a file.
    pretty : bool, optional
        If True, format the output with newlines and indentation.
    compact : bool, optional
        If True, format the output without any whitespace.
    """
    with open(fp, "w") as f:
        kwargs = {}

        if pretty:
            kwargs["sort_keys"] = True
            kwargs["indent"] = 4
        if compact:
            kwargs["indent"] = None
            kwargs["separators"] = (",", ":")

        return json.dump(data, f, cls=DataEncoder, **kwargs)


def json_dumps(data, pretty=False, compact=False):  # type: (...) -> str
    """Write a collection of AIXD objects to a JSON string.

    Parameters
    ----------
    data : object
        Any JSON serializable object.
        This includes any (combination of) AIXD object(s).
    pretty : bool, optional
        If True, format the output with newlines and indentation.
    compact : bool, optional
        If True, format the output without any whitespace.

    Returns
    -------
    str

    """
    kwargs = {}
    if pretty:
        kwargs["sort_keys"] = True
        kwargs["indent"] = 4
    if compact:
        kwargs["indent"] = None
        kwargs["separators"] = (",", ":")

    return json.dumps(data, cls=DataEncoder, **kwargs)


def json_load(fp):  # type: (...) -> dict
    """Read AIXD object data from a JSON file.

    Parameters
    ----------
    fp : path string | file-like object | URL string
        A readable path, a file-like object or a URL pointing to a file.

    Returns
    -------
    object
        The data contained in the file.
    """
    with open(fp, "r") as f:
        return json.load(f, cls=DataDecoder)


def json_loads(s):  # type: (...) -> dict
    return json.loads(s, cls=DataDecoder)
