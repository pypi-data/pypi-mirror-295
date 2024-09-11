"""
Classes for all different callbacks we need to provide. These classes will just ensure
that the data is passed correctly to the Dataset instance, checking for:

    - Correct formatting into numpy array
    - Non existence of uid (up to some extent)
    - Existence of error columns

How the data is passed to these callbacks, it is:

    - Class for import data: no input data, just specifications of shards, in case we want to
split the import

    - Class for sampling and analysis: we provide as input a dataframe, and output a numpy array
      For the design parameters and design representations, the output just contain the features
      For the performance attributes, it also contains a column at the end with errors on the calculations
"""

from typing import TYPE_CHECKING, Callable, List, Union

import numpy as np
import pandas as pd

import aixd.data.constants as constants
from aixd.data.utils_data import convert_to
from aixd.utils import logs

DP_LONG = constants.design_par_long
PA_LONG = constants.perf_attribute_long
DR_LONG = constants.design_rep_long
FORMATS_IO = constants.formats_io

if TYPE_CHECKING:
    from aixd.data.dataset import Dataset

logger = logs.get_logger().get_child("callbacks")


class CustomCallback:
    def __init__(self, name: str, func_callback: Union[Callable, List[Callable]], dataset: "Dataset" = None):
        self.name = name
        if dataset is not None:
            self.datapath = dataset.datapath
            self.design_par = dataset.design_par
            self.perf_attributes = dataset.perf_attributes
            self.design_rep = dataset.design_rep
            self.names_design_rep = list(dataset.design_rep.keys())
        else:
            logger.warning("Please provide a valid dataset instance")

        self.func_callback = func_callback if isinstance(func_callback, list) else [func_callback]

    def run(self, **kwargs):
        """
        This function will run the callback functions.

        Parameters:
        ----------
        **kwargs
            A dictionary containing the keyword arguments to pass to all the callback functions.
        """
        flag_check = True
        if "flag_check" in kwargs.keys():
            flag_check = kwargs["flag_check"]
            kwargs.pop("flag_check")
        if (self.design_par is not None) and (self.perf_attributes is not None):
            for i, func in enumerate(self.func_callback):
                if not i:
                    if "input" in kwargs.keys():
                        in_data = kwargs["input"]
                        kwargs.pop("input")
                        ddata = func(in_data, **kwargs)
                    else:
                        ddata = func(**kwargs)
                    if ddata is None:
                        raise ValueError("Import error: something went wrong when running the functions")
                else:
                    ddata = func(ddata, **kwargs)
            if flag_check:
                return self._check(ddata)
            else:
                return ddata
        else:
            raise ValueError("Callback error: incorrect definition of data blocks")

    def _check(self, ddata):
        """Function to overwrite in the child classes, for checking the data."""
        return ddata

    def _check_mat_dp(self, mat):
        """Check the data matrix for the design parameters."""
        cols_dp = self.design_par.columns_df
        mat = self._check_remove_uids(mat, cols_dp)
        # After checking if the first contains uids
        if mat.shape[1] > (len(cols_dp) - 1):
            mat = mat[:, : len(cols_dp)]
            logger.info("Truncating last columns")
        return mat

    def _check_mat_pa(self, mat):
        """Check the data matrix for the performance attributes."""
        cols_pa = self.perf_attributes.columns_df  # ["uid"] + [...] + ["error"]

        # Remove the uid, if present
        mat = self._check_remove_uids(mat, cols_pa)

        # We allow for a missing error column, and for more columns than required. No uid column is required.
        if mat.shape[1] < len(cols_pa) - 2:
            raise Exception("To few columns. The data does not match the defined performance attributes.")
        elif mat.shape[1] > len(cols_pa) - 1:
            # Truncate additional columns
            mat = mat[:, : (len(cols_pa) - 1)]
            logger.info("The number of columns in the original matrix has been truncated")
        else:
            pass
            # mat.shape[1] == len(cols_pa) - 2 or mat.shape[1] == len(cols_pa) - 1

        # Check the error column, if not present we add one
        if mat.shape[1] == len(cols_pa) - 1:
            if self._check_if_colerrors(mat[:, -1].flatten()):
                logger.info("Error column found")
            else:
                raise Exception("The last column is not an error column.")
        elif mat.shape[1] == len(cols_pa) - 2:
            mat = np.concatenate([mat, np.zeros((mat.shape[0], 1))], axis=1)
            logger.warning("Error column not found. Adding an all zero to the end")

        return mat

    def _check_mat_dr(self, mat, key):
        """Check the data matrix for the design representation."""
        cols_dr = self.design_rep[key].columns_df
        mat = self._check_remove_uids(mat, cols_dr)
        dim_tot = (len(cols_dr) - 1) if len(cols_dr) else self.design_rep[key].dim
        # After checking if the first contains uids
        if mat.shape[1] > dim_tot:
            mat = mat[:, :dim_tot]
            logger.info("Truncating last columns")
        return mat

    def _check_remove_uids(self, mat, cols_block):
        cols_df = mat.columns if isinstance(mat, pd.DataFrame) else None
        if cols_df is not None:
            if "uid" in cols_df:
                mat = mat.drop(columns=["uid"])
        mat = self.to_numpy(mat)
        # Checking col uids
        # -1 for the uid col
        if mat.shape[1] > (len(cols_block) - 1):
            if self._check_if_coluids(mat[:, 0].flatten()):
                mat = mat[:, 1:]
                logger.info("Removing first column as it contains uids")
        return mat

    @staticmethod
    def _check_if_coluids(vec):
        """Heuristic to check if the column is a uid column by checking if it is monotonically increasing."""
        if vec.size < 2:
            return True  # An empty or single-element array is considered monotonically increasing

        return np.all(vec[:-1] == vec[1:] + 1)

    @staticmethod
    def _check_if_colerrors(vec: np.ndarray):
        try:
            """Heuristic to check if the column is an error column by checking if it contains only 0 and 1."""
            return np.all((vec.astype(int) == 0) | (vec.astype(int) == 1))
        except (TypeError, OverflowError, ValueError):
            # In case the int conversion fails
            return False

    @staticmethod
    def to_numpy(mat):
        if isinstance(mat, np.ndarray):
            return mat
        else:
            return np.asarray(mat)


"""
IMPORTER CALLBACK: to consider
- No need to incorporate in the first column any uids
- The format to return is numpy array
- The last column of the performance attributes should incorporate the errors on
    the computation of perf. attributes
- We return a dict
    return {DP_LONG : mat_dp_all, PA_LONG : mat_pa_all, DR_LONG : {'image_600' : mat_dr_all}}

"""


class ImportCallback(CustomCallback):
    def __init__(self, name: str, func_callback: Union[Callable, List[Callable]], dataset: "Dataset" = None):
        self.type = "import"
        super().__init__(name, func_callback, dataset)

    def run(self, vec_shards=[0, 1], **kwargs):
        return super().run(vec_shards=vec_shards, **kwargs)

    def _check(self, ddata):
        """
        Needs to ensure:
        - We send a dict, with at least design parameters and performance attributes
        - These are numpy arrays, without uid for samples, and with column of errors for the perf. att.
        - The design representation is a dict of dicts
        """
        if isinstance(ddata, dict):
            if (DP_LONG in ddata.keys()) and (PA_LONG in ddata.keys()):
                if DR_LONG in ddata.keys():
                    if isinstance(ddata[DR_LONG], dict):
                        return self._data_check(ddata)
                    elif isinstance(ddata[DR_LONG], list):
                        dict_aux = dict()
                        names_dr = self.names_design_rep + [DR_LONG + str(o) for o in range(len(self.names_design_rep), len(ddata[DR_LONG]))]
                        for i, d_extra in enumerate(ddata[DR_LONG]):
                            dict_aux[names_dr[i]] = d_extra
                        ddata[DR_LONG] = dict_aux
                        return self._data_check(ddata)
                    else:
                        raise ValueError("Import error: design representation wrongly provided")
                else:
                    return self._data_check(ddata)
            else:
                raise ValueError("Import error: no correct keys on dictionary")
        elif isinstance(ddata, list):
            if len(ddata) >= 2:
                ddata_aux = {DP_LONG: ddata[0], PA_LONG: ddata[1]}
                dict_aux = dict()
                names_dr = self.names_design_rep + [DR_LONG + str(o) for o in range(len(self.names_design_rep), len(ddata) - 2)]
                for i, d_extra in enumerate(ddata[2:]):
                    dict_aux[names_dr[i]] = d_extra
                if len(dict_aux):
                    ddata_aux[DR_LONG] = dict_aux
                return self._data_check(ddata_aux)
            else:
                raise ValueError("Import error: not enough arrays to create the correct output")
        else:
            raise ValueError("Import error: only accepted outputs are dict or list or arrays")

    def _data_check(self, ddata):
        ddata[DP_LONG] = self._check_mat_dp(ddata[DP_LONG])
        ddata[PA_LONG] = self._check_mat_pa(ddata[PA_LONG])
        if DR_LONG in ddata.keys():
            for key in ddata[DR_LONG]:
                ddata[DR_LONG][key] = self._check_mat_dr(ddata[DR_LONG][key], key)
        return ddata


"""
ANALYSIS CALLBACK: to consider
- No need to incorporate in the first column any uids
- The format to return is numpy array
- The last column of the performance attributes should incorporate the errors on
    the computation of perf. attributes
"""


class AnalysisCallback(CustomCallback):
    def __init__(self, name: str, func_callback: Union[Callable, List[Callable]], dataset: "Dataset" = None, format_in: str = None):
        """
        Parameters
        ----------
        name : str
            Name of the callback.

        func_callback : Union[Callable, List[Callable]]
            Function or list of functions to run.

        dataset : Dataset
            Dataset instance.

        format_in : str, optional, default=None
            The format required by the analyzer function for the input data to use.
            Other options are: ``'dict'``, ``'dict_list'``, ``'array'``, ``'torch'``, ``'list'``,
            ``'df_per_obj'``, ``'df'``. This can be also provided when running the function.

        """
        self.format_in = format_in if format_in in FORMATS_IO else None
        self.type = "analysis"
        super().__init__(name, func_callback, dataset)

    def analyze(self, input=[], format_in: str = "df", format_out: str = "array", **kwargs):
        """
        Function for the user, to evaluate some set of design parameters using
        the Analysis function
        """
        f_in = self.format_in if self.format_in is not None else format_in
        self._check_format(f_in)
        self._check_format(format_out)
        input_data = convert_to(input, format=f_in, dataobjects=self.design_par.dobj_list)
        out_data = super().run(input=input_data, flag_check=False, **kwargs)
        return convert_to(out_data, format=format_out, dataobjects=self.perf_attributes.dobj_list)

    def run(self, input=[], format_in: str = "df", **kwargs):
        """
        This is the function used internally by the Dataset instance,
        to obtain the perf. attributes given some samples
        """
        f_in = self.format_in if self.format_in is not None else format_in
        self._check_format(f_in)
        input_data = convert_to(input, format=f_in, dataobjects=self.design_par.dobj_list)
        return super().run(input=input_data, **kwargs)

    @staticmethod
    def _check_format(fmt: str):
        if fmt not in FORMATS_IO:
            raise ValueError("The format is not valid. Valid format are: {}".format(", ".join(FORMATS_IO)))

    def _check(self, ddata):
        """
        Needs to ensure:
        - We send a dict, with performance attributes, and design representation if obtained
        - These are numpy arrays, without uid for samples, and with column of errors for the perf. att.
        - The design representation is a dict of dicts
        """
        if isinstance(ddata, dict):
            if PA_LONG in ddata.keys():
                if DR_LONG in ddata.keys():
                    if isinstance(ddata[DR_LONG], dict):
                        return self._data_check(ddata)
                    elif isinstance(ddata[DR_LONG], list):
                        dict_aux = dict()
                        names_dr = self.names_design_rep + [DR_LONG + str(o) for o in range(len(self.names_design_rep), len(ddata[DR_LONG]))]
                        for i, d_extra in enumerate(ddata[DR_LONG]):
                            dict_aux[names_dr[i]] = d_extra
                        ddata[DR_LONG] = dict_aux
                        return self._data_check(ddata)
                    else:
                        raise ValueError("Import error: design representation wrongly provided")
                else:
                    return self._data_check(ddata)
            else:
                raise ValueError("Import error: no correct keys on dictionary")
        elif isinstance(ddata, list):
            if len(ddata) >= 1:
                ddata_aux = {PA_LONG: ddata[0]}
                dict_aux = dict()
                names_dr = self.names_design_rep + [DR_LONG + str(o) for o in range(len(self.names_design_rep), len(ddata) - 1)]
                for i, d_extra in enumerate(ddata[1:]):
                    dict_aux[names_dr[i]] = d_extra
                if len(dict_aux):
                    ddata_aux[DR_LONG] = dict_aux
                return self._data_check(ddata_aux)
            else:
                raise ValueError("Import error: not enough arrays to create the correct output")
        elif isinstance(ddata, (pd.DataFrame, np.ndarray)):
            ddata_aux = {PA_LONG: ddata}
            return self._data_check(ddata_aux)
        else:
            raise ValueError("Import error: only accepted outputs are dict or list or arrays")

    def _data_check(self, ddata):
        ddata[PA_LONG] = self._check_mat_pa(ddata[PA_LONG])
        if DR_LONG in ddata.keys():
            for key in ddata[DR_LONG]:
                ddata[DR_LONG][key] = self._check_mat_dr(ddata[DR_LONG][key], key)
        return ddata


"""
SAMPLING CALLBACK: to consider
- No need to incorporate in the first column any uids
- The format to return is numpy array
"""


class SamplingCallback(CustomCallback):
    def __init__(self, name: str, func_callback: Union[Callable, List[Callable]], dataset: "Dataset" = None):
        self.type = "sampling"
        super().__init__(name, func_callback, dataset)

    def run(self, input=[], **kwargs):
        """Run the sampling callback.

        For the custom sampling we also can provide as output some
        value of performance for the acquired samples, as well as
        vector of valid or not samples. If those are not provided
        by the functions, they are just added as default values.
        The order is: ``new_samples_dict``, ``performance``, ``valid``.
        """
        if (self.design_par is not None) and (self.perf_attributes is not None):
            for i, func in enumerate(self.func_callback):
                if not i:
                    if not len(input):
                        ddata = func(**kwargs)
                    else:
                        ddata = func(input, **kwargs)
                    if ddata is None:
                        raise ValueError("Import error: something went wrong when running the functions")
                else:
                    ddata = func(ddata[0], **kwargs)
                ddata = self._ddata_as_list(input=ddata, **kwargs)
            return self._check(ddata)
        else:
            raise ValueError("Import error: incorrect definition of data blocks")

    def _ddata_as_list(self, input, **kwargs):
        if isinstance(input, list):
            len_data = len(input[0])
        else:
            len_data = len(input)
        if "performance" in kwargs.keys():
            performance = kwargs["performance"]
        else:
            performance = np.zeros(len_data)
            logger.info("The performance and validity of samples has been reset")

        valid = np.ones(len_data).astype(bool)
        if "valid" in kwargs.keys():
            valid = kwargs["valid"]
        if isinstance(input, list):
            if len(input) == 1:
                # Performance values, all equal
                input.append(performance)
            if len(input) == 2:
                input.append(valid)
            return input
        else:
            return [input, performance, valid]

    def _check(self, ddata_list):
        """
        Needs to ensure:
        - We send a dict, with design parameters
        - These are numpy arrays, without uid for samples, and with column of errors for the perf. att.
        """
        ddata = ddata_list[0]
        if isinstance(ddata, dict):
            if DP_LONG in ddata.keys():
                return self._data_check(ddata_list)
            else:
                raise ValueError("Import error: no correct keys on dictionary")
        elif isinstance(ddata, list):
            if len(ddata) == 1:
                ddata_aux = {DP_LONG: ddata[0]}
                ddata_list[0] = ddata_aux
                return self._data_check(ddata_list)
            else:
                raise ValueError("Import error: not enough arrays to create the correct output")
        elif isinstance(ddata, (pd.DataFrame, np.ndarray)):
            ddata_aux = {DP_LONG: ddata}
            ddata_list[0] = ddata_aux
            return self._data_check(ddata_list)
        else:
            raise ValueError("Import error: only accepted outputs are dict or list or arrays")

    def _data_check(self, ddata_list):
        ddata_aux = {DP_LONG: self._check_mat_dp(ddata_list[0][DP_LONG])}
        ddata_list[0] = ddata_aux
        return ddata_list


class PostGenerationCallback(CustomCallback):
    """
    Receives the output of the NN, and performs a transformation to it,
    before returning the value to the user, or before feeding it again to
    the
    """

    def __init__(self, name: str, func_callback: Union[Callable, List[Callable]], dataset: "Dataset" = None):
        self.type = "post_generation"
        super().__init__(name, func_callback, dataset)

    def run(self, input=[]):
        input = self.to_numpy(input)
        return super().run(input=input)

    def _check(self, ddata):
        """
        Needs to ensure:
        - What is received, is converted to numpy array, with n_samples x dim
        - Returns a numpy array
        """
        return self.to_numpy(ddata)


class DataloaderCallback(CustomCallback):
    """Callback for pre or post data loading transformation and normalization.

    Receives the output of the NN, and performs a transformation to it,
    before returning the value to the user, or before feeding it again to
    the
    """

    def __init__(self, name: str, func_callback: Union[Callable, List[Callable]], dataset: "Dataset" = None, **kwargs):
        self.type = "callback pre or post dataloader transformation and normalization"
        self.extra_params = kwargs
        super().__init__(name, func_callback, dataset)

    def run(self, x, y):
        if (self.design_par is not None) and (self.perf_attributes is not None):
            for i, func in enumerate(self.func_callback):
                x, y = func(x, y, **self.extra_params)
            return self._check(x), self._check(y)
        else:
            raise ValueError("Import error: incorrect definition of data blocks")

    def _check(self, ddata):
        """
        Needs to ensure:
        - What is received, is converted to numpy array, with n_samples x dim
        - Returns a numpy array
        """
        return self.to_numpy(ddata)
