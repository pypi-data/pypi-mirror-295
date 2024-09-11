from typing import Dict, Union

import numpy as np
import pandas as pd
import torch

from aixd.sampler.operators import Arithmetic, Boolean, Operator


class Reducer:
    """
    Perform agregation operations on the output of an operator.

    Parameters
    ----------
    operator : Operator
        The operator to perform the aggregation on.
    """

    def __init__(self, operator: Operator):
        self.operator = operator

    def is_differentiable(self):
        """Check if the operator is differentiable."""
        return self.operator.is_differentiable()

    def evaluate(self, data: pd.DataFrame):
        """
        Evaluate the operator with given data.

        Parameters
        ----------
        data : pd.DataFrame
            The data to evaluate the operator with.

        Returns
        -------
        Tuple[np.array, torch.Tensor]
            The result of the evaluation.
        """
        raise NotImplementedError()


class Sum(Reducer):
    """
    Add up all the values of the operator.

    Parameters
    ----------
    operator : Operator
        The operator to perform the aggregation on.
    """

    def __init__(self, operator: Arithmetic):
        super().__init__(operator)

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]):
        return self.operator.evaluate(data).sum(axis=0, keepdims=True)


class Mean(Reducer):
    """
    Mean of values of the operator.

    Parameters
    ----------
    operator : Operator
        The operator to perform the aggregation on.
    """

    def __init__(self, operator: Arithmetic):
        super().__init__(operator)

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]):
        return self.operator.evaluate(data).mean(axis=0, keepdims=True)


class Std(Reducer):
    """
    Standard deviation of values of the operator.

    Parameters
    ----------
    operator : Operator
        The operator to perform the aggregation on.
    """

    def __init__(self, operator: Arithmetic):
        super().__init__(operator)

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]):
        return self.operator.evaluate(data).std(axis=0, keepdims=True)


class Var(Reducer):
    """
    Variance of the values of the operator.

    Parameters
    ----------
    operator : Operator
        The operator to perform the aggregation on.
    """

    def __init__(self, operator: Arithmetic):
        super().__init__(operator)

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]):
        return self.operator.evaluate(data).var(axis=0, keepdims=True)


class All(Reducer):
    """
    Check if condition is true for all values of the operator.

    Parameters
    ----------
    operator : Operator
        The operator to perform the aggregation on.
    """

    def __init__(self, operator: Boolean, use_torch: bool = False):
        super().__init__(operator)
        self.use_torch = use_torch

    def is_differentiable(self):
        return False

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]):
        return self.operator.evaluate(data).all(axis=0, keepdims=True)


class Any(Reducer):
    """
    Check if condition is satisfied for any value of the operator.

    Parameters
    ----------
    operator : Operator
        The operator to perform the aggregation on.
    """

    def __init__(self, operator: Boolean, use_torch: bool = False):
        super().__init__(operator)
        self.use_torch = use_torch

    def is_differentiable(self):
        return False

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]):
        return self.operator.evaluate(data).any(axis=0, keepdims=True)
