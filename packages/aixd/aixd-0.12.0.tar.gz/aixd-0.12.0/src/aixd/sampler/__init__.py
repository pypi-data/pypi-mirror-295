"""
********************************************************************************
aixd.sampler
********************************************************************************

This package contains .....

.. toctree::
    :maxdepth: 1

    aixd.sampler.callbacks
    aixd.sampler.constants
    aixd.sampler.engines
    aixd.sampler.operators
    aixd.sampler.reducers
    aixd.sampler.sampler
    aixd.sampler.sampler_definitions
    aixd.sampler.strategies

.. currentmodule:: aixd.sampler.callbacks

Callbacks
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    GeneratorCallback


.. currentmodule:: aixd.sampler.engines

Engines
-------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    SamplingEngine
    AgnosticSamplingEngine
    AdaptiveSamplingEngine
    RandomSamplingEngine
    GridamplingEngine
    SobolSamplingEngine
    LHCSamplingEngine
    BayesOptSamplingEngine

.. currentmodule:: aixd.sampler.operators

Operators
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Operator
    Arithmetic
    Boolean
    Constant
    Add
    Multiply
    Subtract
    Divide
    LessThan
    LessOrEqual
    GreaterThan
    GreaterOrEqual
    Log
    Exp
    Pow
    Not
    And
    Or
    XOr
    Equal
    Negative
    CastBooleanToConstant


.. currentmodule:: aixd.sampler.reducers

Reducers
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Reducer
    Sum
    Mean
    Std
    Var
    All
    Any


.. currentmodule:: aixd.sampler.sampler_definitions

Samplers
--------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    sampler_uniform
    sampler_kde
    sampler_quantile
    sampler_custom
    sampler_conditional_kde
    sampler_bayesian_kde


.. currentmodule:: aixd.sampler.sampler

Samples generator
-----------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    SamplesGenerator


.. currentmodule:: aixd.sampler.strategies

Strategies
----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Strategy
    UniformStrategy
    QuantileStrategy
    KernelDensityStrategy


"""
