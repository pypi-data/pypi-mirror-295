from __future__ import annotations

import io
from collections import defaultdict
from typing import Any, Dict, List, Tuple, Union

import numpy as np
import pandas as pd

import aixd.data.constants as constants
import aixd.data.utils_data as ud
from aixd.data.data_objects import DataObject
from aixd.utils.utils import list_unique

dp_long = constants.design_par_long
pa_long = constants.perf_attribute_long
dr_long = constants.design_rep_long


class DataBlock:
    """
    Generic block of data, i.e., a concatenation of different instances
    of data types

    Parameters
    ----------
    dobj_list : List[DataObject]
       A list of data objects.
    name : str, optional
       A name for the data block
    format_file : str, optional, default="pkl"
       File format used for storage.
    flag_split_perdim : bool, optional, default=False
       Flag to enable the splitting multidimensional DataObject's
    transformation : DataBlockTransformation, optional, default=None
        The per data block normalization.
    display_name : str, optional, default=None
        The display name of the data block. If none it's the same as the `name`.
    """

    def __init__(
        self,
        dobj_list: List[DataObject],
        name: str = None,
        format_file: str = "pkl",
        flag_split_perdim: bool = False,
        transformation: DataBlockTransformation = None,
        display_name: str = None,
    ):
        self.name = name  # Descriptor for the DataBlock
        self.format_file = format_file  # The file format used for storing

        # Enable flag_split_perdim for all DataObject's with dim > 1, if flag_split_perdim is True
        for dobj in dobj_list:
            if dobj.dim > 1 and flag_split_perdim:
                dobj.flag_split_perdim = True

        # Holds the updated data objects
        self.dobj_list = self._update_dobj_list(dobj_list)

        # Testing uniqueness of column names
        un_val, un_count = np.unique(self.columns_df, return_counts=True)
        if (un_count > 1).any():
            list_wrong = [un_val[i] for i in np.argwhere(un_count > 1).flatten()]
            list_wrong = ", ".join(list_wrong) if len(list_wrong) < 10 else ", ".join(list_wrong[:10]) + ", ..."
            raise ValueError(f"DataBlock {self.name} has duplicated column names: {list_wrong}")
        if "error" in self.names_list:
            raise ValueError(f"DataBlock {self.name} has column name 'error', which is a reserved name.")

        # Holds the data, initially None. Set by the user.
        self._data = None

        # Display name
        self.display_name = display_name if display_name is not None else self.name

        # Per data block normalization
        self.transformation = transformation or DefaultDataBlockTransformation()

    def __jsondump__(self):
        data_frame_or_nparray = None
        if self.data is not None:
            if isinstance(self.data, pd.DataFrame):
                data_frame_or_nparray = {"data_type": "dataframe", "data": self.data.to_json(orient="split")}
            else:
                raise NotImplementedError("Support for numpy array not implemented yet.")
                # NOTE: Adding support for this would be something like this:
                # data_frame_or_nparray = {"data_type": "nparray", "data": np.array2string(self.data, separator=" ")}
        return {
            "name": self.name,
            "format_file": self.format_file,
            "dobj_list": self.dobj_list,
            "transformation": self.transformation,
            "display_name": self.display_name,
            "data": data_frame_or_nparray,
        }

    @classmethod
    def __jsonload__(cls, data):
        data_frame_or_nparray = data.pop("data", None)
        datablock = cls(**data)
        if data_frame_or_nparray:
            if data_frame_or_nparray.get("data_type") == "dataframe":
                datablock.data = pd.read_json(io.StringIO(data_frame_or_nparray["data"]), orient="split")
            elif data_frame_or_nparray.get("data_type") == "nparray":
                raise NotImplementedError("Support for numpy array not implemented yet.")
                # NOTE: Adding support for this would be something like this:
                # datablock._data = np.fromstring(data_frame_or_nparray["data"], sep=" ")
        return datablock

    @property
    def data(self) -> Union[np.ndarray, pd.DataFrame]:
        """Getter method for the data, returned as pd.DataFrame or np.ndarray"""
        return self._data

    @data.setter
    def data(self, data: Union[np.ndarray, pd.DataFrame]):
        """
        Setter method for the data. Some conventions must be followed.

        - The data is expected to either be a pd.Dataframe or a np.ndarray.
        - The first column contains the uid's, followed with columns representing the data of the DataObject's

        Parameters
        ----------
        data :  Union[np.ndarray, pd.DataFrame]
            The data to be set on the DataBlock

        """
        if data is not None:
            if self.format_file == "npz":
                self._data = data
            else:
                self._data = data[self.columns_df]
        else:
            self._data = data

    @property
    def data_mat(self) -> np.ndarray:
        """
        Returns the entire data matrix without the uid column as numpy array.
        """
        return np.asarray(self.data)[:, 1:]  # Remove uid column

    @property
    def names_list(self) -> List[str]:
        """
        Returns the names of the DataObject's in the DataBlock.
        """
        return [] if self.dobj_list is None else [dobj.name for dobj in self.dobj_list]

    @property
    def columns_df(self) -> List[str]:
        """
        Returns the names of the columns of the data.
        """
        return ["uid"] + [c for dobj in self.dobj_list for c in dobj.columns_df]

    def get_cols_dobjs(self, attributes_names: Union[str, List[str]], combined: bool = False) -> Union[Tuple[List[DataObject], List[List[str]]], None]:
        """
        In this case, the attributes can be either names of dimensions, or names of
        full data objects, and we need to return the precise column names that correspond
        to the attributes.

        Parameters
        ----------
        attributes_names : Union[str, List[str]]
            The names of valid attributes, that can be either names of dimensions, or names of
            data objects.
        combined : bool, optional, default=False
            If set, the list of DataObject's is unique and the columns are combined.

        Returns
        -------
        Tuple[List[DataObject], List[List[str]]]
            The list of DataObject's and the list of columns of the DataObject's that correspond
            to the attributes. If combined is set, the list of DataObject's is unique and the columns are combined.
        """
        attributes_names = [attributes_names] if isinstance(attributes_names, str) else attributes_names

        dobj_list = []
        cols_list = []
        if set(attributes_names).issubset(self.names_list + self.columns_df):
            for att in attributes_names:
                if att in self.names_list:
                    dobj = [dobj for dobj in self.dobj_list if att == dobj.name][0]
                    cols_list.append(dobj.columns_df)
                elif att in self.columns_df:
                    dobj = [dobj for dobj in self.dobj_list if att in dobj.columns_df][0]
                    cols_list.append([att])
                else:
                    raise AssertionError("This should never happen, since we checked that the attribute names are valid")
                dobj_list.append(dobj)
        else:
            invalid_names = ", ".join(set(attributes_names).difference(self.names_list + self.columns_df))
            raise Exception(f"DataBlock does not have DataObject's or columns with name: {invalid_names}")

        if combined:
            # If combined is True, we combine the columns of the same DataObject, and return a list of unique DataObject's, with combined columns matching the requested attributes
            cols_dict = defaultdict(list)
            for dobj, cols in zip(dobj_list, cols_list):
                cols_dict[dobj.name].extend(cols)

            cols_list = [list_unique(cols) for _, cols in cols_dict.items()]
            dobj_list = self.get_dobjs(list(cols_dict.keys()))

        return dobj_list, cols_list

    def get_dobjs(self, dobj_names: Union[str, List[str]] = None) -> List[DataObject]:
        """
        Returns the data objects. If names is None all DataObjects' are returned.

        Parameters
        ----------
        dobj_names : Union[str, List[str]], optional
            The name or names of DataObject's to return.
        """
        if dobj_names is None:
            return self.dobj_list
        dobj_names = [dobj_names] if isinstance(dobj_names, str) else dobj_names

        if set(dobj_names).issubset(self.names_list):
            return [dobj for dobj in self.dobj_list if dobj.name in dobj_names]
        else:
            invalid_names = ", ".join(set(dobj_names).difference(self.names_list))
            raise Exception(f"DataBlock does not have DataObject's with name: {invalid_names}")

    def get_data_mat(self, dobj_names: Union[str, List[str]] = None, data_mat: np.ndarray = None) -> np.ndarray:
        """
        Returns the data belonging to the requested DataObject's, as a single data matrix.

        Parameters
        ----------
        dobj_names : Union[str, List[str]], optional
            The name or names of DataObject's to consider.
        data_mat : np.ndarray, optional
            The complete data matrix without uid's
        """
        data_mat = data_mat if data_mat is not None else self.data_mat

        if dobj_names is None:
            return data_mat
        else:
            data_mats = self.get_data_mats(dobj_names, data_mat)
            return np.concatenate(data_mats, axis=1)

    def get_data_mat_dtypes(self, dobj_names: Union[str, List[str]] = None) -> List[str]:
        """
        Returns the data types of the columns of the data matrix for the requested DataObject's.

        Parameters
        ----------
        dobj_names: Union[str, List[str]], optional
            The name or names of DataObject's to consider.

        Returns
        -------
        List[str]
            A list of data types.

        """
        return [dobj.dtype for dobj in self.get_dobjs(dobj_names) for _ in range(dobj.dim)]

    def get_data_mats(self, dobj_names: Union[str, List[str]] = None, data_mat: np.ndarray = None) -> List[np.ndarray]:
        """
        Returns the data belonging to the requested DataObject's, as a list of data matrices.

        Parameters
        ----------
        dobj_names : Union[str, List[str]], optional
            The name or names of DataObject's to consider.
        data_mat : np.ndarray, optional
            The complete data matrix without uid's
        """
        data_mat = data_mat if data_mat is not None else self.data_mat
        dobj_names = [dobj_names] if isinstance(dobj_names, str) else dobj_names
        return [data_mat[:, dobj.position_index : dobj.position_index + dobj.dim].astype(dobj.dtype) for dobj in self.get_dobjs(dobj_names)]

    def print_transf(self):
        """
        Prints the applied transformations for the DataBlock.
        """
        print("\n - Transformations and normalizations performed in Data block {}".format(self.display_name))
        self.transformation.print_transf(self.dobj_list)

    def update_obj(self, data: np.ndarray, names: List[str] = None, **kwargs):
        """
        Updates the DataObject instance according to the passed data (e.g., changing its domain or type)

        Parameters
        ----------
        data : np.ndarray
            The data matrix including the uuid.
        names : List[str]
            The names of the DataObject's to update. If None, all DataObject's are updated.
        kwargs
            Arguments passed to the DataObject.update_obj method.
        """
        data = np.asarray(data)[:, 1:]  # Remove uid column
        names = self.names_list if names is None else names
        for da_obj in self.dobj_list:
            if da_obj.name in names:
                da_obj.update_obj(data[:, da_obj.position_index : (da_obj.position_index + da_obj.dim)], **kwargs)

    def check_data_consistency(self, data, **kwargs):
        """
        Checks the data consistency. In particular, checks if the passed data match the DataObjects.

        Parameters
        ----------
        data : np.ndarray
            The data matrix including the uuid.
        kwargs
            Arguments passed to the DataObject.check_data_consistency method.
        """
        data = np.asarray(data)[:, 1:]
        for da_obj in self.dobj_list:
            da_obj.check_data_consistency(data[:, da_obj.position_index : (da_obj.position_index + da_obj.dim)], **kwargs)

    def write(self, df, filename):
        """
        Internal function for writing. Redirects to either pickle or json,
        and also to the specific function of the specific class
        """
        if self.format_file == "pkl":
            self._write_pkl(df, filename)
        elif self.format_file == "json":
            self._write_json(df, filename)
        else:
            raise Exception(f"The file format {self.format_file} is not supported.")

    def read(self, filename):
        """
        Internal function for saving. Redirects to either pickle or json,
        and also to the specific function of the specific class
        """
        if self.format_file == "pkl":
            return self._read_pkl(filename)
        elif self.format_file == "json":
            return self._read_json(filename)
        else:
            raise Exception(f"The file format {self.format_file} is not supported.")

    def print_objects(self):
        """
        Prints the names of the DataObject's.
        """
        print(
            """
        * Data objects names:
            {}
        """.format(
                ", ".join(self.names_list)
            )
        )

    def _check_consistency(self):
        """
        Assess if the dimensions, data types and data ranges of the
        input data matched those indicated by the DataObject instances
        """
        raise NotImplementedError

    @staticmethod
    def _update_dobj_list(dobj_list: List[DataObject]) -> List[DataObject]:
        """
        Updates the DataObject's of the DataBlock. In particular, it splits multidimensional DataObject's, if requested,
        and appends a number to duplicate names. The position and position_index attributes of the DataObject's are also set.
        """

        name_counts = {}
        dobj_list_updated = []
        org_names = [dobj.name for dobj in dobj_list]
        for dobj in dobj_list:
            # Append number to duplicate object names
            if dobj.name in name_counts:
                name_counts[dobj.name] += 1
                name = f"{dobj.name}_{name_counts[dobj.name]}"
            else:
                name = f"{dobj.name}_0" if org_names.count(dobj.name) > 1 else dobj.name  # if there are duplicates append zero to first occurrence
                name_counts[dobj.name] = 0

            # Split multi-dim data objects if requested and object has multiple dim
            if dobj.flag_split_perdim and dobj.dim > 1:
                dobjs_aux = [dobj.copy(name=f"{name}_{i}", dim=1, flag_split_perdim=False) for i in range(dobj.dim)]
            else:
                dobjs_aux = [dobj.copy(name=name, flag_split_perdim=False)]

            dobj_list_updated.extend(dobjs_aux)

        return DataBlock.update_position_indices(dobj_list_updated)

    @staticmethod
    def update_position_indices(dobj_list: List[DataObject]):
        """
        Updates the position and position_index attributes of the DataObject's.
        """
        position_counter = 0
        position_index_counter = 0
        for dobj in dobj_list:
            dobj.position = position_counter
            dobj.position_index = position_index_counter

            position_counter += 1
            position_index_counter += dobj.dim
        return dobj_list

    def info_dobj(self, flag_only_names: bool = False, flag_all_dims: bool = False) -> str:
        """
        Returns information of all the DataObject's of the DataBlock.

        Parameters
        ----------
        flag_only_names: bool, optional, default=False
            If True, only the names of the DataObject's are returned.
        flag_all_dims: bool, optional, default=False
            If True, prints the names of all dimensions for all data objects
        """
        if flag_all_dims:
            all_names = [name for name in self.columns_df if name not in ["uid", "error"]]
            names_and_dim = ['"' + o + '"' for o in all_names]
            return ", ".join(names_and_dim)
        if flag_only_names:
            names_and_dim = ['"' + dobj.name + '"' for dobj in self.dobj_list]
        else:
            names_and_dim = [dobj.name + ": dim " + str(dobj.dim) for dobj in self.dobj_list]
        return ", ".join(names_and_dim)

    def _read_pkl(self, filename):
        """
        Default loading function intended to be used with dataframes.
        """
        return pd.read_pickle(filename)

    def _read_json(self, filename):
        """
        Open data block.
        """
        raise NotImplementedError

    def _write_pkl(self, df, filename):
        """
        Default saving functions intended to be used with dataframes.
        """
        df.to_pickle(filename)

    def _write_json(self, df, filename):
        """
        Save to file.
        """
        raise NotImplementedError

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, dobj_list={self.dobj_list}, transformation={self.transformation})"


class TransformableDataBlock(DataBlock):
    """
    A special data block that is transformable. Does not contain an uid column, and holds no data, it only captures the structure of the data.
    It allows to apply transformation to the data. In particular, it saves the transformed data objects for the inverse transformation.

    Parameters
    ----------
    name : str
        The name of the data block.
    dobj_list : List[DataObject]
        A list of data objects.
    kwargs
        Arguments passed to DataBlock.__init__(...).
    """

    def __init__(self, name: str, dobj_list: List[DataObject], **kwargs):
        super().__init__(name=name, dobj_list=dobj_list, **kwargs)

        # Holds the transformed data objects, initially None. populated by the transform method.
        # The transformed data objects differ from the original data objects in the sense that they have different dimensions.
        self._dobj_list_transf = None

    def to_data_block(self, data: np.ndarray = None, flag_transf: bool = False) -> DataBlock:
        """
        Converts a transformable data block to back to an ordinary data block. A flag controls if the transformed data objects or the original data objects are used.

        Parameters
        ----------
        data : np.ndarray, optional, default=None
            The data matrix to populate the data block with. If provided, the data block is populated with the data.
        flag_transf : bool, optional, default=False
            If set, the transformed data objects are used for the conversion, otherwise the original data objects are used.
        """
        if flag_transf:
            dobj_list = self.dobj_list_transf
        else:
            dobj_list = self.dobj_list

        block = DataBlock(name=self.name, dobj_list=dobj_list, format_file=self.format_file, transformation=self.transformation, display_name=self.display_name)
        if data is not None:
            index = np.arange(len(data)).reshape(len(data), 1)
            data_mat = np.concatenate([index, data], axis=1)
            block.data = pd.DataFrame(data_mat, columns=block.columns_df)

        return block

    @property
    def dobj_list_transf(self):
        """Getter method for the transformed data objects. If no transformation is applied, the original data objects are returned."""
        if self._dobj_list_transf is None:
            return self.dobj_list
        else:
            return self._dobj_list_transf

    def transform(self, data_mat: np.ndarray) -> Tuple[np.ndarray, List[DataObject]]:
        """
        Transforms the data matrix. The transformed data objects are stored internally for inverse transformation.

        Parameters
        ----------
        data_mat : np.ndarray
            The data matrix to transform.

        Returns
        -------
        Tuple[np.ndarray, List[DataObject]]
            A tuple containing two elements, namely, the transformed data matrix and the updated data objects corresponding to the transformed datamatrix.

        """

        data_mat_transf, dobj_list_transf = self.transformation.fit_transform(data_mat, self.dobj_list)  # Fits the transformations, if not already fitted

        # On first call, store the transformed data objects for inverse transformation
        if self._dobj_list_transf is None:
            self._dobj_list_transf = self._update_dobj_list(dobj_list_transf)

        return data_mat_transf, self._dobj_list_transf

    def inverse_transform(self, data_mat: np.ndarray) -> Tuple[np.ndarray, List[DataObject]]:
        """
        Inverse transforms the data matrix.

        Parameters
        ----------
        data_mat : np.ndarray
            The data matrix to inverse transform.

        Returns
        -------
        Tuple[np.ndarray, List[DataObject]]
            A tuple containing two elements, namely, the inversely transformed data matrix and the updated data objects corresponding to the transformed datamatrix.

        """
        return self.transformation.inverse_transform(data_mat, self._dobj_list_transf)

    def transformation_is_fitted(self):
        """
        Returns True if the normalization is fitted.
        """
        return self.transformation.is_fitted()

    @property
    def data(self) -> np.ndarray:
        # Make sure that no data is stored in the TransformableDataBlock
        raise Exception("A transformable data block does not hold data, only the structure of the data.")

    @property
    def columns_df(self) -> List[str]:
        return super().columns_df[1:]

    @property
    def columns_df_transf(self) -> List[str]:
        return [c for dobj in self.dobj_list_transf for c in dobj.columns_df]

    def get_dobj_dimensions(self, flag_transf: bool = False) -> List[int]:
        """
        Returns the dimensions of the data objects. If flag_transf is set, the dimensions of the transformed data objects are returned.

        Parameters
        ----------
        flag_transf : bool, optional
            If set, the dimensions of the transformed data objects are returned.
        """
        if flag_transf:
            return [dobj.dim for dobj in self.dobj_list_transf]
        else:
            return [dobj.dim for dobj in self.dobj_list]


class InputML(TransformableDataBlock):
    """
    A special data block used for the input of the ML model.

    Parameters
    ----------
    name : str, optional
        The name of the data block.
    normalization_class : DataBlockTransformation, optional
        The per data block normalization.
    kwargs
        Arguments passed to super().__init__(...).
    """

    def __init__(self, name: str = "inputML", transformation: DataBlockTransformation = None, **kwargs):
        super().__init__(name=name, flag_split_perdim=False, transformation=transformation, display_name=kwargs.pop("display_name", None) or "Input ML", **kwargs)


class OutputML(TransformableDataBlock):
    """
    A special data block used for the output of the ML model.

    Parameters
    ----------
    name : str, optional
        The name of the data block.
    normalization_class : DataBlockTransformation, optional
        The per data block normalization.
    kwargs
        Arguments passed to super().__init__(...).
    """

    def __init__(
        self,
        name: str = "outputML",
        transformation: DataBlockTransformation = None,
        **kwargs,
    ):
        super().__init__(
            name=name,
            flag_split_perdim=False,
            transformation=transformation,
            display_name=kwargs.pop("display_name", None) or "Output ML",
            **kwargs,
        )


class DesignParameters(DataBlock):
    """
    A data block for design parameters.

    Parameters
    ----------
    name : str, default=dp_long
        The name of the data block.
    display_name : str, optional, default="Design Parameters"
        The display name of the data block. If None it's the same as the `name`.
    kwargs
        Arguments passed to super().__init__(...).
    """

    def __init__(self, name: str = dp_long, **kwargs):
        super().__init__(name=name, display_name=kwargs.pop("display_name", None) or "Design Parameters", **kwargs)


class PerformanceAttributes(DataBlock):
    """
    A data block for design parameters. Additionally, contains an error column at the end of the data.

    Parameters
    ----------
    name : str, optional, default=pa_long
        The name of the data block.
    flag_split_perdim : bool, optional, default=False
        If set, the multidimensional DataObject's are split into multiple DataObject's, one for each dimension.
    display_name : str, optional, default="Performance Attributes"
        The display name of the data block. If None it's the same as the `name`.
    kwargs
        Arguments passed to super().__init__(...).
    """

    def __init__(self, name: str = pa_long, flag_split_perdim: bool = False, **kwargs):
        super().__init__(name=name, flag_split_perdim=flag_split_perdim, display_name=kwargs.pop("display_name", None) or "Performance Attributes", **kwargs)

    @property
    def data_mat(self) -> np.ndarray:
        return np.asarray(self.data)[:, 1:-1]  # Remove uid and error column

    @property
    def columns_df(self) -> List[str]:
        return super().columns_df + ["error"]


class DesignRepresentation(DataBlock):
    """
    Additional types, obtained from the design parameters

    Parameters
    ----------
    name : str
        The name of the data block.
    kwargs
        Arguments passed to super().__init__(...).
    """

    def __init__(self, name="design_rep", **kwargs):
        kwargs["display_name"] = kwargs.get("display_name", "Design Representation")
        super().__init__(name=name, **kwargs)

    @property
    def columns_df(self) -> List[str]:
        if self.format_file == "npz":
            # The columns are not required as the data is saved as a numpy array
            return []
        else:
            return super().columns_df

    def write(self, data, filename):
        """
        Writes the data to a file according to the specified format. Either, pickle, json, npz or png.
        """
        if self.format_file == "npz":
            self._write_npz(data, filename)
        elif self.format_file == "png":
            raise NotImplementedError
        else:
            super().write(data, filename)

    def read(self, filename):
        """
        Reads the data from a file according to the specified format. Either, pickle, json, npz or png.
        """
        if self.format_file == "npz":
            self._read_npz(filename)
        elif self.format_file == "png":
            raise NotImplementedError
        else:
            super().read(filename)

    def _read_npz(self, filename: str) -> np.ndarray:
        """
        Loads a numpy array saved in npz format.
        """
        return np.load(filename)["A"]

    def _write_npz(self, array: np.ndarray, filename: str):
        """
        Saves a numpy array to npz format.
        """
        ud.save_compressed(open(filename, "wb"), A=array)


class DataBlockTransformation:
    """
    Base class to implement DataBlock transformations.
    To implement a custom transformation, inherit from this class and implement the following methods:

    * `transform`: Implements the transformation. If the transformation has state, it can be accessed through the attribute `fitted_values`.
    * `inverse_transform`: Implements the un-transformation. If the transformation has state, it can be accessed through the attribute `fitted_values`.
    * `fit_values` (optional): Required if the has a state that needs to be fitted.

    Attributes
    ----------
    fitted_values : Dict[str, Any]
        Dictionary with the values used for normalization. If None, the normalization is not fitted.
    """

    def __init__(self):
        self.fitted_values = None

    def __jsondump__(self):
        return {}

    @classmethod
    def __jsonload__(cls, data):
        return cls(**data)

    def is_fitted(self) -> bool:
        """Method that returns True if the transformation is fitted."""
        return self.fitted_values is not None

    def fit_values(self, data_mat: np.ndarray, dobj_list: List["DataObject"]) -> Dict[str, Any]:
        """
        Method to override to estimate values used for the transformation, e.g., mean, std, min, max, etc.

        Parameters
        ----------
        data_mat : np.ndarray
            Input data to fit the normalization.
        dobj_list : List[DataObject]
            List of DataObjects in case some extra information is required

        Returns
        -------
        Dict[str, Any]
            Dictionary with the values used for normalization.

        Notes
        -----
        The dictionary returned by this method will be stored in the attribute `fitted_values` when the method `fit` is called.
        """
        return {}

    def fit(self, data_mat: np.ndarray, dobj_list: List["DataObject"]) -> DataBlockTransformation:
        """
        Fits the transformation if not fitted.

        Parameters
        ----------
        data_mat : np.ndarray
            Input data to fit the normalization.
        dobj_list : List[DataObject]
            List of DataObjects in case some extra information is required

        Returns
        -------
        DataBlockTransformation
            The fitted transformation.

        Notes
        -----
        The dictionary returned by the method `fit_values` will be stored in the attribute `fitted_values`.
        """
        self.fitted_values = self.fit_values(data_mat, dobj_list)
        return self

    def fit_transform(self, data_mat: np.ndarray, dobj_list: List["DataObject"]) -> Tuple[np.ndarray, List[DataObject]]:
        """Fits the transformation if not fitted and transforms the input. If already fitted, only transforms the input."""
        if not self.is_fitted():
            return self.fit(data_mat, dobj_list).transform(data_mat, dobj_list)
        else:
            return self.transform(data_mat, dobj_list)

    def transform(self, data_mat: np.ndarray, dobj_list: List["DataObject"]) -> Tuple[np.ndarray, List[DataObject]]:
        """
        Method to implement to transform the input.

        Parameters
        ----------
        data_mat : np.ndarray
            Input data to transform.
        dobj_list : List[DataObject]
            List of DataObjects in case some extra information is required

        Returns
        -------
        Tuple[np.ndarray, List[DataObject]]
            The transformed data and the updated data objects

        """
        raise NotImplementedError

    def inverse_transform(self, data_mat: np.ndarray, dobj_list: List["DataObject"]) -> Tuple[np.ndarray, List[DataObject]]:
        """
        Method to implement to un-transform the input.

        Parameters
        ----------
        data_mat : np.ndarray
            Input data to un-transform.
        dobj_list : List[DataObject]
            List of DataObjects in case some extra information is required

        Returns
        -------
        Tuple[np.ndarray, List[DataObject]]
            The un-transformed data and the updated data objects
        """
        raise NotImplementedError

    @staticmethod
    def print_transf(obj_list: List["DataObject"]):
        """
        Prints and overview of the applied transformations.
        """
        raise NotImplementedError


class DefaultDataBlockTransformation(DataBlockTransformation):
    """
    Implements the default transformation for the DataBlock. The default transformation transforms the data block based on the transformations of the DataObject's.
    """

    def __init__(self):
        super().__init__()
        self._is_fitted = False

    def fit(self, data_mat: np.ndarray, dobj_list: List["DataObject"]) -> DataBlockTransformation:
        self._transform(data_mat, dobj_list, inverse=False, refit=True)
        self._is_fitted = True
        return self

    def is_fitted(self) -> bool:
        return self._is_fitted

    def transform(self, data_mat: np.ndarray, dobj_list: List["DataObject"]) -> Tuple[np.ndarray, List[DataObject]]:
        return self._transform(data_mat, dobj_list, inverse=False)

    def inverse_transform(self, data_mat: np.ndarray, dobj_list: List["DataObject"]) -> Tuple[np.ndarray, List[DataObject]]:
        return self._transform(data_mat, dobj_list, inverse=True)

    @staticmethod
    def _transform(data_mat: np.ndarray, dobj_list: List[DataObject], inverse: bool = False, refit: bool = False) -> Tuple[np.ndarray, List[DataObject]]:
        """
        Helper function that implements the transformation and inverse transformation of the data matrix.

        Parameters
        ----------
        data_mat : np.ndarray, optional
            The input data matrix to be transformed. If not provided, the internal data matrix `self.data_mat`
            will be used for the transformation.
        inverse : bool, optional
            If set, the inverse transformation is performed.

        Returns
        -------
        Tuple[np.ndarray, List[DataObject]]
            A tuple containing two elements, namely, the transformed data matrix and the updated data objects corresponding to the transformed datamatrix.

        """

        data_mats = []
        dobj_list_transformed = []
        for dobj in dobj_list:
            # Apply the per DataObject transform
            start, end = dobj.position_index, (dobj.position_index + dobj.dim)
            if inverse:
                data_mat_sub = dobj.inverse_transform(data_mat[:, start:end])
            else:
                data_mat_sub = dobj.transform(data_mat[:, start:end].astype(dobj.dtype), refit=refit)

            # TODO: maisseal, Check if this is is still needed
            dobj_new = dobj.copy(
                dim=data_mat_sub.shape[1],
                transformations=dobj.transformations,  # no deepcopy
            )  # required since dimension might change after transformation

            data_mats.append(data_mat_sub)
            dobj_list_transformed.append(dobj_new)

        if inverse:
            # Can contain arrays of different types, so we need to specify the type as object
            data_mat_new = np.concatenate(data_mats, axis=1, **{"dtype": object})
        else:
            data_mat_new = np.concatenate(data_mats, axis=1)

        return data_mat_new, DataBlock.update_position_indices(dobj_list_transformed)

    @staticmethod
    def print_transf(dobj_list: List[DataObject]):
        for obj in dobj_list:
            obj.print_transf_norm()
