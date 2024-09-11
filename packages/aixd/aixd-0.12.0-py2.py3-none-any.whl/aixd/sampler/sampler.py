import time
from typing import Dict, List, Union

import numpy as np
import pandas as pd
import torch

import aixd.data.constants as constants
from aixd.data.custom_callbacks import SamplingCallback
from aixd.sampler.operators import And, Boolean, Equal, GreaterOrEqual, LessOrEqual, Operator, Or
from aixd.sampler.strategies import Strategy
from aixd.utils import logs

dp_long = constants.design_par_long

logger = logs.get_logger().get_child("samples-generator")


class SamplesGenerator:
    """
    Samples values according to certain strategies and by, optionally, optimising objectives and respecting conditions.
    The strategies define how samples for each of the features are generated, the objectives inform the underlying engines (like Bayesian Optimization)
    and the conditions define which samples to keep and which to discard.

    Parameters
    ----------
    strategies : List[Strategy]
        List of strategies to be used for sampling.
    objective : Operator, optional, default=None
        Objective to be optimised. The sampler is trained using the objective values of the samples, in order
        to optimize future sampling campaigns,
    condition : Boolean, optional, default=None
        Condition that the samples should satisfy. This does not affect the sampling process, but only the samples
        that satisfy the condition are returned.
    callbacks_class : SamplingCallback, optional, default=None
        In case we want to run some function on the samples obtained in the sampling process.
        This is intended for advanced usage.
    """

    def __init__(self, strategies: List[Strategy], objective: Operator = None, condition: Boolean = None, callbacks_class: SamplingCallback = None):
        self.strategies = strategies
        self.objective = objective
        self.condition = condition
        self.callbacks_class = callbacks_class

        feature_names_with_strategy = []
        columns_features = []
        for strategy in strategies:
            for feature in strategy.features:
                if feature.name in feature_names_with_strategy:
                    logger.warning(f"Several strategies were defined for feature {feature}. Only the last one will be used.")
                else:
                    feature_names_with_strategy.append(feature.name)
                    columns_features.extend(feature.columns_df)
        self.feature_names_with_strategy = feature_names_with_strategy
        self.columns_features = columns_features

    def fit(self, data: Union[pd.DataFrame, np.ndarray, Dict[str, Union[pd.DataFrame, torch.Tensor, np.array]]]):
        """
        Initialises strategies and engines that sample according to some prior distribution. These
        strategies are also fit to the provided data.

        Parameters
        ----------
        data : Union[pd.DataFrame, np.ndarray, Dict[str, Union[pd.DataFrame, torch.Tensor, np.array]]]
            Data to fit the strategies to.
        """
        if isinstance(data, pd.DataFrame):
            data = self._convert_pd_to_dict(data)
        elif isinstance(data, np.ndarray):
            data = self._convert_array_to_dict(data)

        num_samples = len(data[list(data.keys())[0]])

        valid = self.condition.evaluate(data).flatten() if self.condition is not None else np.ones(num_samples).astype(bool)
        performance = self.objective.evaluate(data).flatten() if self.objective is not None else np.zeros(num_samples)

        for strategy in self.strategies:
            strategy.fit(data, performance, valid)

    def generate(
        self,
        n: int,
        pool_size: int = None,
        iterations: int = 10,
        verbose: bool = True,
        output_type: str = "df",
        flag_bound_to_range: bool = False,
        over_generation: int = 10,
        max_it: int = 1000,
    ) -> Union[pd.DataFrame, Dict[str, np.array], np.array]:
        """
        Generates n samples in `iterations` number of iterations and in batches of `pool_size` per iteration.
        Creates a hashmap with collision, where the keys are the performance on the objective (or zero, if no objective)
        and the values are lists of points that evaluate to this performance. Not that only valid points
        (according to the conditions) are added to the hashmap.
        Keeps iterating for `iterations` number of iterations or until at least `n` valid points are in the hashmap.

        Parameters
        ----------
        n : int
            Number of valid points that should be generated
        pool_size : int, optional, default=None
            Number of points to be generated at each iteration.
            Allows to generate much more than `n` points, f.ex. when the conditions are strict and most generated points
            are expected to be invalid. Or generate less points than `n`, f.ex. when bayesian optimization is used and generating
            many points at once is not desirable. Defaults to None, in which case it is set to `n`.
        iterations : int, optional, default=1
            The number of iterations to be performed. If no objectives are defined, this is set to 1 and the loop simply
            iterates until `n` valid points were found. If objectives are defined, `iteration` number of iterations will be
            performed, even if the hashmap already contains `n` valid samples, in which case the worst performing samples in
            the hashmap are replaced by better performing samples generated in the current iteration.
            Defaults to 1.
        verbose : bool, optional, default=True
            Whether to show information about the generation process, number of samples generated per iteration and execution times.
        output_type : str, optional, default='df'
            Type that the output should have. Can be one of {'df' (returns pd.DataFrame), 'dict' (returns a dict of numpy arrays),
            'numpy' (returns concatenated numpy array)}.
        flag_bound_to_range : bool, optional, default=False
            In case we are sampling design parameters, if we want to restrict the sampled values to domains specified by the
            data objects
        over_generation : int, optional, default=10
            If `pool_size` is None, then it is initialized to `n` * `over_generation`. This parameter controls how many
            additional samples are generated in each iteration, in order to compensate for the fact that many of them
            can be discarded due to the conditions, or perform poorly on the objectives.
        max_it : int, optional, default=1000
            Breaking condition for the loop, in case we never achieve `n` valid samples.

        Returns
        -------
        Union[pd.DataFrame, Dict[str, np.array], np.array]
            Samples generated according to the strategies, objectives and conditions.
        """
        # initialise hashmap
        valid_samples = {}
        samples_added = 0
        start_time = time.time()

        if self.objective is None:
            # if no objectives are specified, number of iterations is set to 1
            # and the loop continues until `n` valid points were found.
            iterations = 1

        if pool_size is None:
            pool_size = n * over_generation

        i = 1
        while samples_added < n or i <= iterations:
            iteration_start_time = time.time()

            new_samples_dict = {}
            # start new sampling round from strategies
            for feature_sample in [strategy.sample(pool_size) for strategy in self.strategies]:
                new_samples_dict.update(feature_sample)

            if flag_bound_to_range:
                self.condition = self._create_conditions_to_range()

            # evaluate samples on conditions and objectives
            new_samples_array = np.concatenate(list(new_samples_dict.values()), axis=-1, dtype=object)
            valid = self.condition.evaluate(new_samples_dict)[:, 0] if self.condition is not None else np.ones(len(new_samples_array)).astype(bool)
            performance = self.objective.evaluate(new_samples_dict)[:, 0] if self.objective is not None else np.zeros(len(new_samples_array))

            if self.callbacks_class is not None:
                # TODO for the moment, the values of performance and valid are being reset at the function if not
                # provided as outputs of the custom sampling
                # The data is converted to DataFrame, as this is what we expect the custom sampling to use
                pd_aux = pd.DataFrame.from_dict(new_samples_array)
                pd_aux.columns = self.columns_features
                new_samples, performance, valid = self.callbacks_class.run(input=pd_aux, performance=performance, valid=valid)
                df_aux = pd.DataFrame(new_samples[dp_long], columns=self.columns_features)
                new_samples_dict = self._convert_pd_to_dict(df_aux)
                new_samples_array = np.concatenate(list(new_samples_dict.values()), axis=-1, dtype=object)

            # update strategies with generated samples and corresponding conditions and objectives
            if self.condition is not None or self.objective is not None:
                for strategy in self.strategies:
                    strategy.update({f.name: new_samples_dict[f.name] for f in strategy.features}, performance, valid)

            # get the performance of the worst performing sample in the hashmap
            min_valid_sample = min(valid_samples.keys()) if len(valid_samples) > 0 else -1e12

            # keep only valid samples and samples that performed better than the worst performing sample in the hashmap
            valid_objectives = performance[valid][(len(valid_samples) < n) | (performance[valid] >= min_valid_sample)]
            valid_new_samples = new_samples_array[valid][(len(valid_samples) < n) | (performance[valid] >= min_valid_sample)]

            # sort samples according to their objective, in descending order
            sorted_ixs = np.argsort(valid_objectives)[::-1]
            valid_objectives = valid_objectives[sorted_ixs]
            valid_new_samples = valid_new_samples[sorted_ixs]

            # This step only makes sense in a Bayesian Optimization setting, where we would to get as close as possible
            # to some objective. Hence, only to be used with objectives.
            # Actually, this is the most consuming step, as we go one by one on the newly created samples
            j = 0
            if self.objective is not None:
                while j < len(valid_objectives) and (samples_added < n or min_valid_sample < valid_objectives[j]):
                    # if maximum number of samples has been generated, start replacing samples in the hashmap
                    if samples_added >= n and min_valid_sample < valid_objectives[j]:
                        min_valid_sample = min(valid_samples.keys())
                        if len(valid_samples[min_valid_sample]) == 1:
                            # if there is only one sample with this performance in the hashmap,
                            # delete it including the collision list
                            valid_samples.pop(min_valid_sample)
                        else:
                            # if there are several samples with this performance in the hashmap,
                            # delete one element from the collision list
                            valid_samples[min_valid_sample] = valid_samples[min_valid_sample][:-1]
                        min_valid_sample = min(valid_samples.keys())
                        samples_added -= 1

                    if valid_objectives[j] in valid_samples:
                        # if there are other samples with this performance in the hashmap,
                        # add element to collision list
                        valid_samples[valid_objectives[j]].append(valid_new_samples[j])
                    else:
                        # if there are no other samples with this performance in the hashmap,
                        # add new collision list
                        valid_samples[valid_objectives[j]] = [valid_new_samples[j]]
                    samples_added += 1
                    j += 1
            else:
                samples_added += len(valid_objectives)
                if 0.0 not in valid_samples.keys():
                    valid_samples[0.0] = []
                valid_samples[0.0].extend(valid_new_samples)

            if verbose and len(valid_samples.keys()):
                # placeholder for progress bar
                pass

            if len(valid_samples.keys()):
                elapsed = int(time.time() - start_time)
                hours, remainder = divmod(elapsed, 3600)
                minutes, seconds = divmod(remainder, 60)
                formatted_time = "{:02}:{:02}:{:02}".format(hours, minutes, seconds)
                iteration_elapsed = time.time() - iteration_start_time

                logger.debug(
                    f"Iteration {i}: {samples_added} valid samples so far."
                    + "Objective: max: {:<.3e}, min: {:<.3e}".format(max(valid_samples.keys()), min(valid_samples.keys()))
                    + "- Iter. time: {:.2f} s.".format(iteration_elapsed)
                    + f"Total time: {formatted_time}"
                )

            i += 1
            if i > max_it:
                break

        output_samples = []
        for samples in valid_samples.values():
            output_samples += samples

        if not len(output_samples):
            return []

        output_samples = np.array(output_samples)[np.random.permutation(len(output_samples))][:n]

        output_dict = self._convert_array_to_dict(output_samples)

        if output_type == "numpy":
            df_array = np.concatenate(list(output_dict.values()), axis=-1, dtype=object)
            return df_array
        if output_type == "dict":
            return {k: v.reshape(len(v), -1) for k, v in output_dict.items()}
        else:
            df_array = np.concatenate(list(output_dict.values()), axis=-1, dtype=object)
            return pd.DataFrame(df_array, columns=self.columns_features)

    def reset_states(self):
        """Resetting the states of the strategies"""
        for strategy in self.strategies:
            strategy.reset_states()

    def _create_conditions_to_range(self):
        """Provide a condition instance using the intervals of the features"""
        vec_conds = []
        for strategy in self.strategies:
            for feature in strategy.features:
                if feature.domain.domain_type == "Interval":
                    vec_conds.append(self._condition_range(feature.name, feature.domain.min_value, feature.domain.max_value))
                elif feature.domain.domain_type == "Options":
                    vec_conds.append(self._condition_options(feature.name, feature.domain.array))
        return And(*vec_conds)

    @staticmethod
    def _condition_range(name, min, max):
        """Condition for a feature to be in a range"""
        return And(LessOrEqual(name, max), GreaterOrEqual(name, min))

    @staticmethod
    def _condition_options(name, values):
        """Condition for a feature to be in a list of values"""
        vec_conds = []
        for val in values:
            if not isinstance(val, str):
                val = float(val)
            vec_conds.append(Equal(name, val))
        return Or(*vec_conds)

    def _convert_pd_to_dict(self, df):
        """Converts a dataframe to a dictionary of numpy arrays"""
        output_dict = {}
        for strategy in self.strategies:
            for feature in strategy.features:
                output_dict[feature.name] = np.asarray(df[feature.columns_df]).reshape(-1, len(feature.columns_df))
        return output_dict

    def _convert_array_to_dict(self, array):
        """Converts a dataframe to a dictionary of numpy arrays"""
        output_dict = {}
        features_count = 0
        for strategy in self.strategies:
            for feature in strategy.features:
                output_dict[feature.name] = array[:, features_count : (features_count + feature.dim)]
                features_count += feature.dim
        return output_dict
