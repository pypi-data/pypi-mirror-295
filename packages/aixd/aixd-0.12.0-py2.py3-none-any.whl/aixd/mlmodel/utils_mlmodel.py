import datetime
from typing import Any, Callable, Dict, List, Union

import numpy as np
import torch

"""
Function to perform normalization
In all cases, we define 2 vectors to undo the normalization
- x_mean: that can also correspond to the min value for norm_0to1 and norm_m1to1
- x_std: that can also correspond to data range for norm_0to1 and norm_m1to1
"""


def check_rows_nan(x):
    """Checking presence of NaNs in rows of x"""
    x = np.asanyarray(x).sum(axis=1)
    ind_nan = np.argwhere(np.isnan(x)).flatten()
    ind_notnan = np.argwhere(~np.isnan(x)).flatten()
    return ind_nan, ind_notnan


def ids_attrib(list_attr, attribs_ch):
    """Given a subset of attributes, aka desing parameters or performance attributes,
    it returns the ids of the attributes in the list of all attributes"""
    # In case we just want the design error for the selected x we condition on
    num_attr = len(list_attr)
    if len(attribs_ch) < num_attr:
        ids_att = []
        for att in attribs_ch:
            if att in list_attr:
                ids_att.append(np.argwhere(np.asarray(list_attr) == att).flatten()[0])
        if not len(ids_att):
            ids_att = np.arange(num_attr)
    else:
        ids_att = np.arange(num_attr)
    return ids_att


def rec_concat_dict(data: List[dict]) -> dict:
    """Performs recursive concatenation the elements inside the keys of a dictionary."""
    if len(data) == 0:
        return data
    if len(data) == 1:
        return data[0]

    conc_dict = {}
    for key in data[0].keys():
        if isinstance(data[0][key], dict):
            conc_dict[key] = rec_concat_dict([batch[key] for batch in data])
        elif isinstance(data[0][key], np.ndarray):
            conc_dict[key] = np.concatenate([batch[key] for batch in data])
        elif isinstance(data[0][key], float):
            conc_dict[key] = np.array([[batch[key]] for batch in data])
        else:
            conc_dict[key] = torch.cat([batch[key] for batch in data], dim=0)
    return conc_dict


def numpy_dict_to_tensor(numpy_dict: Dict[str, np.array]) -> Dict[str, torch.Tensor]:
    """Converts a dictionary of numpy arrays to a dictionary of torch tensors."""
    conc_dict = {}
    for key in numpy_dict.keys():
        if isinstance(numpy_dict[key], dict):
            conc_dict[key] = numpy_dict_to_tensor(numpy_dict[key])
        elif isinstance(numpy_dict[key], np.ndarray):
            conc_dict[key] = torch.from_numpy(numpy_dict[key]).float()
        else:
            conc_dict[key] = numpy_dict[key]
    return conc_dict


def torch_dict_to_numpy(torch_dict: Dict[str, torch.Tensor]) -> Dict[str, np.array]:
    """Converts a dictionary of torch tensors to a dictionary of numpy arrays."""
    conc_dict = {}
    for key in torch_dict.keys():
        if isinstance(torch_dict[key], dict):
            conc_dict[key] = torch_dict_to_numpy(torch_dict[key])
        elif torch.is_tensor(torch_dict[key]):
            conc_dict[key] = torch_dict[key].detach().numpy()
        else:
            conc_dict[key] = torch_dict[key]
    return conc_dict


def to_torch(x: Union[torch.Tensor, np.ndarray], dtype: Any = None) -> torch.Tensor:
    """
    Converts a numpy array to a torch tensor, with some given type.

    Parameters
    ----------
    x : Union[torch.Tensor, np.ndarray]
        The input data, either as a tensor or a numpy array.
    dtype : Any, default=None
        The data type of the output tensor. If None, the data type is not changed.

    Returns
    -------
    torch.Tensor
        The data as a torch tensor.
    """

    if isinstance(x, (np.ndarray, np.generic)):
        if x.dtype == object:
            x = torch.from_numpy(x.astype(float))
        else:
            x = torch.from_numpy(x)
    elif isinstance(x, torch.Tensor):
        pass
    else:
        raise TypeError(f"Input must be of type torch.Tensor or np.ndarray but was of type {type(x)}")
    return x if dtype is None else x.type(dtype)


def to_numpy(x: Union[torch.Tensor, np.ndarray]) -> np.ndarray:
    """
    Converts a torch tensor to a numpy array.

    Parameters
    ----------
    x : Union[torch.Tensor, np.ndarray]
        The input data, either as a tensor or a numpy array.

    Returns
    -------
    np.ndarray
        The data as a numpy array.
    """
    if isinstance(x, (np.ndarray, np.generic)):
        return x
    elif isinstance(x, torch.Tensor):
        return x.cpu().detach().numpy()
    else:
        raise TypeError(f"Input must be of type torch.Tensor or np.ndarray but was of type {type(x)}")


def apply_numpy_func(x: Union[torch.Tensor, np.ndarray], numpy_func: Callable[[np.ndarray, ...], np.ndarray], out_type="numpy", **kwargs) -> Union[torch.Tensor, np.ndarray]:
    """
    Applies a numpy function to a torch tensor or numpy array.

    Parameters
    ----------
    x : Union[torch.Tensor, np.ndarray]
        The input data.
    numpy_func : Callable[[np.ndarray], np.ndarray]]
        The numpy function to be applied.
    out_type : str, default="numpy"
        The type of the output data. Can be "numpy", "torch", or "same".
    **kwargs
        Keyword arguments to be passed to the numpy function.

    Returns
    -------
    Union[torch.Tensor, np.ndarray]
        The output data. Has the same type as the input data.

    """
    if isinstance(x, (np.ndarray, np.generic)):
        res = numpy_func(x, **kwargs)
    elif isinstance(x, torch.Tensor):
        res = numpy_func(x.cpu().detach().numpy(), **kwargs)
    else:
        raise TypeError(f"Input must be of type torch.Tensor or np.ndarray but was of type {type(x)}")

    if out_type == "numpy":
        return res
    elif out_type == "torch":
        return torch.from_numpy(res)
    elif out_type == "same":
        return torch.from_numpy(res) if isinstance(x, torch.Tensor) else res
    else:
        raise ValueError(f"Invalid value for out_type: {out_type} (must be 'numpy', 'torch', or 'same')")


def sum_join_dicts(dicts: List[dict]) -> dict:
    res = {}
    for d in dicts:
        for k, v in d.items():
            res[k] = res.get(k, 0.0) + v
    return res


def check_filename(filename: str, replacement="_"):
    """Checks for illegal characters in the filename and replaces them with the replacement character."""
    illegal_chars = ["#", "%", "$", "&", "*", "@", "/", ":", " |", "\\", "<", ">", "`", '"', "!"]
    not_recommended = ["{", "}", "+", "=", " "]

    newname = filename.strip()

    # remove illegal characters
    for char in illegal_chars + not_recommended:
        newname = newname.replace(char, replacement)

    return newname


def timestamp_to_string(fmt="%Y-%m-%d %H-%M"):
    """Returns a string representation of the current timestamp."""
    timestamp = datetime.datetime.now().timestamp()
    timestamp_string = datetime.datetime.fromtimestamp(timestamp).strftime(fmt)
    return timestamp_string


def check_errors_ckpt(dict_compare, dataset):
    """Check several conditions to ensure the checkpoint that is being loaded corresponds
    to the dataset that is being used, and was also obtained with the same number of samples."""
    str_err = ""
    if dict_compare["name_proj"] != dataset.name:
        str_err += "* You have provided a different dataset\n"
    if dict_compare["num_samples"] != len(dataset.design_par.data):
        str_err += "* The number of samples loaded is different\n"
    if dict_compare["num_samples"] == len(dataset.design_par.data):
        if dict_compare["uids_vec"] != list(dataset.design_par.data["uid"]):
            str_err += "* The uids for the samples are different\n"
    return str_err
