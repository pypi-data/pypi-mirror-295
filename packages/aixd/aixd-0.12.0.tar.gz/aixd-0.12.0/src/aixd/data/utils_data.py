from __future__ import annotations

import copy
import io
import json
import zipfile
from collections import defaultdict
from typing import TYPE_CHECKING, Dict, List, Union

import numpy as np
import pandas as pd
import torch

import aixd.data.constants as constants
from aixd.mlmodel.utils_mlmodel import to_numpy, to_torch
from aixd.utils.utils import flatten_dict, flatten_list

if TYPE_CHECKING:  # avoid circular imports, as the following is only used for type checking
    from aixd.data import DataBlock, DataObject


dp_long = constants.design_par_long
pa_long = constants.perf_attribute_long
dr_long = constants.design_rep_long


def save_compressed(fh, **namedict):
    with zipfile.ZipFile(fh, mode="w", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
        for k, v in namedict.items():
            buf = io.BytesIO()
            np.lib.npyio.format.write_array(buf, np.asanyarray(v), allow_pickle=False)
            zf.writestr(k + ".npy", buf.getvalue())


def check_file_ids(files_list, data_gen_dp, data_gen_pa):
    vec_ids_mismatch = dict()
    vec_ids_mismatch_uiddiff = dict()
    string_msg = "- There is no mismatch between files and stored file ids"
    error = 0
    for folder, filename in zip([dp_long, pa_long], [constants.design_par_file, constants.perf_attribute_file]):
        if files_list[folder] is not None:
            ids_folder = fileid_int(files_list[folder], filename)
            if folder == dp_long:
                vec_mis = np.setdiff1d(ids_folder, data_gen_dp["fileid_vector"])
                vec_mis1 = np.setdiff1d(data_gen_dp["fileid_vector"], ids_folder)
            elif folder == pa_long:
                vec_mis = np.setdiff1d(ids_folder, data_gen_pa["fileid_vector"])
                vec_mis1 = np.setdiff1d(data_gen_pa["fileid_vector"], ids_folder)
            vec_ids_mismatch[folder] = vec_mis
            vec_ids_mismatch_uiddiff[folder] = vec_mis1
            if len(vec_mis) or len(vec_mis1):
                string_msg = "- There is a mismatch between files and stored file ids! Regenerate the vector!"
                error = 1
        else:
            vec_ids_mismatch[folder] = None
            string_msg = "- There is a mismatch between files and stored file ids! Regenerate the vector!"
            error = 1
    return vec_ids_mismatch, vec_ids_mismatch_uiddiff, string_msg, error


def check_file_ids_dr(files_list, data_gen_dr):
    vec_ids_mismatch = dict()
    vec_ids_mismatch_uiddiff = dict()
    string_msg = "- There is no mismatch between files and stored file ids"
    error = 0
    for folder in files_list.keys():
        if files_list[folder] is not None:
            ids_folder = fileid_int(files_list[folder], constants.design_rep_file)

            vec_mis = np.setdiff1d(ids_folder, data_gen_dr[folder]["fileid_vector"])
            vec_mis1 = np.setdiff1d(data_gen_dr[folder]["fileid_vector"], ids_folder)

            vec_ids_mismatch[folder] = vec_mis
            vec_ids_mismatch_uiddiff[folder] = vec_mis1
            if len(vec_mis) or len(vec_mis1):
                string_msg = "- There is a mismatch between files and stored file ids! Regenerate the vector!"
                error = 1
        else:
            vec_ids_mismatch[folder] = None
            string_msg = "- There is a mismatch between files and stored file ids! Regenerate the vector!"
            error = 1
    return vec_ids_mismatch, vec_ids_mismatch_uiddiff, string_msg, error


def fileid_str(fileid):
    return "%04d" % int(fileid)


def fileid_int(fileid_str, filename, format=".pkl"):
    if not isinstance(fileid_str, list):
        fileid_str = [fileid_str]
    vec_ids = [int(o.split(filename + "_")[1].split(format)[0]) for o in fileid_str]
    return vec_ids


def data_types(input):
    if isinstance(input, list):
        aux = np.asarray(input)
    elif isinstance(input, (int, float)):
        aux = np.asarray([input])
    else:
        aux = copy.copy(input)
    if len(aux.shape) > 1:
        type_asstr = str(type(aux[0, 0])).split(" '")[1].split("'")[0]
        return type(aux[0, 0]), str(aux.dtype), type_asstr
    else:
        type_asstr = str(type(aux[0].item())).split(" '")[1].split("'")[0]
        return type(aux[0].item()), str(aux.dtype), type_asstr


def copy_without_data(dataset):
    dataset_copy = copy.deepcopy(dataset)

    for block in flatten_dict(dataset_copy.data_blocks):
        block.data = None

    return dataset_copy


def setdiff_sym(vec1, vec2):
    """Returns the symmetric difference of two arrays. In particular, A ⊕ B = (A - B) ∪ (B - A)."""
    return np.union1d(np.setdiff1d(vec1, vec2), np.setdiff1d(vec2, vec1))


def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False


def get_shape(data: Union[pd.DataFrame, np.ndarray, List[List], Dict, List[Dict], torch.Tensor], dataobjects: List[DataObject] = None) -> List:
    """
    Takes some data in any format, and returns its shape
    Parameters
    ----------
    data : Union[pd.DataFrame, np.ndarray, List[List], Dict, List[Dict], torch.Tensor]
        Data with some specific format.

    Returns
    -------
    shape : List
        List with [number_samples, total_dimensions]
    """
    # First detect the format
    format_in = _detect_format(data, dataobjects)

    if format_in in ["dict", "dict_list", "df_per_obj"]:
        data = convert_to(data, "array")
        return list(data.shape)
    elif format_in in ["df", "array", "torch"]:
        return list(data.shape)
    elif format_in == "list":
        return [len(data), len(data[0])]


def convert_to(
    data: Union[pd.DataFrame, np.ndarray, List[List], Dict, List[Dict], torch.Tensor], format: str = "df", dataobjects: List[DataObject] = None
) -> Union[pd.DataFrame, np.ndarray, List[List], Dict, List[Dict], torch.Tensor]:
    """
    Takes any data format, detect the type, and convert it if neccessary.

    The possible formats are:

    - "dict" : dictionary
    - "dict_list" : list of dictionaries
    - "df_per_obj" : dataframe
    - "df" : standard dataframe flattened, all cells contain single values and column names are renamed.
    - "array" : nparray
    - "torch" : torch tensor
    - "list" : nested list

    In principle, the only inputs are the data, the desired format and the data objects. This is all required
    to detect and then convert

    Important: this functions only works with the data. This means it does not expect any
    "uid" or "error" columns. These will cause errors.

    Parameters
    ----------
    data : Union[pd.DataFrame, np.ndarray, List[List], Dict, List[Dict], torch.Tensor]
        Data with some specific format.
    format : str, optional, default="df"
        Desired target format.
    dataobjects : List[DataObject], optional, default=None
        List of data objects from which names and dimensions will be recovered.

    Returns
    -------
    data_out : Union[pd.DataFrame, np.ndarray, List[List], Dict, List[Dict], torch.Tensor]
        Converted data
    """

    if format not in ["dict", "dict_list", "df_per_obj", "df", "array", "torch", "list"]:
        raise ValueError(f"Format {format} is not supported. Supported formats are: 'dict', 'dict_list', 'df_per_obj', 'df', 'array', 'torch', 'list'")

    # First detect the format
    format_in = _detect_format(data, dataobjects)

    # Convert to the required format
    if format_in == format:
        return data

    else:
        # We only work with the data
        if format_in in ["df_per_obj", "df"]:
            data = data.drop(["uid"], axis=1) if "uid" in data.columns else data
            data = data.drop(["error"], axis=1) if "error" in data.columns else data

        if format_in == "dict" or format_in == "dict_list":
            if format_in == "dict_list":
                data = reformat_dictlist_to_dict(data)
                if format == "dict":
                    return data

            if format == "dict_list":
                return reformat_dict_to_dictlist(data)
            elif format in ["list", "array", "torch", "df_per_obj", "df"]:
                data_aux = reformat_dict_to_dataframe(data)
                if format == "df_per_obj":
                    return data_aux
                elif format == "df":
                    return reformat_dataframe_to_dataframeflat(data_aux, dataobjects)
                elif format in ["list", "array", "torch"]:
                    data_aux = reformat_dataframe_to_list(data_aux)
                    return _to_arraytorch(data_aux, format)

        elif format_in == "df_per_obj" or format_in == "df":
            if format_in == "df":
                data = reformat_dataframeflat_to_dataframe(data, dataobjects)
                if format == "df_per_obj":
                    return data

            if format == "df":
                return reformat_dataframe_to_dataframeflat(data, dataobjects)
            elif format == "dict":
                return reformat_dataframe_to_dict(data)
            elif format == "dict_list":
                return reformat_dataframe_to_dictlist(data)
            elif format in ["list", "array", "torch"]:
                data_aux = reformat_dataframe_to_list(data)
                return _to_arraytorch(data_aux, format)

        elif format_in in ["list", "array", "torch"]:
            # Yes, there is a bit of back and forth conversion, but it is not that bad
            if format_in in ["array", "torch"]:
                if format_in == "torch":
                    data = reformat_torch_to_array(data)
                data = reformat_array_to_list(data)

            if format == "dict_list":
                return reformat_list_to_dictlist(data, dataobjects)
            elif format == "dict":
                return reformat_list_to_dict(data, dataobjects)
            elif format in ["df_per_obj", "df"]:
                data_aux = reformat_list_to_dataframe(data, dataobjects)
                if format == "df_per_obj":
                    return data_aux
                elif format == "df":
                    return reformat_dataframe_to_dataframeflat(data_aux, dataobjects)
            elif format in ["list", "array", "torch"]:
                return _to_arraytorch(data, format)


def combine_formats(data: List[Union[pd.DataFrame, np.ndarray, List[List], Dict, List[Dict], torch.Tensor]], format: str = "df"):
    """
    Combines data into a single output and converts them into the specified target format.

    The possible formats are:

    - "dict" : Dict (dictionary)
    - "dict_list" : List[Dict] (list of dictionaries)
    - "df_per_obj" : pd.DataFrame (dataframe where cells can contain list of values for multi-dimensional objects)
    - "df" : pd.DataFrame (standard dataframe flattened, all cells contain single values and column names are renamed)
    - "array" : np.ndarray
    - "torch" : torch.Tensor
    - "list" : List[List] (nested list)

    Intended to combine, for example, data from the design parameters and performance attributes.

    Parameters
    ----------
    data : List[Union[pd.DataFrame, np.ndarray, List[List], Dict, List[Dict], torch.Tensor]]
        A list of data in various types and formats.
    format : str, optional, default="df"
        Name of the target format for the returned combined data.

    Returns
    -------
    pd.DataFrame or np.ndarray or List[List] or Dict or List[Dict] or torch.Tensor
        Combined data in the specified format.
    """

    if not isinstance(data, list):
        raise ValueError("The input data must be a list")

    def create_dict(list_dict):
        dict_out = {}
        for d in list_dict:
            dict_out = {**dict_out, **d}
        return dict_out

    if format == "dict":
        return create_dict(data)
    elif format == "dict_list":
        list_out = []
        for ind1 in range(len(data[0])):
            dict_out = {}
            for ind2 in range(len(data)):
                dict_out = {**dict_out, **data[ind2][ind1]}
            list_out.append(dict_out)
        return list_out
    elif format in ["df_per_obj", "df"]:
        return pd.concat(data, axis=1)
    elif format == "array":
        return np.hstack(data)
    elif format == "torch":
        return torch.hstack(data)
    elif format == "list":
        list_out = []
        for ind1 in range(len(data[0])):
            list_aux = []
            for ind2 in range(len(data)):
                list_aux.extend(data[ind2][ind1])
            list_out.extend(list_aux)
        return list_out
    else:
        raise ValueError(f"Format {format} is not supported. Supported formats are: 'dict', 'dict_list', 'df_per_obj', 'df', 'array', 'torch', 'list'")


def _detect_format(data: Union[pd.DataFrame, np.ndarray, List[List], Dict, List[Dict], torch.Tensor], dataobjects: List[DataObject] = None) -> str:
    """
    Detect the format of the input data.

    Parameters
    ----------
    data : Union[pd.DataFrame, np.ndarray, List[List], Dict, List[Dict], torch.Tensor]
        Data of any of these types and formats.

    Returns
    -------
    str
        Name of the data's type or format: 'dict', 'dict_list', 'df_per_obj', 'df', 'array' or 'torch'.
    """
    if isinstance(data, pd.DataFrame):
        if dataobjects is None:
            # This is an alternative method to compute the format, which might not worked all the time.
            # Only used in case the dataobjects are not really known.
            for col in data.columns:
                if isinstance(data[col].iloc[0], list):
                    return "df_per_obj"
            else:
                return "df"
        else:
            columns_df = list(data.columns)
            columns_df.remove("uid") if "uid" in columns_df else None
            columns_df.remove("error") if "error" in columns_df else None
            columns_df_datablock = [c for dobj in dataobjects for c in dobj.columns_df]

            if columns_df == columns_df_datablock:
                return "df"
            elif len(columns_df) == len(dataobjects):
                return "df_per_obj"
            else:
                raise ValueError("The dataframe does not have the correct columns.")
    elif isinstance(data, np.ndarray):
        return "array"
    elif isinstance(data, torch.Tensor):
        return "torch"
    elif isinstance(data, list):
        if isinstance(data[0], list):
            return "list"
        elif isinstance(data[0], dict):
            return "dict_list"
    elif isinstance(data, dict):
        return "dict"
    else:
        raise ValueError(f"Format {type(data)} is not supported.")


def _to_arraytorch(x, format):
    # Input is a list
    if format == "list":
        return x
    elif format in ["array", "torch"]:
        x = reformat_list_to_array(x)
        if format == "array":
            return x
        elif format == "torch":
            return reformat_array_to_torch(x)


def reformat_dict_to_dataframe(dct: Union[Dict, List[Dict]]) -> pd.DataFrame:
    """
    Reformats data formatted as a (list of) dictionaries to a pandas dataframe.
    In the intended useage, the keys of the dictionary(ies) correspond to the original names of the data objects,
    and to column names in the dataframe.

    Two formats of the input are possible and equivalent:

    - a list of dictionaries: each item corresponds to one sample, all dictionaries have to have the same keys.
    - one dictionary: each key stores a list of values, each value corresponding to one sample.
        The value itself can be a list if the object's dimension is > 1.

    Parameters
    ----------
    dct : Dict or List[Dict]
        A dictionary or a list of dictionaries.

    Returns
    -------
    pd.DataFrame
        DataFrame object.

    Examples
    --------
    The following formats of the input are equivalent and produce the same dataframe:

    >>> dct = [{"a": 0, "b": 1}, {"a": 2, "b": 3}]
    >>> dct = {"a": [0, 2], "b": [1, 3]}
    >>> reformat_dict_to_dataframe(dct)
       a  b
    0  0  1
    1  2  3

    If values itself are multi-dimensional, equally both formats are equivalent:

    >>> dct = [{"a": [0, 0], "b": 1}, {"a": [2, 2], "b": 3}]
    >>> dct = {"a": [[0, 0], [2, 2]], "b": [1, 3]}
    >>> reformat_dict_to_dataframe(dct)
            a  b
    0  [0, 0]  1
    1  [2, 2]  3

    """
    return pd.DataFrame.from_dict(dct)


def reformat_dataframe_to_dict(dataframe: pd.DataFrame, listwrap: bool = False) -> Dict:
    """
    Reformats data formatted as a dataframe into a dictionary.
    In the intended usage, each row of the dataframe corresponds to one data sample and each row to a data object.
    The column names will be mapped to keys in the dictionary.
    To access a particular value, use: `dct[column_name_as_key][nth_sample][ith_dimension]`.

    Parameters
    ----------
    dataframe : pd.DataFrame
        A dataframe object.
    listwrap : bool, optional, default=False
        If True, 1-dimensional values will be put into a 1-item list (e.g., 3.14 -> [3.14]).

    Returns
    -------
    Dict
        A dictionary.
    """
    dct = dataframe.to_dict(orient="list")
    if listwrap:
        dct = {k: [x if isinstance(x, list) else [x] for x in v] for k, v in dct.items()}  # wrap single values into a list for convenience
    return dct


def reformat_dataframe_to_dictlist(dataframe: pd.DataFrame, listwrap: bool = False) -> List[Dict]:
    """
    Reformats data formatted as a dataframe into a dictionary.
    In the intended usage, each row of the dataframe corresponds to one data sample and each row to a data object.
    The column names will be mapped to keys in the dictionary.
    To access a particular value, use: `dct[nth_sample][column_name_as_key][ith_dimension]`.

    Parameters
    ----------
    dataframe : pd.DataFrame
        A dataframe object.
    listwrap : bool, optional, default=False
        If True, 1-dimensional values will be put into a 1-item list (e.g., 3.14 -> [3.14]).

    Returns
    -------
    List[Dict]
        A list of dictionaries, where each item in the list is a dictionary corresponding to one sample.
    """
    dctlist = dataframe.to_dict(orient="records")
    if listwrap:
        dctlist = [{k: v if isinstance(v, list) else [v] for k, v in dct.items()} for dct in dctlist]  # wrap single values into a list for convenience
    return dctlist


def reformat_dataframeflat_to_dict(dataframe: pd.DataFrame, dataobjects: List[DataObject], listwrap: bool = False) -> Dict:
    """
    Reformats data stored in a dataframe to a dictionary collated accordingly to the provided list of data objects.
    In the dataframe, the data is "flattened", i.e. the cells contain single values and for data objects with dim>1 are stored in columns named as in `DataObject.columns_df`.
    In the resulting dictionary, the keys correspond to the original object names and the values store a list of values for individual samples.
    To access a particular value: dict[dataobject_name_as_key][nth_sample][ith_dimension].

    Note:
    Any columns in the dataframe that cannot be associated with any data object will be ignored.
    Any data objects with no corresponding column in the dataframe will be ignored.

    Parameters
    ----------
    dataframe : pd.DataFrame
        A dataframe with "flattened" data.
    dataobjects : List[DataObject]
        A list of data objects from the dataset.
    listwrap : bool, optional, default=False
        If True, 1-dimensional values will be put into a 1-item list (e.g., 3.14 -> [3.14]).

    Returns
    -------
    Dict
        A dictionary with keys corresponding to the original data object names and collated according to their dimensionality.
    """

    dct = {dobj.name: dataframe[dobj.name if dobj.dim == 1 else dobj.columns_df].values.tolist() for dobj in dataobjects}
    if listwrap:
        dct = {k: [x if isinstance(x, list) else [x] for x in v] for k, v in dct.items()}  # wrap single values into a list for convenience

    return dct


def reformat_dataframe_to_dataframeflat(dataframe: pd.DataFrame, dataobjects: List[DataObject]) -> pd.DataFrame:
    """
    Reformats a dataframe that may represent multidimensional data objects (cells containing lists of values, if dim>1), to a flattened dataframe.
    In the flattened dataframe, all cells contain single values and column names are renamed.
    In the intended use each row corresponds to one sample.

    Parameters
    ----------
    dataframe : pd.DataFrame
        A dataframe object with collapsed columns.
    dataobjects : List[DataObject]
        A list of data objects from the dataset.

    Returns
    -------
    pd.DataFrame
        New dataframe, flattened (one value per cell).
    """

    dataframe_flat = pd.DataFrame()
    for dobj in dataobjects:
        if dobj.name in dataframe.columns:
            dataframe_flat[dobj.columns_df if dobj.dim > 1 else dobj.name] = dataframe[dobj.name].values.tolist()
    return dataframe_flat


def reformat_dataframeflat_to_dataframe(dataframeflat: pd.DataFrame, dataobjects: List[DataObject]) -> pd.DataFrame:
    """
    Reformats a flattened dataframe into a dataframe that may represent multidimensional data objects (cells containing n lists of values, if dim>1).
    In the flattened dataframe, all cells contain single values and column names are renamed.

    Parameters
    ----------
    dataframeflat : pd.DataFrame
        A dataframe with flattened data (one value per cell).
    dataobjects : List[DataObject]
        A list of data objects from the dataset.

    Returns
    -------
    pd.DataFrame
        New dataframe with collapsed columns (for data objects with dim>1).
    """
    dataframe = pd.DataFrame()
    for dobj in dataobjects:
        if set(dobj.columns_df).issubset(dataframeflat.columns):
            dataframe[dobj.name] = dataframeflat[dobj.columns_df if dobj.dim > 1 else dobj.name].values.tolist()
    return dataframe


def reformat_list_to_array(nested_list: List[List]) -> np.ndarray:
    """
    Reformats data formatted as a nested list into a numpy.ndarray.
    In the intended use, an item in the main list corresponds to a data sample and to a row in the array.
    The data in the sub-lists must be flattened (no further sub-lists).

    Parameters
    ----------
    nested_list : List[List]
        List of lists, max. depth: 2 (data correspodning to data objects with dim > 1 must be flattened.)

    Returns
    -------
    np.ndarray
        A numpy ndarray.

    Examples
    --------
    >>> nested_list = [[1,2,3],[7,8,9]]
    >>> print(reformat_list_to_array(nested_list))
    [[1 2 3]
     [7 8 9]]
    """
    arr = np.vstack(nested_list)  # n x m
    return arr


def reformat_array_to_list(arr: np.ndarray) -> List[List]:
    """
    Reformat numpy.ndarray into a nested list.
    In the intended use, a row in the array corresponds to a data sample and to an item (which is again a list of values) in the returned list.
    Data corresponding to data objects with dim > 1 are flattened both in the input and output.

    Parameters
    ----------
    arr : np.ndarray
        A 2d numpy ndarray.

    Returns
    -------
    List[List]
        A nested list.

    Examples
    --------
    >>> arr = np.asarray([[1, 2, 3],[7, 8, 9]])
    >>> reformat_array_to_list(np.asarray([[1, 2, 3],[7, 8, 9]]))
    [[1, 2, 3], [7, 8, 9]]
    """
    return arr.tolist()


def reformat_list_to_dataframe(nested_list: List[List], dataobjects: List[DataObject]) -> pd.DataFrame:
    """
    Reformats data formatted as a nested list of data into a dataframe.
    Each item in the list corresponds to one sample and contains a flattened list of values (no further sub-lists).
    The purpose of this method is to recover an unflattened dataframe.
    The information about the original dimensions and names of the data objects is drawn from the given list of data objects.
    The order of the provided data objects must match the data in the nested list.

    Parameters
    ----------
    nested_list : List[List]
        List of lists, containing data.
    dataobjects : List[DataObject]
        List of data objects from which names and dimensions will be recovered.

    Returns
    -------
    pd.DataFrame
        Recovered unflattened dataframe.

    Examples
    --------
    >>> from aixd.data.data_objects import DataInt
    >>> a = DataInt(name = "a", dim=2)
    >>> b = DataInt(name = "b", dim=1)
    >>> c = DataInt(name = "c", dim=1)
    >>> nested_list = [[1, 1, 2, 3], [7, 7, 8, 9]]
    >>> reformat_list_to_dataframe(nested_list, [a, b, c])
            a	b	c
    0	[1, 1]	2	3
    1	[7, 7]	8	9
    """
    return pd.DataFrame(reformat_list_to_dict(nested_list, dataobjects))


def reformat_dataframe_to_list(dataframe: pd.DataFrame) -> List[List]:
    """
    Reformats a pandas dataframe into a nested list.
    In the output, 1st-level items correspond to the rows in the dataframe (e.g. samples), 2nd-level items correspond to the data values.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Dataframe containing data.

    Returns
    -------
    List[List]
        List of lists. They are always flattened.

    Examples
    --------
    >>> dataframe = pd.DataFrame(data = {'a':[[1,1],[7,7]], 'b':[2,8], 'c':[3,9] })
    >>> reformat_dataframe_to_list(dataframe)
    [[1, 1, 2, 3], [7, 7, 8, 9]]
    """
    return [flatten_list(row.to_list()) for _, row in dataframe.iterrows()]


def reformat_list_to_dict(nested_list: List[List], dataobjects: List[DataObject]) -> Dict:
    """
    Reformats data formatted as a nested list into a dictionary.
    Each item in the list corresponds to one sample and contains a flattened list of values (no further sub-lists).
    The purpose of this method is to associate the data with names and collate into their original dimensions.
    The information about the original dimensions and names of the data objects is drawn from the given list of dataobjects.
    The order of the provided data objects must match the data in the nested list.

    Parameters
    ----------
    nested_list : List[List]
        List of lists, containing data.
    dataobjects : List[DataObject]
        List of data objects from which names and dimensions will be recovered.

    Returns
    -------
    Dict
        Data in form of a dictionary.

    Examples
    --------
    >>> from aixd.data.data_objects import DataInt
    >>> a = DataInt(name = "a", dim=2)
    >>> b = DataInt(name = "b", dim=1)
    >>> c = DataInt(name = "c", dim=1)
    >>> nested_list = [[1,1, 2, 3], [7,7,8,9]]
    >>> reformat_list_to_dict(nested_list, [a,b,c])
    {'a': [[1, 1], [7, 7]], 'b': [2, 8], 'c': [3, 9]}
    """

    nested_list = np.asarray(nested_list)

    # Compute the indices of the columns corresponding to each data object
    splits = np.cumsum([0] + [dobj.dim for dobj in dataobjects])

    # Extract the values for each data object
    values = [nested_list[:, start].tolist() if start + 1 == end else nested_list[:, start:end].tolist() for start, end in zip(splits[:-1], splits[1:])]

    # Create a dictionary from the data objects and values
    dct = dict(zip([dobj.name for dobj in dataobjects], values))

    return dct


def reformat_list_to_dictlist(nested_list: List[List], dataobjects: List[DataObject]) -> List[Dict]:
    """
    Reformats data formatted as a nested list into a list of dictionaries.
    Each item in the list corresponds to one sample and contains a flattened list of values (no further sub-lists).
    The purpose of this method is to associate the data with names and collapse to their original dimensions.
    The information about the original dimensions and names of the data objects is drawn from the given list of dataobjects.
    The order of the provided data objects must match the data in the nested list.

    Parameters
    ----------
    nested_list : List[List]
        List of lists, containing data.
    dataobjects : List[DataObject]
        List of data objects from which names and dimensions will be recovered.

    Returns
    -------
    List[Dict]
        Data in form of a list of dictionaries.

    Examples
    --------
    >>> from aixd.data.data_objects import DataInt
    >>> a = DataInt(name = "a", dim=2)
    >>> b = DataInt(name = "b", dim=1)
    >>> c = DataInt(name = "c", dim=1)
    >>> nested_list = [[1,1, 2, 3], [7,7,8,9]]
    >>> reformat_list_to_dictlist(nested_list, [a,b,c])
    [{'a': [1, 1], 'b': 2, 'c': 3}, {'a': [7, 7], 'b': 8, 'c': 9}]
    """

    dct = reformat_list_to_dict(nested_list, dataobjects)
    return reformat_dict_to_dictlist(dct)


def reformat_dictlist_to_dict(dictlist: List[Dict]) -> Dict:
    """
    The input is a list of dictionaries, where each dictionary, e.g., corresponds to one data sample and the keys correspond to the data object names.
    This method reformats it into one dictionary where the values from all samples are collated under the same key.

    Parameters
    ----------
    dictlist : List[dict]
        List of dictionaries.

    Returns
    -------
    Dict
        Single collated dictionary.

    Examples
    --------
    >>> dictlist = [{'a': [1, 1], 'b': 2, 'c': 3}, {'a': [7, 7], 'b': 8, 'c': 9}]
    >>> reformat_dictlist_to_dict(dictlist)
    {'a': [[1, 1], [7, 7]], 'b': [2, 8], 'c': [3, 9]}
    """
    combined_dict = defaultdict(list)

    for dictionary in dictlist:
        for key, value in dictionary.items():
            combined_dict[key].append(value)
    combined_dict = dict(combined_dict)  # convert back to a regular dict

    return combined_dict


def reformat_dict_to_dictlist(dct: Dict) -> List[Dict]:
    """
    In the input dictionary, each key (e.g. corresponding to a data object name) contains a list of items (e.g. corresponding to individual samples).
    This method reformats split it into a list of dictionaries (e.g. so that each dictionary corresponds to one sample)

    Parameters
    ----------
    dct : Dict
        Dictionary containing collated data.

    Returns
    -------
    List[Dict]
        List of dictionaries split per sample.

    Examples
    --------
    >>> dct = {'a': [[1, 1], [7, 7]], 'b': [2, 8], 'c': [3, 9]}
    >>> reformat_dict_to_dictlist(dct)
    [{'a': [1, 1], 'b': 2, 'c': 3}, {'a': [7, 7], 'b': 8, 'c': 9}]
    """
    n = len(list(dct.values())[0])
    assert all([len(v) == n for v in dct.values()]), "Inconsistent number of samples in the input dictionary"
    dictlist = [{key: dct[key][i] for key in dct.keys()} for i in range(n)]
    return dictlist


def reformat_array_to_torch(data: np.ndarray) -> torch.Tensor:
    """
    Converts a numpy array to a torch tensor.

    Parameters
    ----------
    data : np.ndarray
        The input data, either as a tensor or a numpy array.

    Returns
    -------
    torch.Tensor
        The data as a torch tensor.

    """
    data_tensor = to_torch(data, dtype=torch.float32)
    return data_tensor


def reformat_torch_to_array(data: torch.Tensor) -> np.ndarray:
    """
    Converts a torch tensor into a numpy array.

    Parameters
    ----------
    data : torch.Tensor
        The input data, either as a tensor or a numpy array.

    Returns
    -------
    np.array
        The data as a numpy array.

    """
    return to_numpy(data)


def blockdata_as_dict(datablock: DataBlock) -> Dict:
    """
    Retrieves data from the datablock and returns it as a dictionary.
    The keys of the dictionary correspond to the names of the data objects
    and the values corresponding to individual samples are listed together under the same key.
    To access a particular value, use: `dct[object_name_as_key][nth_sample][ith_dimension]`.

    Parameters
    ----------
    datablock : DataBlock
        Data block containing data.

    Returns
    -------
    Dict
        A dictionary.
    """

    return dict(zip(datablock.names_list, datablock.get_data_mats()))


def blockdata_as_dictlist(datablock: DataBlock) -> List[Dict]:
    """
    Retrieves data from the datablock and returns them as a list of dictionaries,
    where each item in the list is a dictionary corresponding to one sample.
    The keys of the dictionary correspond to the names of the data objects.
    To access a particular value, use: `dct[nth_sample][object_name_as_key][ith_dimension]`.

    Parameters
    ----------
    datablock : DataBlock
        Data block containing data.

    Returns
    -------
    List[Dict]
        A list of dictionaries
    """

    dct = blockdata_as_dict(datablock)
    dictlist = reformat_dict_to_dictlist(dct)
    return dictlist
