import math
from typing import Dict, List, Union

import numpy as np
import torch
from bayes_opt import BayesianOptimization, UtilityFunction
from scipy.stats import qmc

from aixd.data.data_objects import DataObject
from aixd.mlmodel.utils_mlmodel import rec_concat_dict
from aixd.sampler.constants import RANDOM_SEED_SAMPLING
from aixd.utils import logs

BAYES_MAX_POINTS = 100

logger = logs.get_logger().get_child("sampling-engine")


class SamplingEngine:
    """
    Initialises the sampling engine. The features are just related to the data objects, and contain
    the information on their type, dimensionality, etc.

    Parameters
    ----------
    features : List[str]
        Names of features in the samples that should be produced
    seed : int, optional
        Seed value for reproducible results.
    """

    def __init__(self, features: List[DataObject], seed: int = RANDOM_SEED_SAMPLING):
        self.features = [f.name for f in features]
        self.dim = sum([f.dim for f in features])
        np.random.seed(seed=seed)

    def sample(self, n: int) -> np.array:
        """
        Performs the sampling.

        Parameters
        ----------
        n : int
            The number of samples to be produced.

        Returns
        ----------
        np.ndarray
            A numpy array containing the new samples, of shape (n, self.dim)
        """
        raise NotImplementedError()

    def update(self, samples: Dict[str, Union[torch.Tensor, np.array]], objectives: Union[torch.Tensor, np.array], valid: Union[torch.Tensor, np.array]) -> None:
        """
        Updates the state of the sampling methods by providing the performance of the generated samples
        in the form of `objectives` and `valid`.

        Parameters
        ----------
        samples : Dict[str, Union[torch.Tensor, np.array]]
            Points where objectives and conditions have been evaluated on.
        objectives : Union[torch.Tensor, np.array]
            The performance of the generated samples according to some objective,
            higher the better (of type float and shape (n, 1)).
        valid : Union[torch.Tensor, np.array]
            Whether the generated samples were valid or not (of type boolean and shape (n, 1))
        """
        raise NotImplementedError()

    def reset_states(self) -> None:
        """
        Resets the engine to its initial state, where all calls to `sample` and `update` are forgotten.
        """
        pass

    @staticmethod
    def deserialise(identifier: str, features: List[str], **kwargs) -> "SamplingEngine":
        """
        Allows to initialise a SamplingEngine by passing the identifier string along with with any specific arguments.
        """
        if isinstance(identifier, SamplingEngine):
            return identifier
        elif identifier == "random":
            return RandomSamplingEngine(features, **kwargs)
        elif identifier == "grid":
            return GridamplingEngine(features, **kwargs)
        elif identifier == "sobol":
            return SobolSamplingEngine(features, **kwargs)
        elif identifier in ["lhc", "latin_hypercube"]:
            return LHCSamplingEngine(features, **kwargs)
        elif identifier == "bayesian":
            return BayesOptSamplingEngine(features, **kwargs)
        else:
            raise ValueError(f'Identifier of SamplingEngine must be one of "random", "grid", "sobol", "lhc" or "bayesian", but was {identifier}.')


class AgnosticSamplingEngine(SamplingEngine):
    """
    Represents sampling procedures that do not adapt to objectives and constraints.

    Parameters
    ----------
    features : List[str]
        Names of features in the samples that should be produced
    seed : int, optional, default=42
        Seed value for reproducible results.
    """

    def __init__(self, features: List[str], seed: int = 42):
        super().__init__(features, seed)
        self.prior_dist_weight = 1

    def update(self, samples: Dict[str, Union[torch.Tensor, np.array]], objectives: Union[torch.Tensor, np.array], valid: Union[torch.Tensor, np.array]) -> None:
        pass


class AdaptiveSamplingEngine(SamplingEngine):
    """
    Represents sampling procedures that adapt to objectives and constraints.

    Parameters
    ----------
    features : List[str]
        Names of features in the samples that should be produced
    seed : int, optional, default=RANDOM_SEED_SAMPLING
        Seed value for reproducible results.
    """

    def __init__(self, features: List[str], seed: int = RANDOM_SEED_SAMPLING):
        super().__init__(features, seed)
        self.prior_dist_weight = None

    def update(self, samples: Dict[str, Union[torch.Tensor, np.array]], objectives: Union[torch.Tensor, np.array], valid: Union[torch.Tensor, np.array]) -> None:
        raise NotImplementedError()


class RandomSamplingEngine(AgnosticSamplingEngine):
    """
    Samples randomly uniform in [0, 1].

    Parameters
    ----------
    features : List[str]
        Names of features in the samples that should be produced
    seed : int, optional, default=RANDOM_SEED_SAMPLING
        Seed value for reproducible results.
    """

    def __init__(self, features: List[str], seed: int = RANDOM_SEED_SAMPLING):
        super().__init__(features, seed)

    def sample(self, n: int) -> np.array:
        return np.random.uniform(size=(n, self.dim))


class GridamplingEngine(AgnosticSamplingEngine):
    """
    Returns a grid of size n in each dimension.

    Parameters
    ----------
    features : List[str]
        Names of features in the samples that should be produced
    seed : int, optional, default=RANDOM_SEED_SAMPLING
        Seed value for reproducible results.
    """

    def __init__(self, features: List[str], seed: int = RANDOM_SEED_SAMPLING):
        super().__init__(features, seed)

    def sample(self, n: int) -> np.array:
        n_per_dim = math.ceil(n ** (1 / self.dim))
        mgrid = np.stack(np.meshgrid(*[np.linspace((0,), (1,), n_per_dim) for _ in range(self.dim)]), axis=-1).reshape(-1, self.dim)
        if len(mgrid) > n:
            logger.warning(
                f"It is not possible to create a {self.dim}D grid with a total number of {n} points. {len(mgrid) - n} points will be randomly dropped from the grid with {len(mgrid)} points."
            )
            ixs = np.arange(0, len(mgrid), step=1, dtype=int)
            np.random.shuffle(ixs)
            return mgrid[ixs][:n]
        return mgrid


class SobolSamplingEngine(AgnosticSamplingEngine):
    """
    Samples in [0, 1] according to a Sobol sequence.

    Parameters
    ----------
    features : List[str]
        Names of features in the samples that should be produced
    scramble : bool, optional, default=True
        If True, use LMS+shift scrambling. Otherwise, no scrambling is done
    seed : int, optional, default=RANDOM_SEED_SAMPLING
        Seed value for reproducible results.
    """

    def __init__(self, features: List[str], scramble: bool = True, seed: int = RANDOM_SEED_SAMPLING, **kwargs):
        super().__init__(features, seed)
        self.iteration = 0
        self.sobol = qmc.Sobol(self.dim, scramble=scramble, seed=seed)

    def sample(self, n: int) -> np.array:
        # As sobol uses power of 2
        n = 2 ** np.ceil(np.log2(n)).astype(int)
        return self.sobol.random(n)

    def reset_states(self) -> None:
        self.sobol.reset()


class LHCSamplingEngine(AgnosticSamplingEngine):
    """
    Samples in [0, 1] according to a Latin Hypercube sequence.

    Parameters
    ----------
    features : List[str]
        Names of features in the samples that should be produced
    scramble : bool, optional, default=True
        If True, use LMS+shift scrambling. Otherwise, no scrambling is done
    optimization : str, optional, default=None
        Whether to use an optimization scheme to improve the quality after sampling.
        Options are random-cd and lloyd. See https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.qmc.LatinHypercube.html
    seed : int, optional, default=RANDOM_SEED_SAMPLING
        Seed value for reproducible results.
    """

    def __init__(self, features: List[str], scramble: bool = True, optimization: str = None, seed: int = RANDOM_SEED_SAMPLING, **kwargs):
        super().__init__(features, seed)
        self.iteration = 0
        self.lhc = qmc.LatinHypercube(self.dim, scramble=scramble, optimization=optimization, seed=seed)

    def sample(self, n: int) -> np.array:
        return self.lhc.random(n)

    def reset_states(self) -> None:
        self.lhc.reset()


class BayesOptSamplingEngine(AdaptiveSamplingEngine):
    """
    Samples in [0, 1] according to a Bayesian Optimisation strategy, where the objectives are maximised.
    Based on the python bayesian-optimization package: https://github.com/fmfn/BayesianOptimization

    Parameters
    ----------
    kind: {'ucb', 'ei', 'poi'}
        * 'ucb' stands for the Upper Confidence Bounds method
        * 'ei' is the Expected Improvement method
        * 'poi' is the Probability Of Improvement criterion.
    kappa: float, optional, default=2.576
        Parameter to indicate how closed are the next parameters sampled.
        Higher value = favors spaces that are least explored.
        Lower value = favors spaces where the regression function is
        the highest.
    xi: float, optional, default=0.0
    kappa_decay: float, optional, default=1
        `kappa` is multiplied by this factor every iteration.
    kappa_decay_delay: int, optional, default=0
        Number of iterations that must have passed before applying the
        decay to `kappa`.
    prior_dist_weight: float, optional, default=0.0001
        The weight to give to the prior distribution. If higher, more weight will be put on respecting prior distribution.
        If lower, optimising the objectives is more important.
    """

    def __init__(
        self,
        features: List[str],
        kind: str = "ucb",
        kappa: float = 2.576,
        xi: float = 0.9,
        kappa_decay: float = 0.9,
        kappa_decay_delay: int = 0,
        prior_dist_weight: float = 0.01,
        seed: int = RANDOM_SEED_SAMPLING,
        **kwargs,
    ):
        super().__init__(features, seed)
        self.kind = kind
        self.kappa = kappa
        self.xi = xi
        self.kappa_decay = kappa_decay
        self.kappa_decay_delay = kappa_decay_delay
        self.prior_dist_weight = prior_dist_weight
        self.seed = seed

        self.utility = UtilityFunction(kind=kind, kappa=kappa, xi=xi, kappa_decay=kappa_decay, kappa_decay_delay=kappa_decay_delay)
        self.optimizer = BayesianOptimization(
            f=None,
            pbounds={f: (0, 1) for f in self.features},
            random_state=seed,
            allow_duplicate_points=True,
            **kwargs,
        )
        self.num_dummy_registered_points = 0

    def sample(self, n: int) -> np.array:
        if len(self.optimizer._space._params) == 0:
            suggested_points = RandomSamplingEngine(self.features, self.seed).sample(n)
            suggested_points = {f: suggested_points[:, i : i + 1] for i, f in enumerate(self.features)}
        else:
            suggested_points = []
            for _ in range(n):
                new_sample = self.optimizer.suggest(self.utility)

                closest_registered_params = np.argmin(
                    ((self.optimizer._space._params - self.optimizer._space._as_array(new_sample)) ** 2).reshape(len(self.optimizer._space._params), -1).mean(axis=-1)
                )

                suggested_points.append(new_sample)

                self.optimizer.register(params=new_sample, target=self.optimizer._space._target[closest_registered_params])

            self.num_dummy_registered_points += n

            if n > 1:
                suggested_points = rec_concat_dict(suggested_points)
            else:
                suggested_points = {k: np.array([[v]]) for k, v in suggested_points[0].items()}

        return np.concatenate(list(suggested_points.values()), axis=-1)

    def update(self, samples: Dict[str, Union[torch.Tensor, np.array]], objectives: Union[torch.Tensor, np.array], valid: Union[torch.Tensor, np.array]) -> None:
        """
        Updates the utility function by subtracting a large number from the performance of invalid samples.
        """
        if len(objectives) > BAYES_MAX_POINTS:
            logger.warning(
                f"You are attempting to register {len(objectives)} points in BayesOptEngine."
                + f" Bayesian Optimization can not cope with this number of points. Only the first {BAYES_MAX_POINTS} are used."
            )

        self.optimizer._space._params = self.optimizer._space._params[: -self.num_dummy_registered_points]
        self.optimizer._space._target = self.optimizer._space._target[: -self.num_dummy_registered_points]
        objectives = objectives - (valid.astype(float) - 1) * 1e6

        for i in range(min(len(objectives), BAYES_MAX_POINTS)):
            self.optimizer.register(
                params={f: samples[f][i] + np.random.normal(0, 1e-7) for f in self.features},  # add very small noise to avoid collisions with previously registered points
                target=objectives[i],
            )

        self.num_dummy_registered_points = 0

    def reset_states(self) -> None:
        """Reset the state of the sampler to start the Bayesian sampling from scratch"""
        self.utility = UtilityFunction(kind=self.kind, kappa=self.kappa, xi=self.xi, kappa_decay=self.kappa_decay, kappa_decay_delay=self.kappa_decay_delay)
        self.optimizer = BayesianOptimization(
            f=None,
            pbounds={f: (0, 1) for f in self.features},
            random_state=self.seed,
            allow_duplicate_points=True,
        )
