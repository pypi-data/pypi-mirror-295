from functools import partial
from itertools import chain
from typing import TYPE_CHECKING, Dict, List, Tuple, Union

import numpy as np
import pandas as pd

from aixd.data.constants import design_par_long as dp_long
from aixd.data.constants import perf_attribute_long as pa_long
from aixd.data.custom_callbacks import ImportCallback

if TYPE_CHECKING:
    from aixd.data.dataset import Dataset


def df_importer(vec_shards: Tuple[int], dataset: "Dataset", data: pd.DataFrame, custom_mapping: Dict[str, Union[str, List[str]]] = None) -> Dict[str, np.ndarray]:
    """
    An importer function that can be used with the ImportCallback class to import data from a pandas dataframe into the dataset. In particular, it maps the columns of the dataframe
    to the DataObjects of the dataset. It follows the following rules for mapping:

    * If a custom mapping is provided for a DataObject, this takes precedence over all the other rules.
    * If the name of a DataObject is found in the columns of the dataframe, it is mapped to that column. Note that for multidimensional DataObjects, columns can contain lists.
    * If a DataObject is multidimensional and the name of a DataObject is not found in the columns of the dataframe, we search for DataObject.columns_df in the columns of the dataframe.
    * If above rules do not apply, the import fails, and the user can either provide a custom mapping or rename the columns of the dataframe.

    For the performance attributes, the importer also checks if the column "error" is present in the dataframe. If so, it is added to the performance attributes.

    Parameters:
    ----------
    vec_shards: Tuple[int]
        A tuple of integers, where the first integer defines the shard number and the second integer defines the total number of shards.
    dataset: Dataset
        The dataset object to import the data into.
    data: pd.DataFrame
        The dataframe containing the data to import.
    custom_mapping: Dict[str, Union[str, List[str]]]
        A dictionary mapping the names of the DataObjects to the names of the columns in the dataframe. For multidimensional DataObjects, a list of column names can be provided.
        If None, the names of the DataObjects must match the names of the columns in the dataframe.

    Returns:
    -------
    Dict[str, np.ndarray]
        A dictionary mapping containing the design parameters and performance attributes.
    """
    if vec_shards != [0, 1]:
        raise Exception("This importer does not support multiple shards.")

    # check for duplicates columns
    if len(data.columns) != len(set(data.columns)):
        print(data.columns)
        raise Exception("Duplicate not allowed in csv file.")

    # check custom mapping
    if custom_mapping is not None:
        custom_mapping = {k: ([v] if isinstance(v, str) else v) for k, v in custom_mapping.items()}
        mapped_values = list(chain(*custom_mapping.values()))
        if len(mapped_values) != len(set(mapped_values)):
            raise Exception("Two or more entries in the custom mapping map to the same value.")
    else:
        custom_mapping = dict()

    def _check_load_columns(block):
        """Helper function to check if columns are available and load them into a matrix."""
        available_columns = set(data.columns)
        data_mat = []
        for dobj in block.dobj_list:
            if dobj.name in custom_mapping:
                cols = custom_mapping[dobj.name]
                if not available_columns.issuperset(cols):
                    raise Exception(f"Custom mapping for {dobj.name} contains columns not found in available columns: " + ", ".join(available_columns))
            elif dobj.name in available_columns:
                cols = [dobj.name]
            elif dobj.dim > 1 and available_columns.issuperset(dobj.columns_df):
                cols = dobj.columns_df
            else:
                if dobj.dim == 1:
                    raise Exception(f"Column {dobj.name} not found in available columns: " + ", ".join(available_columns))
                else:
                    raise Exception(f"Multi-column {dobj.name} nor columns {dobj.columns_df} found in available columns: " + ", ".join(available_columns))

            # As we allow DataFrames to contain lists, we need to flatten the data matrix only across second dimension
            data_mat_sub = data[cols].map(lambda x: x if isinstance(x, list) else [x]).values.tolist()
            data_mat_sub = np.array(data_mat_sub).reshape(len(data_mat_sub), -1)
            data_mat.append(data_mat_sub)

        return np.concatenate(data_mat, axis=1, **{"dtype": object})  # we need to use object dtype to allow for mixed types

    design_par_mat = _check_load_columns(dataset.design_par)
    perf_attributes_mat = _check_load_columns(dataset.perf_attributes)
    if "error" in data.columns:
        perf_attributes_mat = np.concatenate([perf_attributes_mat, data[["error"]].to_numpy()], axis=1)

    return {dp_long: design_par_mat, pa_long: perf_attributes_mat}


def csv_importer(vec_shards: Tuple[int], dataset: "Dataset", file_path: str, custom_mapping: Dict[str, Union[str, List[str]]] = None) -> Dict[str, np.ndarray]:
    """
    Wrapper around df_importer to import data from a csv file. For more information, see df_importer.

    Parameters:
    ----------
    vec_shards: Tuple[int]
        A tuple of integers, where the first integer defines the shard number and the second integer defines the total number of shards.
    dataset: Dataset
        The dataset object to import the data into.
    file_path: str
        The path to the csv file containing the data to import.
    custom_mapping: Dict[str, Union[str, List[str]]]
        A dictionary mapping the names of the DataObjects to the names of the columns in the dataframe. For multidimensional DataObjects, a list of column names can be provided.

    Returns:
    -------
    Dict[str, np.ndarray]
        A dictionary mapping containing the design parameters and performance attributes.
    """
    return df_importer(vec_shards=vec_shards, dataset=dataset, data=pd.read_csv(file_path), custom_mapping=custom_mapping)


def df_importer_callback(dataset: "Dataset") -> ImportCallback:
    """Convenience function to create an ImportCallback for df_importer."""
    return ImportCallback(name="df_importer", func_callback=partial(df_importer, dataset=dataset), dataset=dataset)


def csv_importer_callback(dataset: "Dataset") -> ImportCallback:
    """Convenience function to create an ImportCallback for csv_importer."""
    return ImportCallback(name="csv_importer", func_callback=partial(csv_importer, dataset=dataset), dataset=dataset)
