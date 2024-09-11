import glob
import os
import pickle as pkl
import shutil
import time
import typing
from datetime import datetime
from itertools import chain
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd

import aixd.data.constants as constants
import aixd.data.utils_data as ud
from aixd.data import DataBlock, DesignParameters, DesignRepresentation, PerformanceAttributes
from aixd.data.custom_callbacks import AnalysisCallback, ImportCallback, SamplingCallback
from aixd.data.data_objects import DataObject
from aixd.data.default_importer import csv_importer_callback, df_importer_callback
from aixd.data.encoders import json_dump, json_load
from aixd.data.utils_data import combine_formats, convert_to
from aixd.utils import logs
from aixd.utils.utils import apply_dict, flatten_dict

if typing.TYPE_CHECKING:
    from aixd.sampler.sampler import SamplesGenerator

dp_long = constants.design_par_long
pa_long = constants.perf_attribute_long
dr_long = constants.design_rep_long

logger = logs.get_logger().get_child("dataset")


class Dataset:
    """
    This class manages the Dataset. The data, model checkpoints and other logging information resides in the respective folder/file structure:
     - :code:`{self.datapath}/checkpoints/`
     - :code:`{self.datapath}/design_parameters/`
     - :code:`{self.datapath}/design_representation/`
     - :code:`{self.datapath}/logs/`
     - :code:`{self.datapath}/performance_attributes/`
     - :code:`{self.name}_data.json` (depending on the file format)
     - :code:`{self.name}_data.pkl` (depending on the file format)

    The class handles the import of data and its storing, the loading of data samples, the preparation of the data for the ML-model and more.

    Parameters
    ----------
    name : str
        The name of the dataset.
    design_par : :class:`aixd.data.data_blocks.DesignParameters`, optional, default=None
        Declaration of design parameters.
    perf_attributes : :class:`aixd.data.data_blocks.PerformanceAttributes`, optional, default=None
        Declaration of performance attrbiutes.
    description : str, optional, default=None
        A description of the dataset.
    design_rep : Union[List[DesignRepresentation, Dict[DesignRepresentation]]], optional, default=None
        A list or a dict of design representations.
    root_path : optional, default=current working directory
        Full path to the root of the project.
    overwrite : bool, optional, default=False
        If True, the dataset object will be overwritten.
    file_format : str, optional, default="json"
        Determine the format to use to store the dataset. It can be ``json`` or ``pkl``.
    """

    def __init__(
        self,
        name: str,
        design_par: DesignParameters = None,
        perf_attributes: PerformanceAttributes = None,
        description: str = "",
        design_rep: Union[List[DesignRepresentation], Dict[str, DesignRepresentation]] = None,
        root_path: str = None,
        overwrite: bool = False,
        file_format: str = "json",
    ):
        # Required to check if the dataset already exists
        self.name = name  # Short name, also used for folder, etc.
        self.root_path = root_path if root_path is not None else os.getcwd()
        self.file_format = file_format
        dataset_filepath = os.path.join(self.datapath, self.filename_dataset + "." + self.file_format)

        if os.path.exists(dataset_filepath) and (design_par is not None) and not overwrite:
            logger.warning(
                "Dataset already exists, and it has been reloaded. If this is not the desired behavior:\n"
                "    1. Change the name of the dataset.\n"
                "    2. Specify another root_path\n"
                "    Also, the flag overwrite can be set to True. In that case, the Dataset object will be overwritten."
            )
            self.load_dataset_obj()
        else:
            if overwrite and os.path.exists(dataset_filepath):
                self.load_dataset_obj()
                self._delete_all()

                logger.info("A previous instance of the dataset has been removed")

            self.description = description  # Description of database
            self.datetime = self._get_strtime()  # Datetime of last saving

            self.design_par = design_par  # DataBlock instance with design parameters
            self.perf_attributes = perf_attributes  # DataBlock instance with performance attributes

            # Checking for uniqueness of names
            if self.design_par is not None and self.perf_attributes is not None:
                all_cols = self.design_par.columns_df[1:] + self.perf_attributes.columns_df[1:]
                un_val, un_count = np.unique(all_cols, return_counts=True)
                if (un_count > 1).any():
                    list_wrong = [un_val[i] for i in np.argwhere(un_count > 1).flatten()]
                    list_wrong = ", ".join(list_wrong) if len(list_wrong) < 10 else ", ".join(list_wrong[:10]) + ", ..."
                    raise ValueError(f"Names repeated between design parameters and performance attributes: {list_wrong}")

            if isinstance(design_rep, dict):
                self.design_rep = design_rep  # Dict with additional DataBlocks, i.e. design representations
            elif isinstance(design_rep, list):
                dict_aux = dict()
                for el in design_rep:
                    dict_aux[el.name.replace(" ", "_")] = el
                self.design_rep = dict_aux
            else:
                self.design_rep = dict()

            # Setup paths for the project root, data and log folders
            self._setup_project_folders()

            # Dicts to store all the information of the data already generated
            self.data_gen_dp = {"uid_vector": [], "fileid_vector": [], "samples_perfile_vector": []}
            self.data_gen_pa = {"uid_vector": [], "fileid_vector": [], "samples_perfile_vector": []}
            # One for each object, as we can compute them differently
            if len(self.design_rep.keys()):
                self.data_gen_dr = dict()
                for key in self.design_rep.keys():
                    self.data_gen_dr[key] = {"uid_vector": [], "fileid_vector": [], "samples_perfile_vector": []}

    def __jsondump__(self):
        return {
            "name": self.name,
            "description": self.description,
            "design_par": self.design_par,
            "perf_attributes": self.perf_attributes,
            "design_rep": self.design_rep,
            "file_format": self.file_format,
            "data_gen_dp": self.data_gen_dp if hasattr(self, "data_gen_dp") else None,
            "data_gen_pa": self.data_gen_pa if hasattr(self, "data_gen_pa") else None,
        }

    @classmethod
    def __jsonload__(cls, data):
        dataset = cls.__new__(cls)
        dataset.__dict__.update(data)
        return dataset

    @property
    def filename_dataset(self):
        """A standard file name of the serialized Dataset object: :code:`{filename_dataset}.pkl` and :code:`{filename_dataset}.json`."""
        return "dataset_object"

    @property
    def datapath(self):
        """Full path to this dataset's folder: :code:`{root_path}/{name}`."""
        return os.path.join(self.root_path, self.name.replace(" ", "_"))

    @property
    def file_format(self):
        return self._file_format

    @file_format.setter
    def file_format(self, value):
        if value not in ("json", "pkl"):
            raise ValueError(f"Invalid file format: {value}. Choose from 'json' or 'pkl'")
        self._file_format = value

    def summary_dataobjects(self, flag_print: bool = True) -> Tuple[str, None]:
        """
        More detailed summary of the data objects.

        Parameters
        ----------
        flag_print : bool, optional, default=True
            It True, the summary is printed to the console. Otherwise, it is returned as a string.

        Returns
        -------
        Tuple[str, None]
            If :code:`flag_print=True`, the summary is printed to the console. Otherwise, it is returned as a string.
        """
        str_print = "### Details of data objects in the dataset\n\n"
        str_print += "Design parameters\n"
        str_print += "-----------------------\n"
        aux = [("   " + str(o) + "\n") for o in self.design_par.dobj_list]
        str_print += "".join(aux)
        str_print += "\nPerformance attributes\n"
        str_print += "-----------------------\n"
        aux = [("   " + str(o) + "\n") for o in self.perf_attributes.dobj_list]
        str_print += "".join(aux)
        if len(self.design_rep.keys()):
            str_print += "\nDesign representation\n"
            str_print += "-----------------------\n"
            for key in self.design_rep.keys():
                str_print += "   " + str(key) + "\n"
                aux = [("   " + str(o) + "\n") for o in self.design_rep[key].dobj_list]
                str_print += "".join(aux)
        if flag_print:
            print(str_print)
        else:
            return str_print

    def _setup_project_folders(self):
        """Creates (if not existing) all folders and subfolders for this dataset. Checks consistency of the data if folders already exist. Sets up loggers."""

        # Define all paths
        folders = [self.datapath]
        subfolders = [os.path.join(self.datapath, f) for f in [dp_long, pa_long, dr_long, "logs"]]
        subsubfolders = [os.path.join(self.datapath, dr_long, key) for key in self.design_rep.keys()]

        # Iterate through paths and create folders if they do not exist
        for path in folders + subfolders + subsubfolders:
            os.makedirs(path, exist_ok=True)

    def summary_datablocks(self, flag_print: bool = True) -> Tuple[str, None]:
        """
        Short summary of the data blocks in the dataset, and the data objects they contain.

        Parameters
        ----------
        flag_print : bool, optional, default=True
            It True, the summary is printed to the console. Otherwise, it is returned as a string.

        Returns
        -------
        Tuple[str, None]
            If :code:`flag_print=True`, the summary is printed to the console. Otherwise, it is returned as a string.
        """
        str_print = "### Data blocks and elements in original dataset\n\n"
        str_print += "Design parameters\n"
        str_print += "-----------------------\n"
        str_print += "     {}\n".format(self.design_par.info_dobj(False))
        str_print += "\nPerformance attributes\n"
        str_print += "-----------------------\n"
        str_print += "     {}\n".format(self.perf_attributes.info_dobj(False))
        if len(self.design_rep.keys()):
            str_print += "\nDesign representation\n"
            str_print += "-----------------------\n"
            for key in self.design_rep.keys():
                str_print += "   " + str(key) + "\n"
                str_print += "     {}".format(self.design_rep[key].info_dobj(False))
        if flag_print:
            print(str_print)
        else:
            return str_print

    def _get_strtime(self, format="%d.%m.%y-%HH:%MM:%SS"):
        return datetime.strftime(datetime.now(), format=format)

    def save_dataset_obj(self):
        """Writes the Dataset object to a disk. The format is defined by the :code:`file_format` attribute. Location of the files is given by the :code:`datapath`."""
        # filename_dataset = os.path.join(self.datapath, self.filename_dataset)
        filename_dataset = os.path.join(self.datapath, f"{self.filename_dataset}.{self.file_format}")

        # Copy without data on data blocks and save as pickle, and save as pickle
        copy_self = ud.copy_without_data(self)
        copy_self.datetime = self._get_strtime()
        copy_self.root_path = None  # remove local path

        if self.file_format == "pkl":
            pkl.dump(copy_self, open(filename_dataset, "wb"))
        elif self.file_format == "json":
            json_dump(copy_self, filename_dataset, pretty=False)
        logger.info(f"Dataset object is saved at {filename_dataset}")

    def load_dataset_obj(self):
        """Loads the serialized Dataset object."""
        root_path = self.root_path
        filename_dataset = os.path.join(self.datapath, f"{self.filename_dataset}.{self.file_format}")
        name = self.name  # keep the current name in case the dataset has been saved with a different one to prevent mismatch

        if os.path.exists(filename_dataset):
            if self.file_format == "pkl":
                aux_obj = pkl.load(open(filename_dataset, "rb"))
            elif self.file_format == "json":
                aux_obj = json_load(filename_dataset)

            self.__dict__.update(aux_obj.__dict__)
            self.root_path = root_path  # re-set current path as it has been overwritten
            self.name = name
            name = self.name.replace(" ", "_")
            logger.info(f"Correctly loaded Dataset instance with name {name}")
        else:
            logger.warning(f"No files exist for this dataset with name {self.filename_dataset}")

    @classmethod
    def from_dataset_object(cls, filepath: str) -> "Dataset":
        """
        Loads a Dataset object from a serialized file.

        Parameters
        ----------
        filepath : str
            Full path to the pickle-serialized Dataset object. The root path of this file will be used as the root_path/datapath of the new Dataset object.

        Returns
        -------
        Dataset
            The loaded Dataset object.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Failed to load a dataset object: File {filepath} does not exist")

        root_path = os.path.dirname(os.path.dirname(filepath))
        name = os.path.basename(os.path.dirname(filepath))

        if filepath.endswith(".json"):
            dataset = json_load(filepath)
        else:
            with open(filepath, "rb") as f:
                dataset = pkl.load(f)

        dataset.root_path = root_path
        dataset.name = name

        logger.info(f"Correctly created Dataset instance with name {name}")

        return dataset

    def check_data_consistency(self, **kwargs):
        """
        Checks the consistency of the data objects in the dataset, when compared to the data contained in the dataset. This essentially checks if the domain specified
        for the data objects matches the true domain in the data.

        Parameters
        ----------
        **kwargs
            Keyword arguments to be passed to the `DataBlock.check_data_consistency` method.
        """
        for block in flatten_dict(self.data_blocks):
            block.check_data_consistency(block.data, **kwargs)

    def update_obj_domains(self, names: List[str] = None, flag_only_perfatt: bool = False, **kwargs):
        """
        Updates the domains of the data objects in the dataset, when compared to the
        data contained in the dataset. For `Interval` domain, this updates the min and
        max values. While for `Option` domain, this updates the list of options, `array`.

        Parameters
        ----------
        names : list, optional, default=[]
            List of names of data objects to update. If empty, all data objects are updated.
        flag_only_perfatt : bool, optional, default=False
            If True, only the performance attributes are updated. Otherwise, all data objects are updated.
        """
        data_blocks = flatten_dict(self.data_blocks)
        data_blocks = [block for block in data_blocks if isinstance(block, PerformanceAttributes)] if flag_only_perfatt else data_blocks

        for block in data_blocks:
            block.update_obj(block.data, names, **kwargs)

        self.save_dataset_obj()

    @property
    def data(self) -> dict:
        """
        Returns
        -------
        dict
              two-level nested dictionary containing the data of :class:`DataBlock` instances.
        """
        return apply_dict(self.data_blocks, func=lambda block: block.data)

    @property
    def data_mats(self) -> Dict[str, Union[np.ndarray, Dict[str, np.ndarray]]]:
        """
        Returns
        -------
        Dict[str, Union[np.ndarray, Dict[str, np.ndarray]]]
              two-level nested dictionary containing the data matrices of :class:`DataBlock` instances.
        """
        return apply_dict(self.data_blocks, func=lambda block: block.data_mat)

    @property
    def data_blocks(self) -> Dict[str, Union[DataBlock, Dict[str, DataBlock]]]:
        """
        This method constructs a dictionary that represents the data blocks in the dataset. The keys in the returned dictionary are strings representing the block names.
        The possible block names are: 'design_parameters', 'performance_attributes', and 'design_representation'.

        Returns
        -------
        Dict[str, Union[DataBlock, Dict[str, DataBlock]]]
              two-level nested dictionary containing the :class:`DataBlock` instances of the dataset.

        Example
        -------
        >>> # Assuming all data blocks are defined in the dataset object.
        >>> result = dataset.data_blocks() # doctest: +SKIP
        >>> print(result) # doctest: +SKIP
        {
            'design_parameters': DesignParameters(...),                 # corresponds to self.design_par
            'performance_attributes': PerformanceAttriubtes(...),       # corresponds to self.perf_attributes
            'design_representation': {                                  # corresponds to self.design_rep
                    'repr_1': DesignRepresentation(...),
                    'repr_2': DesignRepresentation(...),
                        ...
                }
        }
        """
        dict_blocks = {
            dp_long: self.design_par,
            pa_long: self.perf_attributes,
        }
        if len(self.design_rep.keys()):
            dict_blocks[dr_long] = self.design_rep
        return dict_blocks

    @property
    def data_objects(self) -> List[DataObject]:
        """
        Returns all the data objects of the data blocks in the dataset. This includes the data objects of the design parameters, performance attributes and design representation.
        """
        return list(chain(*flatten_dict(apply_dict(self.data_blocks, lambda block: block.dobj_list))))

    def get_data_objects_by_name(self, names: List[str]) -> List[DataObject]:
        """
        Finds and returns data objects with the specified name(s) in the given dataset.

        Parameters:
        -----------
        names : List[str]
            List of names of data objects.

        Returns:
        --------
        List[DataObject]
            List with all matching data objects.

        """
        return [obj for obj in self.data_objects if obj.name in names]

    def data_mat_with_dobjs(self, blocks: List[str] = None, dobj_names: Optional[List[str]] = None, flag_transf=True) -> Tuple[np.array, List[DataObject]]:
        """
        Picking the objects from the design parameters, performance_attributes and design representation according to list of names. Returns a new dobj_list with
        a corresponding data matrix. If blocks is None all blocks are considered. If dobj_names is None all DataObjects of specified blocks are returned.

        Parameters
        ----------
        blocks : List[str], optional
            Specifies which type of data blocks to include, possible strings are ["design_parameters", "performance_attributes", "design_representation"].
        dobj_names : List[str], optional
            Names of the requested data objects.
        flag_transf : bool, optional
            Flag to enable transformation of the data.

        Returns
        -------
        Tuple[np.array, List[DataObject]]
            The data matrix with a corresponding list of data objects.

        """

        # Pick the blocks
        if blocks is not None:
            data_blocks = {key: value for key, value in self.data_blocks if key in blocks}

            blocks_notfound = set(self.data_blocks.keys()).difference(blocks)
            if len(blocks_notfound) > 0:
                logger.warning(f"The following blacks were not found:\n{', '.join(blocks_notfound)}")
        else:
            data_blocks = self.data_blocks

        # Pick the data objects
        if dobj_names is not None:
            dobjs_with_data_nested_dict = apply_dict(data_blocks, lambda block: (block.data_mat, [dobj for dobj in block.dobj_list if dobj.name in dobj_names]))

            # Report names that where not found
            all_names = list(chain(*flatten_dict(apply_dict(data_blocks, lambda block: block.names_list))))
            names_notfound = [name for name in dobj_names if name not in all_names]
            if len(names_notfound) > 0:
                logger.warning(f"The following elements were not found:\n{', '.join(names_notfound)}")

        else:
            dobjs_with_data_nested_dict = apply_dict(data_blocks, lambda block: (block.data_mat, block.dobj_list))

        data_mats = []
        dobj_list_new = []
        for data_mat, dobj_list in flatten_dict(dobjs_with_data_nested_dict):
            for dobj in dobj_list:
                data_mat_sub = data_mat[:, dobj.position_index : dobj.position_index + dobj.dim]
                if flag_transf:
                    data_mat_sub = dobj.transform(data_mat_sub)

                dobj_new = dobj.copy(dim=data_mat_sub.shape[1])  # required since dimension might change after transformation
                data_mats.append(data_mat_sub)
                dobj_list_new.append(dobj_new)

        data_mat = np.concatenate(data_mats, axis=1) if len(data_mats) > 0 else np.array([])

        return data_mat, dobj_list_new

    """
    Methods for handling the data
    """

    def load(self, n_samples=None, flag_random=False, flag_noerror=True, design_rep_toload=[]):
        """
        Load the data into the dataset object. There is the option to just load some
        of the stored stuff. Also, we need to explicitly indicate the design representation
        to load, if not none are loaded

        Parameters
        ----------
        n_samples : int, optional, default=None
            Number of samples to load. If None, all samples are loaded.
        flag_random : bool, optional, default=False
            Random samples from all the available ones are loaded. If False, the files
            are used in order.
        flag_noerror : bool, optional, default=True
            Only samples with no error on the analysis are loaded.
        design_rep_toload : list, optional, default=[]
            List of design representations to load. If empty, none are loaded.
        """
        if not len(self.data_gen_dp["uid_vector"]):
            logger.warning('There is not register of data. Run "info_data" to assess the present data')

        else:
            id_to_open = self.data_gen_dp["fileid_vector"]
            tic = time.time()
            if (n_samples is not None) and (n_samples > 0):
                aux_samples = np.cumsum(self.data_gen_dp["samples_perfile_vector"])
                ind_min = np.argwhere(aux_samples >= n_samples).flatten()
                if not len(ind_min):
                    ind_min = len(aux_samples)
                else:
                    ind_min = ind_min[0]
                ind_min += 1
                if flag_random:
                    id_to_open = self.data_gen_dp["fileid_vector"][np.random.permutation(len(aux_samples))[:ind_min]]
                else:
                    id_to_open = self.data_gen_dp["fileid_vector"][:ind_min]

            files_list = self._name_files(id_to_open)
            dp_mat = []
            pa_mat = []
            pa_not_open = []
            for filename in files_list[dp_long]:
                dp_mat.append(self.design_par.read(filename))
            for filename in files_list[pa_long]:
                if os.path.exists(filename):
                    pa_mat.append(self.perf_attributes.read(filename))
                else:
                    pa_not_open.append(str(ud.fileid_int(filename, constants.perf_attribute_file)[0]))

            dp_mat = pd.concat(dp_mat)
            if len(pa_mat):
                pa_mat = pd.concat(pa_mat)

            if len(pa_not_open):
                logger.warning(f"The following files of perf. attributes do not exist: {', '.join(pa_not_open)}")
                flag_noerror = False
            else:
                vec_errors = np.zeros(len(pa_mat))
                if flag_noerror:
                    vec_errors = np.asarray(pa_mat["error"])

                dp_mat = dp_mat.iloc[(vec_errors == 0)].reset_index()
                if len(pa_mat):
                    pa_mat = pa_mat.iloc[(vec_errors == 0)].reset_index()

            self.design_par.data = dp_mat
            if len(pa_mat):
                self.perf_attributes.data = pa_mat

            logger.info(f"Loaded a total of {len(self.design_par.data)} samples from {len(id_to_open)} files in {time.time() - tic} seconds")

            if flag_noerror:
                logger.warning(f"{np.sum(vec_errors)} samples discarded as they could not be analyzed correctly")

            # Loading now design representations
            if len(design_rep_toload):
                files_list_dr = self._name_files_dr(id_to_open)
                for key in design_rep_toload:
                    if key in self.design_rep.keys():
                        d_type = self.design_rep[key].dobj_list[0].dtype
                        dr_mat = []
                        dr_mat_not_open = []
                        for filename in files_list_dr[key]:
                            if os.path.exists(filename):
                                aux_mat = self.design_rep[key].read(filename)
                                if self.design_rep[key].format_file == "npz":
                                    aux_mat = aux_mat.astype(eval("np.{}".format(d_type)))
                                dr_mat.append(aux_mat)
                            else:
                                dr_mat_not_open.append(str(ud.fileid_int(filename, constants.design_rep_file)[0]))
                        if self.design_rep[key].format_file == "npz":
                            self.design_rep[key].data = np.concatenate(dr_mat, axis=0)[(vec_errors == 0)].astype(eval("np.{}".format(d_type)))
                        else:
                            self.design_rep[key].data = pd.concat(dr_mat).iloc[(vec_errors == 0)].reset_index()
                        logger.info(f"Also loaded design representation keys: {', '.join(design_rep_toload)}")

    def _name_files(self, id_list, flag_existing=False):
        """Auxiliary function to obtain a list of existing files with data"""
        fmts = [self.design_par.format_file, self.perf_attributes.format_file]
        if not isinstance(id_list, list):
            id_list = list(id_list)

        files_list = dict()
        folder_path = self.datapath
        if flag_existing:
            for folder, name_file, fmt in zip([dp_long, pa_long], [constants.design_par_file, constants.perf_attribute_file], fmts):
                vec_files = glob.glob(os.path.join(folder_path, folder, name_file + "*." + fmt))
                vec_files.sort()
                files_list[folder] = vec_files
        else:
            vec_dp = []
            vec_pa = []
            for fileid in id_list:
                fileid_str = ud.fileid_str(fileid)
                vec_dp.append(os.path.join(folder_path, dp_long, constants.design_par_file + "_" + fileid_str + "." + fmts[0]))
                vec_pa.append(os.path.join(folder_path, pa_long, constants.perf_attribute_file + "_" + fileid_str + "." + fmts[1]))
            files_list = {dp_long: vec_dp, pa_long: vec_pa}
        return files_list

    def _name_files_dr(self, id_list, flag_existing=False):
        """Auxiliary function to obtain a list of existing files with data, for a given design representation"""
        fmts = [self.design_rep[key].format_file for key in self.design_rep.keys()]
        folders_dr = list(self.design_rep.keys())
        if not isinstance(id_list, list):
            id_list = list(id_list)

        files_list = dict()
        folder_path = os.path.join(self.datapath, dr_long)
        if flag_existing:
            for folder, fmt in zip(folders_dr, fmts):
                vec_files = glob.glob(os.path.join(folder_path, folder, constants.design_rep_file + "*." + fmt))
                vec_files.sort()
                files_list[folder] = vec_files
        else:
            for ind, folder in enumerate(folders_dr):
                vec_dr = []
                for fileid in id_list:
                    fileid_str = ud.fileid_str(fileid)
                    vec_dr.append(os.path.join(folder_path, folder, constants.design_rep_file + "_" + fileid_str + "." + fmts[ind]))
                files_list[folder] = vec_dr
        return files_list

    def check_dataset_consistency(self, regenerate_index=False):
        """
        Assess the correctness of indexes and files for consistency.

        There can be the following inconsistencies:

            1. Indexes do not correspond with the stored files (within DesignObject)
            2. Indexes and/or files do not match between dp and pa (between DesignObjects)
            3. Number of samples or uids are different in the indexes (between)

        Solutions:

            * For 1, we just update all indexes: uids, fileids and number_of_samples
            * For 2, it is ok if the existing matches also match in uids and number of files,
              and the problem are missign pa files, this is just because we have not analyzed all
            * If same fileids contain different uids or number of samples, the best is to regenerate all

        Parameters
        ----------
        regenerate_index : bool, optional, default=False
            Whether to regenerate the index or not. TO BE IMPLEMENTED
        """
        files_list = self._name_files([], flag_existing=True)
        files_list_dr = self._name_files_dr([], flag_existing=True)
        if len(files_list_dr):
            files_list[dr_long] = files_list_dr
        # We check first for 1, and update file ids if required
        vec_ids_mismatch, vec_ids_mismatch_uiddiff, _, error = self._check_file_ids()
        if error:
            for key in vec_ids_mismatch.keys():
                if len(vec_ids_mismatch[key]) or len(vec_ids_mismatch_uiddiff[key]):
                    logger.info("Updated file ids for {}!".format(key.replace("_", " ")))
                    if key == dp_long:
                        self.data_gen_dp["fileid_vector"] = ud.fileid_int(files_list[key], constants.design_par_file)
                    elif key == pa_long:
                        self.data_gen_pa["fileid_vector"] = ud.fileid_int(files_list[key], constants.perf_attribute_file)
                    elif key == dr_long:
                        for key_dr in files_list[dr_long].keys():
                            self.data_gen_dr[key_dr]["fileid_vector"] = ud.fileid_int(
                                files_list[key][key_dr], constants.design_rep_file, format=self.design_rep[key_dr].format_file
                            )

        # For each file, we check the uid vector and number of samples
        for key in [dp_long, pa_long]:
            tot_uid_vector = []
            error = 0
            for ind, filename in enumerate(files_list[key]):
                df_aux = pd.read_pickle(filename)
                tot_uid_vector.extend(list(df_aux["uid"]))
                if key == dp_long:
                    if len(files_list[key]) != len(self.data_gen_dp["samples_perfile_vector"]):
                        self.data_gen_dp["samples_perfile_vector"] = list(np.zeros(len(files_list[key])).astype(int))
                    if self.data_gen_dp["samples_perfile_vector"][ind] != len(df_aux):
                        self.data_gen_dp["samples_perfile_vector"][ind] = len(df_aux)
                        error = 1
                elif key == pa_long:
                    if len(files_list[key]) != len(self.data_gen_pa["samples_perfile_vector"]):
                        self.data_gen_pa["samples_perfile_vector"] = list(np.zeros(len(files_list[key])).astype(int))
                    if self.data_gen_pa["samples_perfile_vector"][ind] != len(df_aux):
                        self.data_gen_pa["samples_perfile_vector"][ind] = len(df_aux)
                        error = 1

            if error:
                logger.info(f"Updated number of samples for {key.replace('_', ' ')}")

            if key == dp_long:
                # if (len(np.setdiff1d(tot_uid_vector, self.data_gen_dp['uid_vector'])) or
                #    len(np.setdiff1d(self.data_gen_dp['uid_vector'], tot_uid_vector))):
                if len(ud.setdiff_sym(tot_uid_vector, self.data_gen_dp["uid_vector"])):
                    logger.info("Updating uid vector for design parameters")

                    self.data_gen_dp["uid_vector"] = tot_uid_vector
            elif key == pa_long:
                # if (len(np.setdiff1d(tot_uid_vector, self.data_gen_pa['uid_vector'])) or
                #    len(np.setdiff1d(self.data_gen_pa['uid_vector'], tot_uid_vector))):
                if len(ud.setdiff_sym(tot_uid_vector, self.data_gen_pa["uid_vector"])):
                    logger.info("Updating uid vector for performance attributes")

                    self.data_gen_pa["uid_vector"] = tot_uid_vector

        # For each file, we check the uid vector and number of samples
        if len(self.design_rep):
            for key in files_list[dr_long].keys():
                tot_uid_vector = []
                error = 0
                for ind, filename in enumerate(files_list[dr_long][key]):
                    df_aux = self.design_rep[key].read(filename)
                    if self.design_rep[key].format_file.replace(".", "") == "pkl":
                        tot_uid_vector.extend(list(df_aux["uid"]))

                    if len(files_list[dr_long][key]) != len(self.data_gen_dr[key]["samples_perfile_vector"]):
                        self.data_gen_dr[key]["samples_perfile_vector"] = list(np.zeros(len(files_list[dr_long][key])).astype(int))
                    if self.data_gen_dr[key]["samples_perfile_vector"][ind] != len(df_aux):
                        self.data_gen_dr[key]["samples_perfile_vector"][ind] = len(df_aux)
                        error = 1
                if error:
                    logger.info(f"Updated number of samples for design representation {key.replace('_', ' ')}!")

                if self.design_rep[key].format_file.replace(".", "") == "npz":
                    tot_uid_vector = self.data_gen_pa["uid_vector"]

                if len(ud.setdiff_sym(tot_uid_vector, self.data_gen_dr[key]["uid_vector"])):
                    logger.info("Updating uid vector for performance attributes")

                    self.data_gen_dr[key]["uid_vector"] = tot_uid_vector

        # Number of files between performance attributes and design par
        error_regen = 0
        if len(self.data_gen_dp["fileid_vector"]) > len(self.data_gen_pa["fileid_vector"]):
            logger.warning("There are still samples that have not been analyzed")

        elif len(self.data_gen_dp["fileid_vector"]) < len(self.data_gen_pa["fileid_vector"]):
            logger.warning("There are more performance attribute samples than design parameter samples")

            error_regen = 1

        # The correspondence of uid vector and samples number between dp and pa
        ind_common = np.intersect1d(self.data_gen_dp["fileid_vector"], self.data_gen_pa["fileid_vector"])
        files_list = self._name_files(ind_common)
        if not error_regen and len(files_list[dp_long]):
            error_regen = 0
            for filedp, filepa in zip(files_list[dp_long], files_list[pa_long]):
                df_dp = pd.read_pickle(filedp)
                df_pa = pd.read_pickle(filepa)
                dp_vec = list(df_dp["uid"])
                pa_vec = list(df_pa["uid"])
                if len(np.setdiff1d(dp_vec, pa_vec)) or len(np.setdiff1d(pa_vec, dp_vec)):
                    logger.warning("* There is a mismatch between uids and files, hence, there has been a problem at some point during the analysis or creation of the dataset")

                    error_regen = 1
                    break

        # TODO regeneration of samples

    def _check_file_ids(self):
        """
        Part of the consistency checks. Just to check if the fileids of the file
        correspond to the ones stored in the info dictionaries
        TODO incorporate check for design rep
        """
        files_list = self._name_files([], flag_existing=True)

        return ud.check_file_ids(files_list, self.data_gen_dp, self.data_gen_pa)

    def _check_file_ids_dr(self):
        """
        Part of the consistency checks. Just to check if the fileids of the file
        correspond to the ones stored in the info dictionaries
        """
        files_list = self._name_files_dr([], flag_existing=True)

        return ud.check_file_ids_dr(files_list, self.data_gen_dr)

    def summary_data(self, flag_print: bool = True) -> Tuple[str, None]:
        """
        Report with information, such as:
        - Loadable data contained
        - Number of samples, and number of files, sampling campaigns
        - If design parameters and performances attributes are correctly
          aligned by their uid

        Parameters
        ----------
        flag_print : bool, optional, default=True
            It True, the summary is printed to the console. Otherwise, it is returned as a string.

        Returns
        -------
        Tuple[str, None]
            If :code:`flag_print=True`, the summary is printed to the console. Otherwise, it is returned as a string.
        """
        # TODO incorporate info for design rep
        if not len(self.data_gen_dp["fileid_vector"]):
            info_files_dp = [0, 0]
        else:
            info_files_dp = [len(self.data_gen_dp["fileid_vector"]), np.sum(self.data_gen_dp["samples_perfile_vector"])]
        if not len(self.data_gen_pa["fileid_vector"]):
            info_files_pa = [0, 0]
        else:
            info_files_pa = [len(self.data_gen_pa["fileid_vector"]), np.sum(self.data_gen_pa["samples_perfile_vector"])]
        if info_files_pa[0] or info_files_dp[0]:
            # if (not len(np.setdiff1d(self.data_gen_pa["fileid_vector"], self.data_gen_dp["fileid_vector"])) and
            #    not len(np.setdiff1d(self.data_gen_pa["uid_vector"], self.data_gen_dp["uid_vector"]))):
            if not len(ud.setdiff_sym(self.data_gen_pa["fileid_vector"], self.data_gen_dp["fileid_vector"])) and not len(
                ud.setdiff_sym(self.data_gen_pa["uid_vector"], self.data_gen_dp["uid_vector"])
            ):
                string1 = "- There is a full correspondence for the design parameters files and samples"
                string2 = "    * Total of {} files and {} samples".format(info_files_dp[0], info_files_dp[1])
            else:
                string1 = "- There is a mismatch between files and uids."
                string2 = """    * Design pararameters: {} files and {} samples
                * Performance attributes: {} files and {} samples""".format(
                    info_files_dp[0], info_files_dp[1], info_files_pa[0], info_files_pa[1]
                )
        else:
            string1 = "- There are no files, and hence no samples, in the indexes"
            string2 = ""

        # Checking the corresponde between files in the folders and uids
        _, _, string_msg, error = self._check_file_ids()
        # We need a vector file to store the number of samples per file
        str_all = "\n* Information of the current dataset\n    - The files of the dataset are stored in: {}\n    {}\n    {}\n    {}".format(
            self.datapath, string1, string2, string_msg
        )
        if flag_print:
            print(str_all)
        else:
            return str_all

    def import_data_from_csv(self, file_path: str, custom_mapping: Dict[str, Union[str, List[str]]] = None) -> None:
        """
        Import data from a csv file into the dataset.

        Parameters
        ----------
        file_path : str
            Path to the csv file.
        custom_mapping : Dict[str, Union[str, List[str]]], optional
            A dictionary mapping the names of DataObjects in the Dataset to the names of the columns in the CSV file. For multidimensional DataObjects, a list of column names can
            be provided. If None, the names of the DataObjects must match the names of the columns in CSV file.

        Notes
        -----
        See :func:`aixd.data.default_importer.df_importer` for more information.
        """
        self.import_data(callbacks_class=csv_importer_callback(self), file_path=file_path, custom_mapping=custom_mapping)

    def import_data_from_df(self, data: pd.DataFrame, custom_mapping: Dict[str, Union[str, List[str]]] = None, samples_perfile: int = 1000, flag_fromscratch: bool = False) -> None:
        """
        Import data from a pandas dataframe into the dataset.

        Parameters
        ----------
        data : pd.DataFrame
            The dataframe containing the data to be imported.
        custom_mapping : Dict[str, Union[str, List[str]]], optional
            A dictionary mapping the names of DataObjects in the Dataset to the names of the columns in the dataframe. For multidimensional DataObjects, a list of column names can
            be provided. If None, the names of the DataObjects must match the names of the columns in the dataframe.

        Notes
        -----
        See :func:`aixd.data.default_importer.df_importer` for more information.
        """
        self.import_data(callbacks_class=df_importer_callback(self), data=data, samples_perfile=samples_perfile, flag_fromscratch=flag_fromscratch, custom_mapping=custom_mapping)

    def import_data(
        self, samples_perfile: int = 1000, n_shards: int = 1, n_samples_toimport: int = None, flag_fromscratch: bool = False, callbacks_class: ImportCallback = None, **kwargs
    ):
        """
        Import data.

        To import some data from other files, with different format.
        The callbacks_class is taking CARE of all the conversion to a numpy array
        that needs to fulfill:

            - Same number of columns that those specified with the design_par,
              performance_att and desig_rep definition
            - Needs to provide a dict with design_rep, performance_att, and design_rep
              (if that exists)
            - It can open the files in batches, in case the dataset to import is
              quite large

        The following is not checked:

            - Data types of the columns, or intervals. Though can be updated later!

        More considerations:

            - NEW files are created and stored in the repo, with the indicated folder structure
            - The uids are resetted
            - The internal variables to track are updated
            - In the new dataset also different files can be created with a
              specified amount of samples

        Parameters
        ----------
        samples_perfile : int, optional, default=1000
            Number of samples per file to store the data
        n_shards : int, optional, default=1
            Defins in how many batches the data is going to be opened. It has to be
            allowed by the ``callbacks_class`` functions.
        n_samples_toimport : _type_, optional, default=None
            Out of the total number of samples available, the number of samples to import
        callbacks_class : _type_, optional, default=None
            Required callbacks to import the data. If None, no data is imported.
        flag_fromscratch : bool, optional, default=False
            If True, all existing files are deleted and the data is imported from scratch.
        """

        def mat_to_df(n_samples, cols, mat, uid_start):
            if isinstance(mat, pd.DataFrame):
                mat = np.asarray(mat)
            mat_samp = np.zeros((n_samples, len(cols))).astype(object)
            mat_samp[:, 0] = np.arange(uid_start, uid_start + n_samples).astype(int)
            # This also compensates for the error column if it has not been added
            mat_samp[:n_samples, 1 : (mat.shape[1] + 1)] = mat[:n_samples, :]
            df = pd.DataFrame(mat_samp, columns=cols)
            return df

        if (
            not len(ud.setdiff_sym(self.data_gen_pa["fileid_vector"], self.data_gen_dp["fileid_vector"]))
            and not len(ud.setdiff_sym(self.data_gen_pa["uid_vector"], self.data_gen_dp["uid_vector"]))
        ) or flag_fromscratch:
            if flag_fromscratch:
                self._delete_all()

                logger.warning("All existing files have been deleted. Starting from scratch")

            if callbacks_class is not None:
                # Functions are executed in order
                tot_samples_imported = 0
                for ind_shard in range(n_shards):
                    vec_shards = [ind_shard, n_shards]
                    if not len(self.data_gen_dp["uid_vector"]):
                        uid_start = 0
                        fileid_start = 0
                    else:
                        uid_start = self.data_gen_dp["uid_vector"][-1] + 1
                        fileid_start = self.data_gen_dp["fileid_vector"][-1] + 1

                    dict_data = callbacks_class.run(vec_shards=vec_shards, **kwargs)

                    if n_samples_toimport is None:
                        n_samples = len(dict_data[dp_long])
                    else:
                        n_samples = np.min([n_samples_toimport - tot_samples_imported, len(dict_data[dp_long])])

                    n_files = np.ceil(n_samples / samples_perfile).astype(int)

                    # Saving design parameters
                    if not len(self.data_gen_dp["uid_vector"]):
                        uid_start = 0
                        fileid_start = 0
                    else:
                        uid_start = self.data_gen_dp["uid_vector"][-1] + 1
                        fileid_start = self.data_gen_dp["fileid_vector"][-1] + 1

                    df = mat_to_df(n_samples, self.design_par.columns_df, dict_data[dp_long], uid_start)
                    self._write_it(df, n_files, samples_perfile, list(df["uid"]), fileid_start, vec_info="data_gen_dp", string_log="imported")  # Also data_gen_pa

                    # Saving performance attributes
                    df = mat_to_df(n_samples, self.perf_attributes.columns_df, dict_data[pa_long], uid_start)
                    self._write_it(df, n_files, samples_perfile, list(df["uid"]), fileid_start, vec_info="data_gen_pa", string_log="imported")  # Also data_gen_pa

                    vec_uids = list(df["uid"])
                    if dr_long in dict_data.keys():
                        # similar for design representation
                        dict_aux = dict()
                        for key in dict_data[dr_long].keys():
                            if self.design_rep[key].format_file == "npz":
                                # For consistency, also design parameter preceded by uid
                                df = np.concatenate([np.arange(uid_start, uid_start + n_samples).reshape(-1, 1), dict_data[dr_long][key][:n_samples, :]], axis=1)
                                # df = dict_data[dr_long][key][:n_samples,:] # Here we just have an array, but we also attach the ids
                            else:
                                df = mat_to_df(n_samples, self.design_rep[key].columns_df, dict_data[dr_long][key], uid_start)

                            dict_aux[key] = df

                        self._write_it(dict_aux, n_files, samples_perfile, vec_uids, fileid_start, vec_info="data_gen_dr", string_log="imported")

                    self.save_dataset_obj()

                    tot_samples_imported += n_samples
                    if n_samples_toimport is not None:
                        if tot_samples_imported >= n_samples_toimport:
                            logger.warning(f"Not all available data was imported. Only {tot_samples_imported} samples")

                            break

                logger.info("Data import finished. Updating range of performance attributes")

                self.load()
                self.update_obj_domains(flag_only_perfatt=True)
            else:
                logger.info("No callbacks provided to perform the data import")
        else:
            logger.warning("There is a mismatch between sampled and analyzed files. Import cancelled.")

    def _delete_all(self):
        """Deletes all files, in case we want to start from scratch. The folders are kept."""
        files_list = self._name_files([], flag_existing=True)
        for key in files_list.keys():
            for file in files_list[key]:
                os.remove(file)
        files_list = self._name_files_dr([], flag_existing=True)
        for key in files_list.keys():
            for file in files_list[key]:
                os.remove(file)
        self._reset_info_pa_dr()
        self._reset_info_dp()
        if os.path.exists(os.path.join(self.datapath, "logs")):
            shutil.rmtree(os.path.join(self.datapath, "logs"))
        if os.path.exists(os.path.join(self.datapath, "checkpoints")):
            shutil.rmtree(os.path.join(self.datapath, "checkpoints"))

    def _reset_info_pa_dr(self):
        """Resets the info of performance attributes and design representation"""
        files_list = self._name_files_dr([], flag_existing=True)
        for key in files_list.keys():
            self.data_gen_dr[key] = {"uid_vector": [], "fileid_vector": [], "samples_perfile_vector": []}
        self.data_gen_pa = {"uid_vector": [], "fileid_vector": [], "samples_perfile_vector": []}

    def _reset_info_dp(self):
        """Resets the info of design parameters"""
        self.data_gen_dp = {"uid_vector": [], "fileid_vector": [], "samples_perfile_vector": []}

    """
    Methods for performing different analysis and sampling operations
    """

    def sampling(
        self,
        sampler: "SamplesGenerator" = None,
        n_samples: int = 1000,
        samples_perfile: int = 1000,
        callbacks_class: "SamplingCallback" = None,
        flag_sample_distrib: bool = False,
        strategy: str = "uniform",
        engine: str = "sobol",
        flag_bound_to_range: bool = False,
        flag_save: bool = True,
    ) -> Tuple[None, pd.DataFrame]:
        """Only a sampling campaign, to obtain design parameters that will be stored.

        Optionally, we can provide an ad-hoc function to perform the sampling
        on the callbacks, and this is run. It still needs to generate as df as
        output. This callback is run after the sampling, but it can fully override
        the values provided by it.

        Parameters
        ----------
        sampler : _type_, optional, default=None
            An object that performs the sampling.
        n_samples : int, optional, default=1000
            The number of samples to generate.
        samples_perfile : int, optional, default=1000
            The number of samples to include in each file.
        callbacks_class : _type_, optional, default=None
            A callback function for running after sampling.
        flag_sample_distrib : bool, optional, default=False
            To enforce following the distribution of previous samples,
            either coming from an import, or those that have been correctly analysed.
        strategy : str, optional, default='uniform'
            The sampling strategy to use. Other: ``'kde'``, ``'quantile'``
        engine : str, optional, default='sobol'
            The engine to use for sampling. Other: ``'lhc'``, ``'grid'``, ``'random'``, ``'bayesian'``
        flag_bound_to_range : bool, optional, default=False
            If True, the sampling is performed within the range of the design parameters.
        flag_save : bool, optional, default=True
            To save the generated samples or not.

        Returns
        -------
        int
            Returns 0 if ``value_vec`` is required to sample around it and generation is not initiated,
            otherwise returns the number of generated samples.

        """
        # value_vec = None, percentage = 10, c
        # We call one by one the generator, to sample for
        # generator(self, design_par, number, uid_start)

        log = f"""Starting generation of samples with:
            - Strategy {strategy}
            - Engine {engine}"""
        logger.info(log)

        if not len(self.data_gen_dp["uid_vector"]):
            uid_start = 0
            fileid_start = 0
        else:
            uid_start = self.data_gen_dp["uid_vector"][-1] + 1
            fileid_start = self.data_gen_dp["fileid_vector"][-1] + 1

        if flag_sample_distrib:
            strategy = "kde"
        strategy = "uniform" if uid_start == 0 else strategy

        # The user can provide a Sampler already defined, using the SamplesGenerator class
        check_prev = False
        if hasattr(self, "sampler_prev"):
            if self.sampler_prev[1] == strategy and self.sampler_prev[2] == engine:
                check_prev = True

        if sampler is None:
            if check_prev:
                sampler = self.sampler_prev[0]
            else:
                if strategy == "uniform":
                    from aixd.sampler.sampler_definitions import sampler_uniform

                    sampler = sampler_uniform(self.design_par.dobj_list, engine, callbacks_class)

                elif strategy in ["kde", "quantile"]:
                    from aixd.sampler.sampler_definitions import sampler_kde, sampler_quantile

                    self.load()
                    log.info("Sampling following the distribution of previous design parameters values, only those correctly analysed")

                    if strategy == "kde":
                        sampler = sampler_kde(self.design_par.dobj_list, engine, callbacks_class)
                    elif strategy == "quantile":
                        sampler = sampler_quantile(self.design_par.dobj_list, engine, callbacks_class)
                    sampler.fit(self.design_par.data)
                    flag_bound_to_range = True
                self.sampler_prev = [sampler, strategy, engine]

        # First, we sample all at the same time
        # The reason for this is that some sampling schemas, such as sobol
        # or grid, will depend on the other samples
        if samples_perfile > n_samples:
            samples_perfile = n_samples
        n_files = np.ceil(n_samples / samples_perfile).astype(int)
        n_samples = int(samples_perfile * n_files)

        logger.info(f"Starting campaign of sampling for {n_samples} samples in {n_files} files, from uid/fileid {uid_start}/{fileid_start}")

        tic = time.time()

        # Running sampler
        df = sampler.generate(n_samples, output_type="df", flag_bound_to_range=flag_bound_to_range, verbose=False)

        if not flag_save:
            return df

        uid_col = np.arange(uid_start, uid_start + len(df)).astype(int)
        df = pd.concat([pd.DataFrame(uid_col.reshape(-1, 1), columns=["uid"]), df], axis=1)

        self._write_it(df, n_files, samples_perfile, list(uid_col), fileid_start, vec_info="data_gen_dp", string_log="obtained")
        self.save_dataset_obj()

        logger.info(f"Total time required for {n_samples} samples: {time.time() - tic}")

    """
    To compute design representation, we can proceed in 2 ways
    - If the returned element is just a matrix, then it is assumed these are
        the performance attributes
    - But if the return element is a dict, we just save it depending on what we
        find. The keys in this dict should follow the perf. and design_rep convention.
        In any case, if the design_rep is just one element, and the original dictionary has only
        one element, it is assigned automatically
    """

    def analysis(self, analyzer: "AnalysisCallback", n_files: int = None, flag_fromscratch: bool = False, **kwargs):
        """
        We take already sampled samples, and analyze them. Only compute those files
        for which we don't have performance attributes. This means that we can run new
        sampling campaigns later, and then come back and perform the analysis.

        Parameters
        ----------
        analyzer : AnalysisCallback
            The callback function created with the analysis function. It feeds the design parameters
            to the analysis function, obtains the performance attributes, and ensures they are returned
            in the correct format.
        n_files : int, optional, default=None
            Out of all the files with design parameters which have not been analyzed, how many we
            want to analyze. In case the process is quite computationally expensive, and we prefer
            to proceed in batches. If None, it analyzes all the files.
        flag_fromscratch : bool, optional, default=False
            To remove all existing performance attributes files, and perform the analysis again
            on all sets of design parameters. This is useful if the analysis function has changed.
        """
        if flag_fromscratch:
            # This flags exists in case the analysis functions changes
            id_files_analyze = self.data_gen_dp["fileid_vector"]
            # ATTENTION, the files are not deleted
            self._reset_info_pa_dr()

            logger.warning("Index info reseted to start from scratch! But the old files remain!")

        else:
            # TODO: the ids to analyze depend on either computing pa or design_rep
            # Hence, we should update this, as if the callback is just for design_rep, this is wrong
            id_files_analyze = np.setdiff1d(self.data_gen_dp["fileid_vector"], self.data_gen_pa["fileid_vector"])
            if (n_files is not None) and (n_files > 0):
                id_files_analyze = id_files_analyze[:n_files]

        # TODO implement parallel means
        filename = self._name_files(id_files_analyze)
        if len(self.design_rep.keys()):
            filename_dr = self._name_files_dr(id_files_analyze)
        tic = time.time()
        tot_samples = 0

        logger.info("Starting evaluation of design parameters to obtain performance attributes")

        for file_dp, file_pa, ind in zip(filename[dp_long], filename[pa_long], range(len(filename[pa_long]))):
            if os.path.exists(file_dp):
                # df_dp = pd.read_pickle(file_dp)
                df_dp = self.design_par.read(file_dp)
                # Running the analysis on the opened design parameters
                dict_pa_dr = analyzer.run(df_dp, **kwargs)
                # If the analysis fails, we still need to return a matrix of the same size for both
                # design_rep and perf_att, but with a 1 on error, and any value on the rows
                fileid = ud.fileid_int(file_dp, constants.design_par_file)[0]
                extra_samples = 0
                vec_uids = list(df_dp["uid"])
                if isinstance(dict_pa_dr, dict):
                    if pa_long in dict_pa_dr.keys():
                        self._write_performance_att(dict_pa_dr[pa_long], file_pa, vec_uids, fileid)
                        extra_samples = len(dict_pa_dr[pa_long])
                    if dr_long in dict_pa_dr.keys():
                        self._write_design_rep(dict_pa_dr[dr_long], filename_dr, vec_uids, fileid, int(ind))
                        extra_samples = len(dict_pa_dr[pa_long])
                else:
                    self._write_performance_att(dict_pa_dr, file_pa, vec_uids, fileid)
                    extra_samples = len(dict_pa_dr)
                tot_samples += int(extra_samples)
            else:
                logger.info(f"File {file_dp.split('/')[-1]} does not exist! Regenerate indexes!")

        logger.info("Updating ranges for performance attributes")

        self.load()
        logger.info("Updating ranges for performance attributes")
        self.update_obj_domains(flag_only_perfatt=True)

        logger.info(f"Total time requires for analyzing {tot_samples} samples: {time.time() - tic}")

    def write_data_dp_pa(self, data_combined, samples_perfile=None):
        # TODO deprecated??
        all_objs = self.design_par.dobj_list + self.perf_attributes.dobj_list
        data_combined = convert_to(data_combined, "df", all_objs)
        cols_dp = self.design_par.columns_df
        cols_dp.remove("uid")
        cols_pa = self.perf_attributes.columns_df
        cols_pa.remove("uid")
        cols_pa.remove("error")
        n_samples = len(data_combined)

        # By default, we just store all the samples in one file
        if samples_perfile is None:
            samples_perfile = n_samples

        if set(cols_dp).issubset(data_combined.columns) and set(cols_pa).issubset(data_combined.columns):
            if not len(self.data_gen_dp["uid_vector"]):
                uid_start = 0
                fileid_start = 0
            else:
                uid_start = self.data_gen_dp["uid_vector"][-1] + 1
                fileid_start = self.data_gen_dp["fileid_vector"][-1] + 1

            n_files = np.ceil(n_samples / samples_perfile).astype(int)
            uid_col = np.arange(uid_start, uid_start + n_samples).astype(int)

            df_dp = data_combined[cols_dp]
            df_pa = data_combined[cols_pa]
            error_vec = pd.DataFrame(np.zeros(n_samples).reshape(-1, 1), columns=["error"])
            df_uid = pd.DataFrame(uid_col, columns=["uid"])
            if "error" in data_combined.columns:
                error_vec = data_combined["error"]
            df_dp = pd.concat([df_uid, df_dp], axis=1)
            df_pa = pd.concat([df_uid, df_pa, error_vec], axis=1)

            self._write_it(df_dp, n_files, samples_perfile, list(uid_col), fileid_start, vec_info="data_gen_dp", string_log="obtained")
            self._write_it(df_pa, n_files, samples_perfile, list(uid_col), fileid_start, vec_info="data_gen_pa", string_log="obtained")  # Also data_gen_pa
            self.save_dataset_obj()

        else:
            raise ValueError("The data provided does not contain all the required information")

    def get_samples(
        self,
        sampler: "SamplesGenerator" = None,
        analyzer: "AnalysisCallback" = None,
        n_samples: int = 1,
        format_in: str = "df",
        format_out: str = "df",
        callbacks_class: "SamplingCallback" = None,
        flag_sample_distrib: bool = False,
        strategy: str = "uniform",
        engine: str = "sobol",
        flag_bound_to_range: bool = False,
    ):
        """
        Method to obtain some samples and return them in the desired format, but without saving them
        into files. Besides, if an `AnalysisCallback` is provided, the samples are analyzed and a
        combined output is returned, with design parameters and performance attributes.

        Parameters
        ----------
        sampler : SamplesGenerator, optional, default=None
            An object that performs the sampling. If None, the `sampler` is created following the strategy and engine.
        analyzer : AnalysisCallback, optional, default=None
            The callback function created with the analysis function. It feeds the design parameters
            to the analysis function, obtains the performance attributes, and ensures they are returned
            in the correct format. If None, only design parameters are returned.
        n_samples : int, optional, default=1
            The number of samples to generate.
        format_in : str, optional, default="df"
            The format required by the analyzer function for the input data to use.
            Other options are: ``'dict'``, ``'dict_list'``, ``'array'``, ``'torch'``, ``'list'``,
            ``'df_per_obj'``, ``'df'``
        format_out : str, optional, default="df"
            The format in which we want the output to be returned.
            Other options are: ``'dict'``, ``'dict_list'``, ``'array'``, ``'torch'``, ``'list'``,
            ``'df_per_obj'``, ``'df'``
        callbacks_class : SamplingCallback, optional, default=None
            A callback function for running after sampling.
        flag_sample_distrib : bool, optional, default=False
            To enforce following the distribution of previous samples,
            either coming from an import, or those that have been correctly analysed.
        strategy : str, optional, default="uniform"
            The sampling strategy to use. Other: ``'kde'``, ``'quantile'``
        engine : str, optional, default="sobol"
            The engine to use for sampling. Other: ``'lhc'``, ``'grid'``, ``'random'``, ``'bayesian'``
        flag_bound_to_range : bool, optional, default=False
            If True, the sampling is performed within the range of the design parameters.
        """
        dp_samples = self.sampling(
            sampler,
            n_samples,
            samples_perfile=1,
            callbacks_class=callbacks_class,
            flag_sample_distrib=flag_sample_distrib,
            strategy=strategy,
            engine=engine,
            flag_bound_to_range=flag_bound_to_range,
            flag_save=False,
        )

        dp_samples = convert_to(dp_samples, format_out, self.design_par.dobj_list)

        if analyzer is not None:
            pa_samples = analyzer.analyze(input=dp_samples, format_in=format_in, format_out=format_out)
            return combine_formats([dp_samples, pa_samples], format_out)
        else:
            return dp_samples

    def _write_design_par(self, mat, filename, vec_uids, fileid, string_log="obtained"):
        """Auxiliary function to write design parameters in the files"""
        df_pa = pd.DataFrame(mat, columns=self.design_par.columns_df)
        df_pa["uid"] = df_pa["uid"].astype(int)
        self._write_single(df_pa, filename, vec_uids, fileid, save_set="design_par", vec_info="data_gen_dp", string_log=string_log)

    def _write_performance_att(self, mat, filename, vec_uids, fileid, string_log="obtained"):
        """Auxiliary function to write performance attributes in the files"""
        if mat.shape[1] < len(self.perf_attributes.columns_df):
            mat = np.concatenate([np.asarray(vec_uids).reshape(-1, 1), mat], axis=1)
        df_pa = pd.DataFrame(mat, columns=self.perf_attributes.columns_df)
        df_pa["uid"] = df_pa["uid"].astype(int)
        df_pa["error"] = df_pa["error"].astype(int)
        self._write_single(df_pa, filename, vec_uids, fileid, save_set="perf_attributes", vec_info="data_gen_pa", string_log=string_log)

    def _write_design_rep(self, dict_mat, filename, vec_uids, fileid, ind, string_log="obtained"):
        """Auxiliary function to write design representations in the files"""
        if isinstance(dict_mat, dict):
            for key in dict_mat.keys():
                file_dr = filename[key][ind]
                self._write_single(dict_mat[key], file_dr, vec_uids, fileid, save_set="design_rep", vec_info='data_gen_dr["{}"]'.format(key), string_log=string_log)
        elif len(self.design_rep.keys()) == 1:
            key = list(self.design_rep.keys())[0]
            file_dr = filename[key][ind]
            self._write_single(dict_mat[key], filename, vec_uids, fileid, save_set="design_rep", vec_info='data_gen_dr["{}"]'.format(key), string_log=string_log)
        else:
            logger.error("Problem finding the correspondence for design representation")

    def _write_it(self, df, n_files, samples_perfile, vec_uids, fileid_start, vec_info="data_gen_dp", string_log="obtained"):
        """Auxiliary function that calls the individual write functions"""
        # Second, we store
        for nf in range(n_files):
            vec_uids_aux = vec_uids[(nf * samples_perfile) : ((nf + 1) * samples_perfile)]
            fileid = fileid_start + nf
            if vec_info == "data_gen_pa":
                str_el = pa_long
                filename = self._name_files([fileid])[str_el][0]
                df_aux = df.iloc[(nf * samples_perfile) : ((nf + 1) * samples_perfile)]
                self._write_performance_att(df_aux, filename, vec_uids_aux, fileid, string_log)
            elif vec_info == "data_gen_dp":
                str_el = dp_long
                filename = self._name_files([fileid])[str_el][0]
                df_aux = df.iloc[(nf * samples_perfile) : ((nf + 1) * samples_perfile)]
                self._write_design_par(df_aux, filename, vec_uids_aux, fileid, string_log)
            elif vec_info == "data_gen_dr":
                str_el = dr_long
                filename = self._name_files_dr([fileid])
                dict_aux = dict()
                for key in df.keys():
                    if self.design_rep[key].format_file == "npz":
                        dict_aux[key] = df[key][(nf * samples_perfile) : ((nf + 1) * samples_perfile), :]
                    else:
                        dict_aux[key] = df[key].iloc[(nf * samples_perfile) : ((nf + 1) * samples_perfile)]
                self._write_design_rep(dict_aux, filename, vec_uids_aux, fileid, 0, string_log)

    def _write_single(self, df, filename, vec_uids, fileid, save_set="perf_attributes", vec_info="data_gen_pa", string_log="obtained"):
        """Auxiliary function to write a single file, for any of the three types of data"""
        if save_set == "perf_attributes":
            set_str = ["performance attributes", "perf_attributes"]
        elif save_set == "design_rep":
            set_str = ["design representation", "design_rep" + vec_info.replace("data_gen_dr", "")]
        elif save_set == "design_par":
            set_str = ["design parameters", "design_par"]

        try:
            eval("self.{}.write(df, filename)".format(set_str[1]))

            logger.info(f"{len(df)} {set_str[0]} {string_log} and stored in {'/'.join(filename.split('/')[-2:])}")

            eval('self.{}["uid_vector"].extend(list(vec_uids))'.format(vec_info))
            eval('self.{}["fileid_vector"].append(int(fileid))'.format(vec_info))
            eval('self.{}["samples_perfile_vector"].append(len(vec_uids))'.format(vec_info))
            if save_set == "perf_attributes":
                if np.sum(list(df["error"])):
                    logger.warning(f"Error computing the performance attributes for {np.sum(list(df['error']))} samples from {'/'.join(filename.split('/')[-2:])}")

        except Exception:
            logger.error(f"Problem saving {set_str[0]} from {'/'.join(filename.split('/')[-2:])}")
