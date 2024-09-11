from typing import List, Union

import numpy as np
import pandas as pd

from aixd.data import DataObject
from aixd.data.custom_callbacks import SamplingCallback
from aixd.sampler.engines import SamplingEngine
from aixd.sampler.operators import Operator
from aixd.sampler.sampler import SamplesGenerator
from aixd.sampler.strategies import KernelDensityStrategy, QuantileStrategy, UniformStrategy


def sampler_uniform(dobjects: List[DataObject], engine: SamplingEngine, callbacks_class: SamplingCallback = None) -> SamplesGenerator:
    """
    Just a sampler to uniformly sample from all design parameters

    Parameters
    ----------
    dobjects: List[DataObject]
        List of DataObjects to sample from
    engine: SamplingEngine
        To use for sampling
    callbacks_class: SamplingCallback, optional, default=None
        In case we want to run some function on the samples obtained in the sampling process.
        This is intended for advanced usage.

    Returns
    -------
    SamplesGenerator
        The sampler object
    """
    strategies = [UniformStrategy([d for d in dobjects], engine=engine)]
    sampler = SamplesGenerator(strategies, callbacks_class=callbacks_class)
    return sampler


def sampler_kde(dobjects: List[DataObject], engine: SamplingEngine, callbacks_class: SamplingCallback = None) -> SamplesGenerator:
    """
    A KDE sampler that can be fit to some data, and then sample from its distribution

    Parameters
    ----------
    dobjects: List[DataObject]
        List of DataObjects to sample from
    engine: SamplingEngine
        To use for sampling
    callbacks_class: SamplingCallback, default=None
        In case we want to run some function on the samples obtained in the sampling process.
        This is intended for advanced usage.

    Returns
    -------
    SamplesGenerator
        The sampler object
    """
    strategies = [KernelDensityStrategy([d for d in dobjects], engine=engine)]
    sampler = SamplesGenerator(strategies, callbacks_class=callbacks_class)
    return sampler


def sampler_quantile(dobjects: List[DataObject], engine: SamplingEngine, callbacks_class: SamplingCallback = None) -> SamplesGenerator:
    """
    A sampler that can be fit to some data, and then sample using a quantile strategy. The
    sampling is univariate, so each column is sampled independently.

    Parameters
    ----------
    dobjects: List[DataObject]
        List of DataObjects to sample from
    engine: SamplingEngine
        To use for sampling
    callbacks_class: SamplingCallback, optional, default=None
        In case we want to run some function on the samples obtained in the sampling process.
        This is intended for advanced usage.

    Returns
    -------
    SamplesGenerator
        The sampler object
    """
    strategies = [QuantileStrategy([d for d in dobjects], engine=engine)]
    sampler = SamplesGenerator(strategies, callbacks_class=callbacks_class)
    return sampler


def sampler_custom(dobjects: List[DataObject], engine: SamplingEngine, data: Union[pd.DataFrame, np.array] = None) -> SamplesGenerator:
    """
    A sampler to sample from all design parameters, given some data containing the distributions we are intending
    For each column, aka dataobject, we can just specify a different distribution.

    Parameters
    ----------
    dobjects: List[DataObject]
        List of DataObjects to sample from
    engine: SamplingEngine
        To use for sampling
    data: Union[pd.DataFrame, np.array], optional, default=None
        Just a quantile strategy for sampler that is fitted to some data, in order
        to provide samples that follow, in an univariate fashion, the distribution of the data.

    Returns
    -------
    SamplesGenerator
        The sampler object
    """
    if data is not None:
        strategies = [QuantileStrategy([d for d in dobjects], engine=engine)]
        sampler = SamplesGenerator(strategies, callbacks_class=None)
        sampler.fit(data)
        return sampler
    else:
        return sampler_uniform(dobjects, engine)


def sampler_conditional_kde(
    dobjects: List[DataObject], engine: SamplingEngine, condition: Operator, data: Union[pd.DataFrame, np.array] = None, callbacks_class: SamplingCallback = None
) -> SamplesGenerator:
    """
    A KDE sampler fitted to some data, and also link to some conditions. When sampling,
    only the samples that satisfy some conditions are returned.

    Parameters
    ----------
    dobjects: List[DataObject]
        List of DataObjects to sample from
    engine: SamplingEngine
        To use for sampling
    condition: Operator
        The condition the samples need to satisfy
    data: Union[pd.DataFrame, np.array], optional, default=None
        Just a quantile strategy for sampler that is fitted to some data, in order
        to provide samples that follow, in an univariate fashion, the distribution of the data.
    callbacks_class: SamplingCallback, optional, default=None
        In case we want to run some function on the samples obtained in the sampling process.
        This is intended for advanced usage.

    Returns
    -------
    SamplesGenerator
        The sampler object
    """
    strategies = [KernelDensityStrategy([d for d in dobjects], engine=engine)]
    sampler = SamplesGenerator(strategies, condition=condition, callbacks_class=callbacks_class)
    if data is not None:
        sampler.fit(data)
    return sampler


def sampler_bayesian_kde(
    dobjects: List[DataObject],
    engine: SamplingEngine,
    objective: Operator,
    condition: Operator = None,
    data: Union[pd.DataFrame, np.array] = None,
    callbacks_class: SamplingCallback = None,
) -> SamplesGenerator:
    """
    A KDE fitted to some data, and then sampling optimizing for some objective. This process is slower
    than a KDE sampler with a condition.

    Parameters
    ----------
    dobjects: List[DataObject]
        List of DataObjects to sample from
    engine: SamplingEngine
        To use for sampling
    objective: Operator
        Objective operator to measure the performance of the obtained samples,
        in order to update the strategy of the sampler. Used in the Bayesian case.
    condition: Operator
        The condition the samples need to satisfy
    data: Union[pd.DataFrame, np.array]
        Just a quantile strategy for sampler that is fitted to some data, in order
        to provide samples that follow, in an univariate fashion, the distribution of the data.
    callbacks_class: SamplingCallback
        In case we want to run some function on the samples obtained in the sampling process.
        This is intended for advanced usage.

    Returns
    -------
    sampler: SamplesGenerator
        The sampler object
    """
    strategies = [KernelDensityStrategy([d for d in dobjects], engine=engine)]
    sampler = SamplesGenerator(strategies, objective=objective, condition=condition, callbacks_class=callbacks_class)

    if data is not None:
        sampler.fit(data)
    return sampler


def sampler_wrapper(
    dobjects: List[DataObject],
    engine: SamplingEngine,
    objective: Operator = None,
    condition: Operator = None,
    data: Union[pd.DataFrame, np.array] = None,
    callbacks_class: SamplingCallback = None,
) -> SamplesGenerator:
    """
    A writter to call the correct sampler based on the input arguments. A KDE sampler is called when the  objective is None.

    Parameters
    ----------
    dobjects: List[DataObject]
        List of DataObjects to sample from
    engine: SamplingEngine
        To use for sampling
    objective: Operator
        Objective operator to measure the performance of the obtained samples,
        in order to update the strategy of the sampler. Used in the Bayesian case.
    condition: Operator
        The condition the samples need to satisfy
    data: Union[pd.DataFrame, np.array]
        Just a quantile strategy for sampler that is fitted to some data, in order
        to provide samples that follow, in an univariate fashion, the distribution of the data.
    callbacks_class: SamplingCallback
        In case we want to run some function on the samples obtained in the sampling process.
        This is intended for advanced usage.

    Returns
    -------
    sampler: SamplesGenerator
        The sampler object
    """
    if isinstance(objective, Operator):
        return sampler_bayesian_kde(dobjects, engine, objective, condition, data, callbacks_class)
    else:
        return sampler_conditional_kde(dobjects, engine, condition, data, callbacks_class)
