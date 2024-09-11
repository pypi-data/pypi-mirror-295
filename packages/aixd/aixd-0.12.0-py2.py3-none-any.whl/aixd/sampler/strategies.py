from typing import Dict, List, Union

import numpy as np
import pandas as pd
import torch
from scipy.special import gammainc
from sklearn.neighbors import KernelDensity
from sklearn.preprocessing import QuantileTransformer
from sklearn.utils import check_random_state
from sklearn.utils.extmath import row_norms

from aixd.data.data_objects import DataObject
from aixd.sampler.constants import RANDOM_SEED_SAMPLING
from aixd.sampler.engines import AdaptiveSamplingEngine, AgnosticSamplingEngine, GridamplingEngine, SamplingEngine
from aixd.utils import logs

logger = logs.get_logger().get_child("sampler-mapping")


class Strategy:
    """
    Receives samples from the range [0, 1]^len(features) and maps them to the feature-space according to some strategy.
    NOTE: currently, there is no seeding mechanism, as we expect full randomness when sampling new points. Before
    it ocurred that the same points were sampled, which is not desirable.

    Parameters
    ----------
    features : Union[DataObject, List[DataObject]]
        The features refer to the data objects, which contain the information about the domain of the features.
    engine : Union[SamplingEngine, str]
        The different engines, such as GridamplingEngine, SobolSamplingEngine, RandomSamplingEngine, LHCSamplingEngine, etc.
    """

    def __init__(self, features: Union[DataObject, List[DataObject]], engine: Union[SamplingEngine, str], **kwargs):
        self.features = features if isinstance(features, list) else [features]
        self.engine = SamplingEngine.deserialise(engine, features=[f for f in self.features], **kwargs)
        self.seed = RANDOM_SEED_SAMPLING  # Random seed everytime

    def fit(self, data: Dict[str, Union[torch.Tensor, np.array]], objectives: Union[torch.Tensor, np.array], validity: Union[torch.Tensor, np.array]):
        """Fit the strategy to the data, also using some vectors of `objectives` and `validity` values."""
        self.engine.update({f.name: f.domain.domain_to_normalised(data[f.name]) for f in self.features}, objectives, validity)

    def sample(self, n: int) -> Dict[str, np.array]:
        NotImplementedError()

    def update(self, samples: Dict[str, Union[torch.Tensor, np.array]], objectives: Union[torch.Tensor, np.array], validity: Union[torch.Tensor, np.array]):
        """
        Updates the state of the sampling methods by providing the performance of the generated samples
        in the form of `objectives` and `validity`.

        Parameters
        ----------
        samples : Dict[str, Union[torch.Tensor, np.array]]
            The samnples at which the objectives and conditions where evaluated.
        objectives : Union[torch.Tensor, np.array]
            The performance of the generated samples according to some objective,
            higher the better (of type float and shape (n, 1)).
        valid : Union[torch.Tensor, np.array]
            Whether the generated samples were valid or not (of type boolean and shape (n, 1))
        """
        self.engine.update({f.name: f.domain.domain_to_normalised(samples[f.name]) for f in self.features}, objectives, validity)

    def reset_states(self):
        """Reset the state of the engine."""
        self.engine.reset_states()


class UniformStrategy(Strategy):
    """
    Scales and shifts the samples from [0, 1] to [feature.min, feature.max]) for continuous features, or discretises them through binning.

    Parameters
    ----------
    features : Union[DataObject, List[DataObject]]
        The features refer to the data objects, which contain the information about the domain of the features.
    engine : Union[SamplingEngine, str], optional, default="random"
        In this case the default engine is "random", as it is the only one that makes sense to use with this strategy.
    """

    def __init__(self, features: Union[DataObject, List[DataObject]], engine: Union[SamplingEngine, str] = "random", **kwargs):
        super().__init__(features, engine, **kwargs)

    def sample(self, n: int) -> Dict[str, np.array]:
        uniform_samples = self.engine.sample(n)
        aux_dict = {}
        feature_count = 0
        for i, f in enumerate(self.features):
            aux_dict[f.name] = f.domain.normalised_to_domain(uniform_samples[:, feature_count : (feature_count + f.dim)])
            feature_count += f.dim
        return aux_dict


class QuantileStrategy(Strategy):
    """
    Fits a univariate quantile transformer to each of the features. Allows to sample according to some prior distribution
    provided by the user through the "fit" function.
    https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.QuantileTransformer.html

    Parameters
    ----------
    features : Union[DataObject, List[DataObject]]
        The features refer to the data objects, which contain the information about the domain of the features.
    n_quantiles : float, optional, default=1000
        Number of quantiles to be computed. It corresponds to the number of landmarks used to discretize the cumulative
        distribution.
    engine : Union[SamplingEngine, str], optional, default="random"
        In this case the default engine is "random", as it is the only one that makes sense to use with this strategy.
    """

    # TODO: Make it work with features that have more than one dimension
    def __init__(self, features: Union[DataObject, List[DataObject]], n_quantiles: float = 1000, engine: Union[SamplingEngine, str] = "random", **kwargs):
        super().__init__(features, engine, **kwargs)
        self.n_quantiles = n_quantiles
        self.qts = None

    def fit(self, data: Dict[str, Union[torch.Tensor, np.array]], objectives: Union[torch.Tensor, np.array], validity: Union[torch.Tensor, np.array]):
        super().fit(data, objectives, validity)

        data = convert_to_numpy_dict(data)

        self.qts = {}
        for feature in self.features:
            self.qts[feature.name] = QuantileTransformer(n_quantiles=min(self.n_quantiles, len(data[feature.name])), output_distribution="uniform")
            self.qts[feature.name].fit(feature.domain.domain_to_normalised(data[feature.name].reshape(-1, len(feature.columns_df))))

    def sample(self, n: int) -> Dict[str, np.array]:
        if self.qts is None:
            raise ValueError('Strategy has not been initialised. Call "fit(data)" to initialise it.')

        uniform_samples = self.engine.sample(n)

        aux_dict = {}
        feature_count = 0
        for i, f in enumerate(self.features):
            aux_dict[f.name] = f.domain.normalised_to_domain(self.qts[f.name].inverse_transform(uniform_samples[:, feature_count : (feature_count + f.dim)]))
            feature_count += f.dim
        return aux_dict

    def reset_states(self):
        super().reset_states()
        self.qts = None


class KernelDensityStrategy(Strategy):
    """
    Fits a multivariate Kernel Density Estimator to the features. Allows to sample according to some prior distribution
    provided by the user through the "fit" function.
    https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KernelDensity.html

    Parameters
    ----------
    features : Union[DataObject, List[DataObject]]
        The features refer to the data objects, which contain the information about the domain of the features.
    bandwidth : float, optional, default=0.05
        The badnwidth of the kernel for the KDE.
    engine : Union[SamplingEngine, str], optional, default="random"
        In this case the default engine is "random", as it is the only one that makes sense to use with this strategy.
    """

    # TODO: Make it work with features that have more than one dimension
    def __init__(self, features: Union[DataObject, List[DataObject]], bandwidth: float = 0.05, engine: Union[SamplingEngine, str] = "random", **kwargs):
        super().__init__(features, engine, **kwargs)
        if isinstance(self.engine, GridamplingEngine):
            logger.warning(
                "Using GridamplingEngine in combination with KernelDensityStrategy can result in unexpected behaviour,"
                + " as only a small subset of points in the prior dataset will be selected due to the discretisation."
            )

        self.bandwidth = bandwidth
        self.kde = None

    def fit(self, data: Dict[str, Union[torch.Tensor, np.array]], objectives: Union[torch.Tensor, np.array], validity: Union[torch.Tensor, np.array]):
        super().fit(data, objectives, validity)
        data = convert_to_numpy_dict(data)

        self.kde = KernelDensity(bandwidth=self.bandwidth, kernel="gaussian", rtol=1e-9, atol=1e-9)
        self.kde.fit(np.hstack([feature.domain.domain_to_normalised(data[feature.name].reshape(-1, len(feature.columns_df))) for feature in self.features]))

    def sample(self, n: int) -> Dict[str, np.array]:
        if self.kde is None:
            raise ValueError('Strategy has not been initialised. Call "fit(data)" to initialise it.')

        if isinstance(self.engine, AdaptiveSamplingEngine):
            # the engine learns the prior distribution of the data through the `objective`.
            res = self.engine.sample(n)
        else:
            # the engine is agnostic to the `objective` and therefore the KDE sampling procedure must be used.
            res = self.__custom_kernel_density_sample(n)

        aux_dict = {}
        feature_count = 0
        for i, f in enumerate(self.features):
            aux_dict[f.name] = f.domain.normalised_to_domain(res[:, feature_count : (feature_count + f.dim)])
            feature_count += f.dim
        return aux_dict

    def update(self, samples, objectives, validity):
        """
        Add the log-likelihood of the samples to the objectives. This way, f.ex. a BayesOptSamplingEngine learns to sample
        from the prior distribution.
        """
        if not isinstance(self.engine, AgnosticSamplingEngine):
            dict_norm = {f.name: f.domain.domain_to_normalised(samples[f.name]) for f in self.features}
            samples_array = np.concatenate([dict_norm[feature.name] for feature in self.features], axis=1, dtype=object) if len(samples) > 1 else samples[self.features[0]]
            objectives = objectives + self.engine.prior_dist_weight * self.kde.score_samples(samples_array)
            self.engine.update(dict_norm, objectives, validity)

    def reset_states(self):
        super().reset_states()
        self.kde = None

    def __custom_kernel_density_sample(self, n_samples=1, seed: int = RANDOM_SEED_SAMPLING):
        """
        Custom sample method for KernelDensity. The implementation from sklearn samples randomly
        and does not provide the option to sample e.g. with Sobol, LHC or Bayes.

        Generate random samples from the model.
        Currently, this is implemented only for gaussian and tophat kernels.

        Parameters
        ----------
        engine : SamplingEngine
            The engine to use for sampling the points on the range [0, 1]
        n_samples : int, optional, default=1
            Number of samples to generate.
        seed : int, optional, default=RANDOM_SEED_SAMPLING
            Determines random number generation used to generate
            random samples. Pass an int for reproducible results
            across multiple function calls.

        Returns
        -------
        array-like of shape (n_samples, n_features)
            List of samples.
        """
        if self.kde.kernel not in ["gaussian", "tophat"]:
            raise NotImplementedError()

        data = np.asarray(self.kde.tree_.data)

        rng = check_random_state(self.seed)

        # instead of uniformly sampling the points from data, we include the sampling engine here
        # u = rng.uniform(0, 1, size=n_samples)
        u = self.engine.sample(n_samples)[:, 0]

        if self.kde.tree_.sample_weight is None:
            i = (u * data.shape[0]).astype(np.int64)
        else:
            cumsum_weight = np.cumsum(np.asarray(self.kde.tree_.sample_weight))
            sum_weight = cumsum_weight[-1]
            i = np.searchsorted(cumsum_weight, u * sum_weight)
        i[i >= len(data)] = len(data) - 1

        if self.kde.kernel == "gaussian":
            return np.atleast_2d(rng.normal(data[i], self.kde.bandwidth))

        elif self.kde.kernel == "tophat":
            # we first draw points from a d-dimensional normal distribution,
            # then use an incomplete gamma function to map them to a uniform
            # d-dimensional tophat distribution.
            dim = data.shape[1]
            X = rng.normal(size=(n_samples, dim))
            s_sq = row_norms(X, squared=True)
            correction = gammainc(0.5 * dim, 0.5 * s_sq) ** (1.0 / dim) * self.kde.bandwidth / np.sqrt(s_sq)
            return data[i] + X * correction[:, np.newaxis]


def convert_to_numpy_dict(input_dict: Dict[str, Union[np.ndarray, pd.DataFrame, torch.Tensor]]) -> Dict[str, np.ndarray]:
    """Convert elements in the dictionary to numpy.ndarray."""
    output_dict = {}
    for key, value in input_dict.items():
        if isinstance(value, np.ndarray):
            output_dict[key] = value
        elif isinstance(value, pd.DataFrame):
            output_dict[key] = value.to_numpy()
        elif isinstance(value, torch.Tensor):
            output_dict[key] = value.numpy()
        else:
            raise ValueError("Value should be either numpy.ndarray, pandas.DataFrame, or torch.Tensor")
    return output_dict
