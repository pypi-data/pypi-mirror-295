from __future__ import annotations

from typing import Dict, Tuple, Union

import numpy as np
import pandas as pd
import torch

from aixd.data.data_objects import DataObject


class Operator:
    """
    A base class for defining arithmetic and boolean operations on objects that do not yet contain actual data.
    The operations are executed only when the `evaluate` method is called with data.

    Raises:
    ValueError: If an argument is not of type float, int, str, Operator, or DataObject.

    Parameters
    ----------
    *args : list of float, int, str, Operator, or DataObject.
        The arguments to initialize the operator.
    """

    def __init__(self, *args):
        self.args = []
        for arg in args:
            if arg is None:
                continue
            elif isinstance(arg, Operator):
                self.args.append(arg)
            elif isinstance(arg, (float, int)):
                self.args.append(Constant(arg))
            elif isinstance(arg, str):
                self.args.append(arg)
            elif isinstance(arg, DataObject):
                self.args.append(arg.name)
            else:
                raise ValueError(f"Only args of type Operator, float, int or str are allowed, but type was {arg.__class__}.")

    def is_differentiable(self):
        """Check if the operator is differentiable."""
        raise NotImplementedError()

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]) -> Union[np.array, torch.Tensor]:
        """
        Evaluate the operator with given data.

        Parameters
        ----------
        data : pd.DataFrame or Dict[str, Union[torch.Tensor, np.array]]
            The data to evaluate the operator with.

        Returns
        -------
        Tuple[np.array, torch.Tensor]
            The result of the evaluation.
        """
        raise NotImplementedError()

    def print_all(self):
        """Print the operator and all its arguments."""
        vec_str = self._print_rec(self.args)
        vec_str = self._join_it(vec_str)
        print(vec_str.replace(", (", "(")[1:-1])

    @staticmethod
    def _join_it(vec_str):
        str_join = []
        for el in vec_str:
            if isinstance(el, list):
                str_join.append(Operator._join_it(el))
            else:
                str_join.append(str(el))
        return "(" + ", ".join(str_join) + ")"

    @staticmethod
    def _print_rec(args_p):
        vec_str = []
        for arg in args_p:
            if isinstance(arg, Constant):
                vec_str.append(arg.value)
            elif isinstance(arg, Operator):
                vec_str.append(arg.__class__.__name__)
                vec_str.append(Operator._print_rec(arg.args))
            elif isinstance(arg, str):
                vec_str.append(arg)
            elif isinstance(arg, DataObject):
                vec_str.append(arg.name)
        return vec_str


class Arithmetic(Operator):
    """
    A base class for defining arithmetic operations on objects that do not yet contain actual data.
    The operations are executed only when the `evaluate` method is called with data.

    Raises:
    ValueError: If an argument is not of type float, int, str, Operator, or DataObject.

    Parameters
    ----------
    *args : list of float, int, str, Operator, or DataObject.
        The arguments to initialize the operator.
    """

    def __init__(self, *args: Arithmetic):
        super().__init__(*args)

    def is_differentiable(self):
        for arg in self.args:
            if isinstance(arg, Operator) and not arg.is_differentiable():
                return False
        return True


class Boolean(Operator):
    """
    A base class for defining boolean operations on objects that do not yet contain actual data.
    The operations are executed only when the `evaluate` method is called with data.

    Raises:
    ValueError: If an argument is not of type float, int, str, Operator, or DataObject.

    Parameters
    ----------
    *args : list of float, int, str, Operator, or DataObject.
        The arguments to initialize the operator.
    """

    def __init__(self, *args: Arithmetic):
        super().__init__(*args)

    def is_differentiable(self):
        return False


class Constant(Operator):
    """
    Trivial operator, just returning the stored value.

    Parameters
    ----------
    valie : of an type, to be set as constant to for example evaluate an objective.
        The arguments to initialize the operator.
    """

    def __init__(self, value):
        super().__init__(None)
        self.value = value

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]) -> Union[np.array, torch.Tensor]:
        return self.value


class Add(Arithmetic):
    """
    Adding operation using operators. Only operates when the evaluate method is called.

    Raises:
    ValueError: If an argument is not of type float, int, str, Operator, or DataObject.

    Parameters
    ----------
    *args : list of float, int, str, Operator, or DataObject.
        The arguments to initialize the operator.
    """

    def __init__(self, *args: Tuple[Arithmetic]):
        super().__init__(*args)

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]) -> Union[np.array, torch.Tensor]:
        result = 0
        for arg in self.args:
            if isinstance(arg, str):
                result = result + data[arg]
            elif isinstance(arg, Operator):
                result = result + arg.evaluate(data)
        return result


class Multiply(Arithmetic):
    """
    Multiply operation using operators. Only operates when the evaluate method is called.

    Raises:
    ValueError: If an argument is not of type float, int, str, Operator, or DataObject.

    Parameters
    ----------
    *args : list of float, int, str, Operator, or DataObject.
        The arguments to initialize the operator.
    """

    def __init__(self, *args: Tuple[Arithmetic]):
        super().__init__(*args)

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]) -> Union[np.array, torch.Tensor]:
        result = 1
        for arg in self.args:
            if isinstance(arg, str):
                result = result * data[arg]
            elif isinstance(arg, Operator):
                result = result * arg.evaluate(data)
        return result


class Subtract(Arithmetic):
    """
    Substract operation using operators. Only operates when the evaluate method is called.

    Raises:
    ValueError: If an argument is not of type float, int, str, Operator, or DataObject.

    Parameters
    ----------
    *args : list of float, int, str, Operator, or DataObject.
        The arguments to initialize the operator.
    """

    def __init__(self, arg1: Arithmetic, arg2: Arithmetic):
        super().__init__(arg1, arg2)

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]) -> Union[np.array, torch.Tensor]:
        value1 = data[self.args[0]] if isinstance(self.args[0], str) else self.args[0].evaluate(data)
        value2 = data[self.args[1]] if isinstance(self.args[1], str) else self.args[1].evaluate(data)
        return value1 - value2


class Divide(Arithmetic):
    """
    Divide operation using operators. Only operates when the evaluate method is called.

    Raises:
    ValueError: If an argument is not of type float, int, str, Operator, or DataObject.

    Parameters
    ----------
    *args : list of float, int, str, Operator, or DataObject.
        The arguments to initialize the operator.
    """

    def __init__(self, arg1: Arithmetic, arg2: Arithmetic):
        super().__init__(arg1, arg2)

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]) -> Union[np.array, torch.Tensor]:
        value1 = data[self.args[0]] if isinstance(self.args[0], str) else self.args[0].evaluate(data)
        value2 = data[self.args[1]] if isinstance(self.args[1], str) else self.args[1].evaluate(data)
        return value1 / value2


class LessThan(Boolean):
    """
    Boolean less than operation. Only operates when the evaluate method is called.

    Raises:
    ValueError: If an argument is not of type float, int, str, Operator, or DataObject.

    Parameters
    ----------
    arg1 : Arithmetic operator
        First argument to compare.
    arg2 : Arithmetic operator
        Second argument to compare.
    """

    def __init__(self, arg1: Arithmetic, arg2: Arithmetic):
        super().__init__(arg1, arg2)

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]) -> Union[np.array, torch.Tensor]:
        value1 = data[self.args[0]] if isinstance(self.args[0], str) else self.args[0].evaluate(data)
        value2 = data[self.args[1]] if isinstance(self.args[1], str) else self.args[1].evaluate(data)
        return value1 < value2


class LessOrEqual(Boolean):
    """
    Boolean less or equal operation. Only operates when the evaluate method is called.

    Raises:
    ValueError: If an argument is not of type float, int, str, Operator, or DataObject.

    Parameters
    ----------
    arg1 : Arithmetic operator
        First argument to compare.
    arg2 : Arithmetic operator
        Second argument to compare.
    """

    def __init__(self, arg1: Arithmetic, arg2: Arithmetic):
        super().__init__(arg1, arg2)

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]) -> Union[np.array, torch.Tensor]:
        value1 = data[self.args[0]] if isinstance(self.args[0], str) else self.args[0].evaluate(data)
        value2 = data[self.args[1]] if isinstance(self.args[1], str) else self.args[1].evaluate(data)
        return value1 <= value2


class GreaterThan(Boolean):
    """
    Boolean greater than operation. Only operates when the evaluate method is called.

    Raises:
    ValueError: If an argument is not of type float, int, str, Operator, or DataObject.

    Parameters
    ----------
    arg1 : Arithmetic operator
        First argument to compare.
    arg2 : Arithmetic operator
        Second argument to compare.
    """

    def __init__(self, arg1: Arithmetic, arg2: Arithmetic):
        super().__init__(arg1, arg2)

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]) -> Union[np.array, torch.Tensor]:
        value1 = data[self.args[0]] if isinstance(self.args[0], str) else self.args[0].evaluate(data)
        value2 = data[self.args[1]] if isinstance(self.args[1], str) else self.args[1].evaluate(data)
        return value1 > value2


class GreaterOrEqual(Boolean):
    """
    Boolean greater or equal operation. Only operates when the evaluate method is called.

    Raises:
    ValueError: If an argument is not of type float, int, str, Operator, or DataObject.

    Parameters
    ----------
    arg1 : Arithmetic operator
        First argument to compare.
    arg2 : Arithmetic operator
        Second argument to compare.
    """

    def __init__(self, arg1: Arithmetic, arg2: Arithmetic):
        super().__init__(arg1, arg2)

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]) -> Union[np.array, torch.Tensor]:
        value1 = data[self.args[0]] if isinstance(self.args[0], str) else self.args[0].evaluate(data)
        value2 = data[self.args[1]] if isinstance(self.args[1], str) else self.args[1].evaluate(data)
        return value1 >= value2


class Log(Arithmetic):
    """
    Log operation. Only operates when the evaluate method is called.

    Parameters
    ----------
    arg1 : Arithmetic operator
        Value to operate on.
    """

    def __init__(self, arg1: Arithmetic):
        super().__init__(arg1)

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]) -> Union[np.array, torch.Tensor]:
        value = data[self.args[0]] if isinstance(self.args[0], str) else self.args[0].evaluate(data)
        if torch.is_tensor(value):
            return torch.math.log(value)
        else:
            return np.log(value)


class Exp(Arithmetic):
    """
    Exponential operation. Only operates when the evaluate method is called.

    Parameters
    ----------
    arg1 : Arithmetic operator
        Value to operate on.
    """

    def __init__(self, arg1: Arithmetic):
        super().__init__(arg1)

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]) -> Union[np.array, torch.Tensor]:
        value = data[self.args[0]] if isinstance(self.args[0], str) else self.args[0].evaluate(data)
        if torch.is_tensor(value):
            return torch.math.exp(value)
        else:
            return np.exp(value)


class Pow(Arithmetic):
    """
    Power of base to exponent operation. Only operates when the evaluate method is called.

    Parameters
    ----------
    base : Arithmetic operator
        Value to exponentiate.
    exponent : Arithmetic operator
        Value to exponentiate.
    """

    def __init__(self, base: Operator, exponent: Operator):
        super().__init__(base, exponent)

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]) -> Union[np.array, torch.Tensor]:
        base = data[self.args[0]] if isinstance(self.args[0], str) else self.args[0].evaluate(data)
        exponent = data[self.args[1]] if isinstance(self.args[1], str) else self.args[1].evaluate(data)
        return base**exponent


class Not(Boolean):
    """
    Not boolean operation. Only operates when the evaluate method is called.

    Parameters
    ----------
    arg : Arithmetic operator
        Value to operate on.
    """

    def __init__(self, arg: Boolean):
        super().__init__(arg)

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]) -> Union[np.array, torch.Tensor]:
        return ~(data[self.args[0]] if isinstance(self.args[0], str) else self.args[0].evaluate(data))


class And(Boolean):
    """
    And boolean operation. Only operates when the evaluate method is called.

    Parameters
    ----------
    *args : list of float, int, str, Operator, or DataObject.
        List of value to operate on iteratively.
    """

    def __init__(self, *args: Tuple[Boolean]):
        super().__init__(*args)

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]) -> Union[np.array, torch.Tensor]:
        value = data[self.args[0]] if isinstance(self.args[0], str) else self.args[0].evaluate(data)
        for arg in self.args[1:]:
            value = value & (data[arg] if isinstance(arg, str) else arg.evaluate(data))
        return value


class Or(Boolean):
    """
    Or boolean operation. Only operates when the evaluate method is called.

    Parameters
    ----------
    *args : list of float, int, str, Operator, or DataObject.
        List of value to operate on iteratively.
    """

    def __init__(self, *args: Tuple[Boolean]):
        super().__init__(*args)

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]) -> Union[np.array, torch.Tensor]:
        value = data[self.args[0]] if isinstance(self.args[0], str) else self.args[0].evaluate(data)
        for arg in self.args[1:]:
            value = value | (data[arg] if isinstance(arg, str) else arg.evaluate(data))
        return value


class XOr(Boolean):
    """
    Xor boolean operation. Only operates when the evaluate method is called.

    Parameters
    ----------
    *args : list of float, int, str, Operator, or DataObject.
        List of value to operate on iteratively.
    """

    def __init__(self, *args: Tuple[Boolean]):
        super().__init__(*args)

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]) -> Union[np.array, torch.Tensor]:
        value = data[self.args[0]] if isinstance(self.args[0], str) else self.args[0].evaluate(data)
        for arg in self.args[1:]:
            value = value ^ (data[arg] if isinstance(arg, str) else arg.evaluate(data))
        return value


class Equal(Boolean):
    """
    Equal boolean operation. Only operates when the evaluate method is called.

    Parameters
    ----------
    *args : list of float, int, str, Operator, or DataObject.
        List of value to operate on iteratively.
    """

    def __init__(self, *args: Tuple[Operator]):
        super().__init__(*args)

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]) -> Union[np.array, torch.Tensor]:
        value = data[self.args[0]] if isinstance(self.args[0], str) else self.args[0].evaluate(data)
        for arg in self.args[1:]:
            value = value == (arg.evaluate(data) if isinstance(arg, Operator) else arg)
        return value


class Negative(Arithmetic):
    """
    Negation operation. Only operates when the evaluate method is called.

    Parameters
    ----------
    arg1 : Arithmetic operator
        Operator to negate.
    """

    def __init__(self, arg1: Arithmetic):
        super().__init__(arg1)

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]) -> Union[np.array, torch.Tensor]:
        value = data[self.args[0]] if isinstance(self.args[0], str) else self.args[0].evaluate(data)
        return -value


class CastBooleanToConstant(Arithmetic):
    """
    Type casting operation. Only operates when the evaluate method is called.

    Parameters
    ----------
    arg1 : Boolean Arithmetic operator
        Operator to cast.
    """

    def __init__(self, arg1: Boolean):
        super().__init__(arg1)

    def is_differentiable(self):
        return False

    def evaluate(self, data: Union[pd.DataFrame, Dict[str, Union[torch.Tensor, np.array]]]) -> Union[np.array, torch.Tensor]:
        value = self.args[0].evaluate(data)
        if torch.is_tensor(value):
            return value.float()
        else:
            return value.astype(float)
