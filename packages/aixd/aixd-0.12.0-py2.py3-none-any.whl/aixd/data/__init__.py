"""
********************************************************************************
aixd.data
********************************************************************************

This package contains classes for defining data objects, data blocks, normalizations and transformations that are used
to describe datasets.

.. currentmodule:: aixd.data

Dataset
-------
.. autosummary::
    :toctree: generated/
    :nosignatures:

    Dataset


Data objects
------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    DataObject
    DataReal
    DataDiscrete
    DataInt
    DataCategorical
    DataBool


Domain definitions
------------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Domain
    Options
    Interval
    IntervalMasked


Data blocks
-----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    DataBlock
    DesignParameters
    PerformanceAttributes
    DesignRepresentation
    TransformableDataBlock
    InputML
    OutputML

.. currentmodule:: aixd.data.custom_callbacks

Custom callbacks
----------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    CustomCallback
    AnalysisCallback
    DataloaderCallback
    ImportCallback
    PostGenerationCallback
    SamplingCallback

.. currentmodule:: aixd.data.transform

Transformation
--------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    register_transformation
    resolve_transformation
    DataObjectTransform
    Log10Transform
    SigmoidTransform
    Standardization
    MinMaxScaler
    ZeroToOne
    MinusOneToOne
    MaskedMinMaxScaler
    MaskedZeroToOne
    MaskedMinusOneToOne
    LabelEncoder
    ToFloat

.. currentmodule:: aixd.data

Utils
-----

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~utils_data.convert_to
    ~utils_data.combine_formats
    ~utils_data.reformat_dict_to_dataframe
    ~utils_data.reformat_dataframe_to_dict
    ~utils_data.reformat_dataframe_to_dictlist
    ~utils_data.reformat_dataframeflat_to_dict
    ~utils_data.reformat_dataframe_to_dataframeflat
    ~utils_data.reformat_dataframeflat_to_dataframe
    ~utils_data.reformat_list_to_array
    ~utils_data.reformat_array_to_list
    ~utils_data.reformat_list_to_dataframe
    ~utils_data.reformat_dataframe_to_list
    ~utils_data.reformat_list_to_dict
    ~utils_data.reformat_list_to_dictlist
    ~utils_data.reformat_dictlist_to_dict
    ~utils_data.reformat_dict_to_dictlist
    ~utils_data.reformat_array_to_torch
    ~utils_data.reformat_torch_to_array
"""

from .data_blocks import (
    DataBlock,
    DesignParameters,
    DesignRepresentation,
    InputML,
    OutputML,
    PerformanceAttributes,
    TransformableDataBlock,
)
from .data_objects import (
    DataBool,
    DataCategorical,
    DataDiscrete,
    DataInt,
    DataMatrix,
    DataObject,
    DataOrdinal,
    DataOther,
    DataReal,
)
from .dataset import Dataset
from .domain import (
    Domain,
    Options,
    Interval,
    IntervalMasked,
)

__all__ = [
    # domain definitions
    "Domain",
    "Options",
    "Interval",
    "IntervalMasked",
    # data objects
    "DataBool",
    "DataCategorical",
    "DataDiscrete",
    "DataInt",
    "DataMatrix",
    "DataObject",
    "DataOrdinal",
    "DataOther",
    "DataReal",
    # data blocks
    "DataBlock",
    "InputML",
    "OutputML",
    "DesignParameters",
    "PerformanceAttributes",
    "DesignRepresentation",
    "TransformableDataBlock",
    # dataset
    "Dataset",
]
