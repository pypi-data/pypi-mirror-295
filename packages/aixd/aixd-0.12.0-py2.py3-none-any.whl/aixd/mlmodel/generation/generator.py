"""
Function for the definition of the generator class
It intervenes in the last part of the process. Receives the following elements:
- Datamodule instance
- Model instance

Besides, it also uses an instance of the sampler class.

It uses then all these elements, and the sampler for generation, to perform
the following actions:
- Provide some feasible vector to the decoder, given a request
- Generate samples for a large range of values, to be used by the plotter

"""

import itertools
import warnings
from typing import Dict, List, Tuple, Union

import numpy as np
import pandas as pd
import torch

from aixd.data import DataBlock, DataObject, TransformableDataBlock
from aixd.data.custom_callbacks import AnalysisCallback, CustomCallback
from aixd.data.utils_data import combine_formats, convert_to
from aixd.mlmodel.architecture.cond_ae_model import CondAEModel
from aixd.mlmodel.data.data_loader import DataModule
from aixd.mlmodel.generation.sampling import GeneratorSampler
from aixd.mlmodel.utils_mlmodel import ids_attrib
from aixd.utils import logs

logger = logs.get_logger().get_child("mlmodel-generator")


class Generator:
    """
    Initialize a Generator instance. This instance is used to request the trained model
    the generation of sets of design parameters for a given set of attributes.

    Parameters
    ----------
    model : CondAEModel, optional, default=None
        The LightningModule that defines the generation process. If not provided,
        generation will be performed without a specific model.
    datamodule : DataModule optional, default=None
        The LightningDataModule that handles data loading and preprocessing.
        If not provided, data handling should be managed externally.
    sampling_type : str, optional, default="sampling"
        The type of sampling to be used for generation. The options are: "bayesian",
        and "sampling". See notes for more details.
    over_sample: int, optional, default=10
        If we request to generate n_samples, we will generate n_samples * over_sample,
        and then select the best n_samples.
    callbacks_class : class, optional, default=None
        A custom callback class to be used during the data generation process.
        This class should be derived from LightningCallbacks.
    fast_generation : bool, optional, default=False
        If True, the generation process will be faster, but the values of z will not be
        generated conditioned on the y requested. Only applicable to the Conditional AE model.

    Notes
    -----
    - All the instances of `datamodule` and `model` (with the checkpoint) loaded
        are required
    - The default `sampling_type` type is "sampling", and also the most recommended. "bayesian" is too
        slow.
    - If you want to use custom callbacks, provide a user-defined class via the
    `callbacks_class` parameter.
    """

    def __init__(
        self,
        model: CondAEModel,
        datamodule: DataModule,
        sampling_type: str = "sampling",
        over_sample: int = 10,
        callbacks_class: CustomCallback = None,
        fast_generation: bool = True,
    ) -> None:
        # Check if the model is on GPU, and if so, move it to CPU
        if not next(model.parameters()).is_cpu:
            model = model.to("cpu")
            warnings.warn("The generator currently only support models on CPU. The model has been moved to CPU.")

        self.model = model
        self.datamodule = datamodule
        self.fast_generation = fast_generation if isinstance(model, CondAEModel) else True

        if isinstance(datamodule, DataModule):
            self.attributes_valid = self.datamodule.output_ml_dblock.columns_df  # _transf
            self.info_attributes_req()
        else:
            logger.warning("A valid data module should be provided")

        self.sampler = GeneratorSampler(sampling_type, datamodule)
        self.callbacks_class = callbacks_class
        self.over_sample = over_sample  # How many more samples are obtaining, to later choose the indicated number

    def info_attributes_req(self) -> None:
        """
        It just prints the attributes that could be requested for generation
        """
        print("* Possible individual attributes to request for the design are:")
        print('     "{}"'.format('", "'.join(self.attributes_valid)))
        print("\n* You can also request for full data objects, with the following format: [None, 2, None]:")
        print("  For 'A' with dim = 3, y_req = [None, 2, None], which would be similar to requesting for 'A_1' = 2")
        print('     "{}"'.format('", "'.join(self.datamodule.output_ml_dblock.names_list)))
        val_gen = "Fast" if self.fast_generation else "Slow"
        print("\n* The generation process is set to: {}".format(val_gen))
        if self.fast_generation:
            print(
                """
    In this case, the values of z will not be generated conditioned on the y requested.
    This vastly accelerates the generation process, and is compensated by the over_sample
    parameter, which will allow generating more designs to then choose the best.
                """
            )
        else:
            print(
                """
    In this case, the values of z are generated conditioned on the y requested. This is quite
    costly, but allows generating samples that will lead to more precise generations, reducing the
    need for over sampling and the selection of the best designs.
                """
            )

    def generate(
        self,
        request: Dict[str, Union[int, float, bool, str, List]] = None,
        y_req: List[Union[int, float, bool, str, List]] = None,
        attributes: List[str] = None,
        weights: Dict[str, Union[int, float, bool, str, List]] = None,
        format_out: str = "df",
        n_samples: int = 50,
        print_results: bool = True,
        analyzer: "AnalysisCallback" = None,
        **kwargs,
    ) -> Tuple[Union[Dict, List, pd.DataFrame], Dict[str, Dict]]:
        """
        Wrapper method to call the generation process. It takes care of adapting the request,
        running the generator, and then providing the output in the specified format. Some of the options
        are simplified, as this is the function exposed to the user. For example, we assume the values are
        requested in the original domain, and that we are performing a single request.
        To run more specific generation process, it is better to use .run method.

        Parameters
        ----------
        self : object
            The instance of the class containing this method.
        request : Dict[str, Union[int, float, bool, str, List]], optional, default=None
            A dictionary with the attributes and values requested for generation. If provided,
            the `y_req` and `attributes` parameters are ignored.
        y_req : List[int, float, bool, str, List[int, float, bool, str]], optional, default=None
            The values requested for each of the attributes specified. Depending on the type of attribute,
            we can have to provide an specific type. Besides, if we want to generate in an interval, we can
            alternatively provide a List.
        attributes : List[str], optional, default=None
            The list of attribute names used to run the generative process.
        weights : Dict[str, Union[int, float, bool, str, List]], optional, default=None
            To assign different weighting to each attribute, when selecting the best instances
        format_out : str, optional, default=None
            The format of the output. The options are: "dict", "dict_list", "array", "torch", "list",
            "df_per_obj", "df". If not provided, the output will be a dictionary with
            all the information gathered from the generation process.
        n_samples : int, optional, default=50
            The number of samples of design parameters to generate.
        print_results : bool, optional, default=True
            Print an overview of the samples generated, and the errors computed.
        analyzer : AnalysisCallback, optional, default=None
            If provided, the generator will use the analyzer to compute the ground truth values. This is
            only possible when the InputML and OutputML are aligned with the DesignParameters and the
            PerformanceAttributes. If not, these values won't be computed.

        Returns
        -------
        Tuple[Union[Dict, List, pd.DataFrame]
            The dataframe with the combined inputML and outputML data, in the format specified by `format_out`.
        Dict[str, Dict]]
            This dictionary contains all the information gathered from the generation process. Hence, it can
            be used in other methods, from plotting, to computing errors, etc.
        """
        # Adapting the request to refer to specific columns
        y_req, attributes = self._adapt_request(request, y_req, attributes)

        weights = {o: 1 for o in attributes} if weights is None else weights
        self.weights = [weights[o] if o in weights.keys() else 1 for o in attributes]

        # Calling the generation
        dict_res = self._run(y_req, attributes, n_samples, request_orig_range=True, flag_peratt=False, nbins=1, **kwargs)

        if analyzer is not None and self._check_analyzer_sets(analyzer):
            y_gt = analyzer.analyze(input=dict_res["all"]["untransformed"]["x_gen"], format_out="df")
            dict_res = self._update_with_gt(dict_res, y_gt, n_samples)

        # Printing the results
        if print_results:
            self.print_results_gen(dict_res)

        # Converting the output to the desired format
        if format_out is None:
            return dict_res
        else:
            in_ml = dict_res["all"]["untransformed"]["x_gen_best"]
            out_ml = dict_res["all"]["untransformed"]["y_pred_all_best"]  # if analyzer is None else dict_res["all"]["untransformed"]["y_gt_best_all"]
            in_ml = convert_to(in_ml, format_out, self.datamodule.input_ml_dblock.dobj_list)
            out_ml = convert_to(out_ml, format_out, self.datamodule.output_ml_dblock.dobj_list)
            return combine_formats([in_ml, out_ml], format_out), dict_res

    def _check_analyzer_sets(self, analyzer: "AnalysisCallback") -> bool:
        all_val = True
        if not set(self.datamodule.output_ml_dblock.names_list).issubset(analyzer.perf_attributes.names_list):
            all_val = False
            subset = np.setdiff1d(self.datamodule.output_ml_dblock.names_list, analyzer.perf_attributes.names_list)
            print("Some outputML attributes are missing from the performance attributes: {}".format(", ".join(subset)))

        if not set(analyzer.design_par.names_list).issubset(self.datamodule.input_ml_dblock.names_list):
            all_val = False
            subset = np.setdiff1d(analyzer.design_par.names_list, self.datamodule.perf_attributes.names_list)
            print("Not all design parameters missing from inputML: {}".format(", ".join(subset)))

        return all_val

    def _update_with_gt(self, dict_res: Dict[str, Dict], y_gt_untransf: np.ndarray, n_samples: int, key_in: str = "all") -> Dict[str, Dict]:
        """Given the gt values computed using the CAD/FEM, the dict is updated with the new error values"""

        def to_df(x, cols):
            return pd.DataFrame(x, columns=cols)

        def to_np(x):
            return np.asarray(x)

        def unord(vec, ind_sort):
            vec_aux = np.zeros(vec.shape).astype(vec.dtype)
            vec_aux[ind_sort] = vec
            return vec_aux

        ind_sort_all, ind_sort_best, ind_attribute = dict_res[key_in]["ind_sort"], dict_res[key_in]["ind_sort_best"], dict_res[key_in]["ids_att"]

        # First, we need to undo the ordering
        y_gt_untransf_unord_o = unord(to_np(y_gt_untransf), ind_sort_all)[:, :-1]  # To remove the error column
        y_gt_transf_unord_o = self.datamodule.transform_y(y_gt_untransf_unord_o)

        y_samp_transf_unord = unord(to_np(dict_res[key_in]["transformed"]["y_samp_all"]), ind_sort_all)
        y_samp_untransf_unord = unord(to_np(dict_res[key_in]["untransformed"]["y_samp_all"]), ind_sort_all)

        y_pred_transf_unord = unord(to_np(dict_res[key_in]["transformed"]["y_pred_all"]), ind_sort_all)
        y_pred_untransf_unord = unord(to_np(dict_res[key_in]["untransformed"]["y_pred_all"]), ind_sort_all)

        y_gt_transf_unord, y_pred_transf_unord, y_samp_transf_unord = (
            self.model.split_y_head_in(y_gt_transf_unord_o),
            self.model.split_y_head_in(y_pred_transf_unord),
            self.model.split_y_head_in(y_samp_transf_unord),
        )

        y_gt_untransf_unord, y_pred_untransf_unord, y_samp_untransf_unord = (
            self.model.split_y_head_in(y_gt_untransf_unord_o),
            self.model.split_y_head_in(y_pred_untransf_unord),
            self.model.split_y_head_in(y_samp_untransf_unord),
        )

        ind_attribute = dict_res[key_in]["ids_att"]

        # Errors: between requested and ground truth, and between predicted and ground truth
        y_losses_gt_untransf = self.model.y_losses_calculation(y_gt_transf_unord, y_samp_transf_unord, y_gt_untransf_unord, y_samp_untransf_unord, untransform=True)
        y_losses_gt_pred_untransf = self.model.y_losses_calculation(y_gt_transf_unord, y_pred_transf_unord, y_gt_untransf_unord, y_pred_untransf_unord, untransform=True)

        y_losses_gt_transf = self.model.y_losses_calculation(y_gt_transf_unord, y_samp_transf_unord, y_gt_untransf_unord, y_samp_untransf_unord, untransform=False)
        y_losses_gt_pred_transf = self.model.y_losses_calculation(y_gt_transf_unord, y_pred_transf_unord, y_gt_untransf_unord, y_pred_untransf_unord, untransform=False)

        y_cols = y_losses_gt_untransf.columns

        error_gt = np.asarray(y_losses_gt_transf)[:, ind_attribute].reshape(len(y_losses_gt_transf), -1).mean(axis=-1)[ind_sort_all]
        error_gt_best = error_gt[ind_sort_best]

        # Storing errors
        dict_res[key_in]["transformed"]["error_gt"] = error_gt
        dict_res[key_in]["transformed"]["error_gt_best"] = error_gt_best

        # Storing individual errors per attributes and output of model - untransformedd, i.e. original range
        dict_vec = {"y_gt": to_df(y_gt_untransf_unord_o, y_cols), "y_diff_gt": y_losses_gt_untransf, "y_diff_gt_pred": y_losses_gt_pred_untransf}
        dict_res = self._create_dict_res(dict_res, dict_vec, dict_res[key_in]["attributes"], ind_sort_all, ind_sort_best, key_in, "untransformed")

        # Storing individual errors per attributes and output of model - Normalized
        dict_vec = {"y_gt": to_df(y_gt_transf_unord_o, y_cols), "y_diff_gt": y_losses_gt_transf, "y_diff_gt_pred": y_losses_gt_pred_transf}
        dict_res = self._create_dict_res(dict_res, dict_vec, dict_res[key_in]["attributes"], ind_sort_all, ind_sort_best, key_in, "transformed")

        return self._dict_all_tocdn(dict_res)

    def _run(
        self,
        y_req: List[Union[int, float, bool, str, List]],
        attributes: List[str],
        n_samples: int,
        request_orig_range: bool = True,
        flag_peratt: bool = False,
        nbins: int = 1,
        analyzer: "AnalysisCallback" = None,
        **kwargs,
    ) -> Dict[str, Dict]:
        """
        Method to generate sets of design parameters given a set of attributes from `outputML`,
        and the values for the generation.

        Parameters
        ----------
        self : object
            The instance of the class containing this method.
        request : Dict[str, Union[int, float, bool, str, List]], optional, default=50
            A dictionary with the attributes and values requested for generation. If provided,
            the `y_req` and `attributes` parameters are ignored.
        y_req : List[int, float, bool, str, List[int, float, bool, str]], optional, default=50
            The values requested for each of the attributes specified. Depending on the type of attribute,
            we can have to provide an specific type. Besides, if we want to generate in an interval, we can
            alternatively provide a List.
        attributes : List[str], optional, default=50
            The list of attribute names used to run the generative process.
        n_samples : int, optional, optional, default=50
            The number of samples of design parameters to generate.
        request_orig_range : bool, optional, optional, default=False
            If True, the `y_req` is specified within the original range of the real data.
        flag_peratt : bool, optional, optional, default=False
            If True, make independent generation requests for each attribute provided.
        nbins : int, optional, optional, default=1
            Using `nbins` is mostly intended for plotting purposes. It allows to generate
            many different requests in a binarize interval, and compute the error. Hence, it works
            differently as a request with a provided interval
        analyzer : AnalysisCallback, optional, default=None
            If provided, the generator will use the analyzer to compute the ground truth values. This is
            only possible when the InputML and OutputML are aligned with the DesignParameters and the
            PerformanceAttributes. If not, these values won't be computed.
        **kwargs : dict
            Additional keyword arguments specific to the generation method.

        Returns
        -------
        dict_out : Dict[str, Dict]
            This dictionary contains all the information gathered from the generation process. Hence,
            it can be used for many purposes, from plotting, to computing errors, or to extract
            the set of best generated samples

        Notes
        -----
        - The 'y_req' list should have the same length as the 'attributes' list.
        - If 'flag_peratt' is True, 'n_samples' will be divided equally among attributes.
        - When nbins = 1, the error for the attribute assigned to an interval is 0 if the value is within the interval
            When nbins > 1, which is intended for plotting purposes, the error is not 0, but the difference to requested
            value, which is sampled in that interval

        Example:
        --------
        >>> data_gen = Generator(datamodule, model, over_sample=1) # doctest: +SKIP
        >>> y_req = [3, 4.5, 'bananas'] # doctest: +SKIP
        >>> attributes = ['Age', 'Income', 'Fruit'] # doctest: +SKIP
        >>> samples_gen_dict = data_gen.generation(y_req, attributes, n_samples=100, request_orig_range=True) # doctest: +SKIP
        """

        # TODO account for the case we request for a full dobj, proving a list and Nones
        dummy_dblock = TransformableDataBlock(name="dummy", dobj_list=self.datamodule.output_ml_dblock.dobj_list, flag_split_perdim=True)

        # Checking if the all attributes are valid
        y_req, attributes_req, dobj_req, flag_range = self._get_corr_attributes(dummy_dblock, y_req, attributes)
        self.weights = [1 for o in attributes_req]
        nbins = 1 if not flag_range else nbins

        if len(attributes_req):
            # Calling generation
            dict_out = self._call_gen(dummy_dblock, y_req, attributes_req, n_samples, request_orig_range, flag_peratt, flag_range, nbins, dobj_req, max_samples_per=5000, **kwargs)
            # Calling selection of best
            dict_out = self._choose_best(dict_out, n_samples, nbins, dummy_dblock.dobj_list_transf, flag_range=flag_range)
            dict_out = self._dict_all_tocdn(dict_out)

            if analyzer is not None and self._check_analyzer_sets(analyzer):
                for key in dict_out.keys():
                    y_gt = analyzer.analyze(input=dict_out[key]["untransform"]["x_gen"], format_out="array")
                    dict_out = self._update_with_gt(dict_out, y_gt, n_samples, key_in=key)

            return dict_out

        else:
            # print("None of the attributes specified were found in the dataset")
            logger.warning("None of the attributes specified were found in the dataset")
            return None

    def _adapt_request(self, request: Dict[str, Union[int, float, bool, str, List]] = None, y_req: List[Union[int, float, bool, str, List]] = None, attributes: List[str] = None):
        """
        It takes care of collecting the request, and adapting it to the format required by the generation
        method. Possible input types are:

        Having A dimension 2 and B dimension 3
        req = {'A_1': 1, 'B_0': 2}
        attributes = ['A_1', 'B_0'], y_req = [1,2]

        Or referring to the Data Objects
        req = {'A': [None, 1], 'B': [2, None, None]}
        attributes = ['A', 'B'], y_req = [[None, 1],[2, None, None]]

        We can also mix names of columns and dobjects
        req = {'A': [None, 1], 'B_0': [2]}

        Besides, we have the extra level of complexity, when we are requesting ranges, or mix of
        ranges and single values
        req = {'A_1': [1,3], 'B_0': 2}
        attributes = ['A_1', 'B_0'], y_req = [[1,3],2]

        req = {'A': [None, [1,3]], 'B': [2, None, None]}
        attributes = ['A', 'B'], y_req = [[None, [1,3]],[2, None, None]]

        All these different types of inputs need to be converted to the following format:

        attributes = ['A_1', 'B_0'], y_req = [1,2]

        because the main method, .run, is using one dataobject per column, as required by the sampler
        """

        # Obtaining the requested values
        if request is not None:
            attributes = list(request.keys())
            y_req = [request[k] for k in attributes]
        elif y_req is None or attributes is None:
            raise ValueError("You have to provide a request or the values and attributes requested")

        assert len(y_req) == len(attributes), "The number of attributes and values requested do not match"

        # Now, we just form the new attributes and y_req, only with information
        outputML = self.datamodule.output_ml_dblock
        y_req_def = []
        attributes_def = []
        for ind, att in enumerate(attributes):
            if att in self.attributes_valid:
                attributes_def.append(att)
                y_req_def.append(y_req[ind])
            elif att in outputML.names_list:
                dobjs = outputML.get_dobjs([att])
                req_aux = y_req[ind]
                for indr, req in enumerate(req_aux):
                    if req is not None:
                        attributes_def.append(dobjs[0].columns_df[indr])
                        y_req_def.append(req)
            else:
                logger.warning(f"Attribute/Data Object {att} not found in the dataset")
        return y_req_def, attributes_def

    def print_results_gen(self, dict_out: Dict[str, Dict]) -> None:
        """
        Print the results stored in a dictionary of dictionaries.

        This method takes a dictionary of dictionaries as input, where the outer dictionary
        represents categories or groups, and the inner dictionaries contain results or data
        associated with each category. It prints the results in a readable format.

        Parameters:
        ----------
        self : object
            The instance of the class containing this method.

        dict_out : Dict[str, Dict])
            The dictionary generated by the `generation` method, which contains a lof of nested
            dictionaries with the results of the generation process.
        """

        print("###########")
        print("Error during generation")
        print("###########\n")
        for key in dict_out.keys():
            str_req = [str(o) + " = " + str(i) for o, i in zip(dict_out[key]["attributes"], dict_out[key]["untransformed"]["y_req"])]
            print("* Errors when requesting: {}".format(", ".join(str_req)))
            n_samples = len(dict_out[key]["untransformed"]["y_diff_pred_best"])
            mean_err = np.mean(dict_out[key]["untransformed"]["y_diff_pred_best"], axis=0)
            print("Mean for {} samples: {}".format(n_samples, ", ".join([str(o) for o in mean_err])))
            mean_err = np.mean(dict_out[key]["untransformed"]["y_diff_pred_best"][: int(np.ceil(n_samples / 10))], axis=0)
            print("Mean for {} sample(s): {}\n".format(np.ceil(n_samples / 10), ", ".join([str(o) for o in mean_err])))
            print("Best sample: {}\n".format(", ".join([str(o) for o in np.asarray(dict_out[key]["untransformed"]["y_pred_best"])[0]])))

    def _get_corr_attributes(self, datablock: DataBlock, y: List[Union[int, float, bool, str, List]], attributes: List[str]) -> Tuple[List, List, List[DataObject], bool]:
        """
        Print the results stored in a dictionary of dictionaries.

        This method takes a dictionary of dictionaries as input, where the outer dictionary
        represents categories or groups, and the inner dictionaries contain results or data
        associated with each category. It prints the results in a readable format.

        Parameters:
        ----------
        self : object
            The instance of the class containing this method.
        y : List[Union[int, float, bool, str, List]]
            The list of requested values, also including list that can specify intervals
        attributes : List[str]
            The list of attributes requested

        Returns:
        ----------
        y_req : List
            List of requested value, only including the valid ones, according to the attributes checked
        attributes_req : List
            Only the names correctly specified are returned
        dobj_req : List[DataObject]
            DataObject instances for the attributes requested, to be used in later steps
        flag_range : bool
            Indicates if the list of requests include intervals or not
        """

        flag_range = False
        attributes_req = []
        dobj_req = []
        y_req = []

        for ind, att in enumerate(attributes):
            name_att = att.strip().replace(" ", "_")
            if name_att in self.attributes_valid:
                # TODO: maisseal, this can be solved better, in the end we want to retrieve a data object by name
                # TODO: maisseal, Do we need the transformed objects here?
                dobj = datablock.dobj_list[self.attributes_valid.index(name_att)]
                attributes_req.append(att.strip().replace(" ", "_"))
                dobj_req.append(dobj)
                val_req = y[ind]
                if not isinstance(val_req, list):
                    val_req = [val_req]
                if dobj.domain.domain_type == "Interval":
                    y_req.append(val_req[:2])
                else:
                    y_req.append(val_req)

                if len(val_req) > 1:
                    # Also applies for the case we request more than 1 possible option
                    flag_range = True
            else:
                logger.warning(f"Attribute {att} not found in the dataset")
        return y_req, attributes_req, dobj_req, flag_range

    def _call_gen(
        self,
        datablock: DataBlock,
        y_req: List[Union[int, float, bool, str, List]],
        attributes: List[str],
        n_samples: int = 50,
        request_orig_range: bool = False,
        flag_peratt: bool = False,
        flag_range: bool = False,
        nbins: int = 1,
        dobj_req: List[DataObject] = None,
        max_samples_per: int = 5000,
        **kwargs,
    ):
        """
        Call the function that generates the sets of design parameters, either per attributes
        or for all attributes simultaneously

        Parameters:
        -----------
        self : object
            The instance of the class containing this method.
        y_req : List[int, float, bool, str, List[int, float, bool, str]]
            The values requested for each of the attributes specified. Depending on the type of attribute,
            we can have to provide an specific type. Besides, if we want to generate in an interval, we can
            alternatively provide a List.
        attributes : List[str]
            The list of attribute names used to run the generative process.
        n_samples : int, optional, default=50
            The number of samples of design parameters to generate.
        request_orig_range : bool, optional, default=False
            If True, the `y_req` is specified within the original range of the data.
        flag_peratt : bool, optional, default=False
            If True, make independent generation requests for each attribute provided.
        flag_range : bool, optional, default=False
            If True, indicates if the list of requests include intervals or not
        nbins : int, optional, default=1
            Using `nbins` is mostly intended for plotting purposes. It allows to generate
            many different requests in a binarize interval, and compute the error. Hence, it works
            differently as a request with a provided interval
        dobj_req : List[DataObject], optional, default=None
            A list of DataObject instances used by the sampler
        max_samples_per : int, optional, default=5000
            To avoid passing batches too large through the decoder, we can limit the number of samples,
            and compute the decode step as this maximum is beign achieved

        **kwargs
            Additional keyword arguments for customization.

        Returns:
        --------
        dict_out : Dict[str, Dict]
            This dictionary contains all the information gathered from the generation process. Hence,
            it can be used for many purposes, from plotting, to computing errors, or to extract
            the set of best generated samples
        """

        max_samples_per = 5000  # To decode in batches, to avoid killing the GPU/CPU

        if not isinstance(attributes, list):
            attributes = list(attributes)

        ids_att = ids_attrib(self.attributes_valid, attributes)
        dict_params = self.sampler._default_params() | kwargs

        if flag_peratt:
            vec_att = []
            for ind, att in enumerate(attributes):
                flag_range_aux = True if len(y_req[ind]) > 1 else False
                nbins_aux = nbins if len(y_req[ind]) > 1 else 1
                vec_att.append({"y_req": [y_req[ind]], "atts": [att], "dobjs": [dobj_req[ind]], "f_range": flag_range_aux, "nbins": nbins_aux})
        else:
            vec_att = [{"y_req": y_req, "atts": attributes, "dobjs": dobj_req, "f_range": flag_range, "nbins": nbins}]

        dict_out = {}
        n_samples_tot = n_samples * self.over_sample
        for ind, list_att in enumerate(vec_att):
            lists_ranges = []
            # Assembling all combinations when using binning
            for i in range(len(list_att["atts"])):
                if len(list_att["y_req"][i]) == 2 and list_att["dobjs"][i].domain.domain_type == "Interval":
                    aux_range = np.linspace(list_att["y_req"][i][0], list_att["y_req"][i][1], list_att["nbins"] + 1)
                    lists_ranges.append([[aux_range[i], aux_range[i + 1]] for i in range(len(aux_range) - 1)])
                else:
                    lists_ranges.append([list_att["y_req"][i]])
            vec_iter_par = list(itertools.product(*lists_ranges))

            # Generating samples
            # By default, untransformed. With _transf, means transformed
            x_gen, y_samp, z_samp_aux, y_samp_aux, y_req = [], [], [], [], []
            n_samples_per = int(n_samples_tot / len(vec_iter_par))
            for i, list_ranges in enumerate(vec_iter_par):
                y_aux, z_aux, y_req_aux = self.sampler.generate(
                    datablock,
                    list_ranges,
                    list_att["atts"],
                    n_samples_per,
                    request_orig_range,
                    list_att["dobjs"],
                    list_att["f_range"],
                    sample_z=not self.fast_generation,
                    model=self.model,
                    **dict_params,
                )
                y_samp_aux.append(y_aux)
                z_samp_aux.append(z_aux)
                y_req.append(y_req_aux)

                if len(y_samp_aux) * n_samples_per > max_samples_per or i == len(vec_iter_par) - 1:
                    y_samp_aux, z_samp_aux = np.vstack(y_samp_aux), np.vstack(z_samp_aux) if not self.fast_generation else None
                    _, x_gen_aux = self.model.generate(y=y_samp_aux, z=z_samp_aux, return_untransformed=True)
                    x_gen_aux = self.callbacks_class.run(x_gen_aux) if self.callbacks_class is not None else x_gen_aux
                    x_gen.append(x_gen_aux)
                    y_samp.append(y_samp_aux)
                    y_samp_aux, z_samp_aux = [], []

            att = list_att["atts"][0] if flag_peratt else "all"
            x_gen, y_samp = np.vstack(x_gen), np.vstack(y_samp)
            dict_out[att] = {
                "attributes": attributes,
                "y_req": vec_iter_par,
                "y_req_transf": y_req,
                "x_gen": x_gen,
                "y_samp": y_samp,
                "ids_att": ids_att,
            }

        return dict_out

    def _choose_best(self, dict_out: Dict[str, Dict], n_samples: int, nbins: int, dobjs: List[DataObject], flag_range: bool = False) -> Dict[str, Dict]:
        """
        Call the function that generates the sets of design parameters, either per attributes
        or for all attributes simultaneously

        Parameters
        ----------
        self : object
            The instance of the class containing this method.
        dict_out : Dict[str, Dict]
            This dictionary contains all the information gathered from the generation process.
        n_samples : int
            The number of samples of design parameters to generate.
        nbins : int
            Using `nbins` is mostly intended for plotting purposes. It allows to generate
            many different requests in a binarize interval, and compute the error. Hence, it works
            differently as a request with a provided interval
        dobjs : List[DataObject]
            A list of DataObject instances used by the sampler
        flag_range : bool, optional, default=False
            If True, indicates if the list of requests include intervals or not

        Returns
        -------
        dict_results: Dict[str, Dict]
            Dictionary created from dict_out with all the final results

        """

        def reweight(y_diff, dobjs, weights):
            # Reweight the categorical and ordinal losses
            ind_cat = [i for i, dobj in enumerate(dobjs) if dobj.type in ["categorical", "ordinal"]]
            ind_mean_err = [i for i, dobj in enumerate(dobjs) if dobj.type not in ["categorical", "ordinal"]]
            if len(ind_cat):
                mean_err = np.mean(y_diff[:, ind_mean_err])
                weights[ind_cat] = weights[ind_cat] * mean_err
            return weights.reshape(1, -1)

        def to_df(x, cols):
            return pd.DataFrame(x, columns=cols)

        dict_results = {}
        for ind, att in enumerate(dict_out.keys()):
            # Still normalized variables
            _, y_losses, x_pred, y_pred = self.model.evaluate((dict_out[att]["x_gen"], dict_out[att]["y_samp"]))
            _, y_losses_unt, _, y_pred_untransf = self.model.evaluate((dict_out[att]["x_gen"], dict_out[att]["y_samp"]), untransform=True)
            x_cols, y_cols = x_pred.columns, y_pred.columns

            # Here we use all the previous information to compute the errors, transforming them to numpy arrays
            ind_attribute = dict_out[att]["ids_att"]
            y_req, y_req_untransf = dict_out[att]["y_req_transf"], dict_out[att]["y_req"]

            y_samp_transf = self.datamodule.transform_y(dict_out[att]["y_samp"])
            x_gen_transf = self.datamodule.transform_x(dict_out[att]["x_gen"])

            y_diff_pred = np.asarray(y_losses)
            y_diff_pred_untransf = np.asarray(y_losses_unt)
            weights = reweight(y_diff_pred[:, ind_attribute], [o for i, o in enumerate(dobjs) if i in ind_attribute], np.asarray(self.weights).astype(float))
            y_diff_pred_weighted = y_diff_pred[:, ind_attribute].reshape(len(y_diff_pred), -1) * weights

            # The errors are averaged over the attributes requested, and selected per bins
            if flag_range and nbins > 1:
                # If nbins > 1, the error is not considered as in the case of single ranges. This nbin
                # option is used for plotting, when we want to generate many designs in some bin. Therefore, the errors
                # is still respect to the value requested.
                ind_sort_all = []
                ind_sort_best = []

                sampler_per = int(len(y_pred) / len(y_req))
                for ind_bin, ybin in enumerate(y_req):
                    offset_bin = int(ind_bin * sampler_per)
                    ind_bin = np.arange(offset_bin, offset_bin + sampler_per)
                    error_bin = y_diff_pred_weighted[ind_bin, :].reshape(len(y_diff_pred[ind_bin]), -1).mean(axis=-1)
                    ind_sort = np.argsort(error_bin, axis=0)
                    ind_sort_all.append(ind_bin[ind_sort])
                    ind_sort_best.append(ind_bin[ind_sort[: int(n_samples / len(y_req))]])

                ind_sort_all = np.concatenate(ind_sort_all)
                ind_sort_best = np.concatenate(ind_sort_best)

            else:
                y_req = y_req[0]
                y_req_untransf = y_req_untransf[0]
                if flag_range:
                    # For the case of intervals, the error is 0 if the value is within the interval,
                    # and the difference to the mean of the interval otherwise
                    for ind_att, pos_att in enumerate(ind_attribute):
                        if len(y_req[ind_att]) == 2 and dobjs[pos_att].domain.domain_type == "Interval":
                            valid = np.asarray(
                                (np.asarray(y_pred)[:, pos_att].flatten() >= y_req[ind_att][0]) & (np.asarray(y_pred)[:, pos_att].flatten() < y_req[ind_att][1])
                            ).flatten()
                            y_diff_pred_weighted[valid, ind_att] = 0
                            y_diff_pred_untransf[valid, pos_att] = 0
                            mean_val = 0.5 * (y_req[ind_att][0] + y_req[ind_att][1])
                            y_diff_pred_weighted[~valid, ind_att] = np.abs(np.subtract(np.asarray(y_pred)[~valid, pos_att], mean_val)) * weights[0, ind_att]
                            mean_val = 0.5 * (y_req_untransf[ind_att][0] + y_req_untransf[ind_att][1])
                            y_diff_pred_untransf[~valid, pos_att] = np.abs(np.subtract(np.asarray(y_pred_untransf)[~valid, pos_att], mean_val))
                        if len(y_req[ind_att]) >= 2 and dobjs[pos_att].domain.domain_type == "Options":
                            valid = np.isin(np.asarray(y_pred)[:, pos_att].flatten(), y_req[ind_att][0]).flatten()
                            y_diff_pred_weighted[valid, ind_att] = 0
                            y_diff_pred_untransf[valid, pos_att] = 0

                error_all_pred = y_diff_pred_weighted.reshape(len(y_diff_pred), -1).mean(axis=-1)
                ind_sort_all = np.argsort(error_all_pred, axis=0)
                ind_sort_best = ind_sort_all[:n_samples]

            error_all_pred = y_diff_pred_weighted.reshape(len(y_diff_pred), -1).mean(axis=-1)
            error_all_pred_best = error_all_pred[ind_sort_best]

            dict_results[att] = {"attributes": dict_out[att]["attributes"], "ids_att": ind_attribute, "ind_sort": ind_sort_all, "ind_sort_best": ind_sort_best}

            # Transformed
            dict_results[att]["transformed"] = {
                "y_req": y_req,
                "x_gen": to_df(x_gen_transf, x_cols).iloc[ind_sort_all],
                "x_gen_best": to_df(x_gen_transf, x_cols).iloc[ind_sort_best],
                "error_est": error_all_pred,
                "error_est_best": error_all_pred_best,
            }
            dict_vec = {"y_samp": to_df(y_samp_transf, y_cols), "y_pred": y_pred, "y_diff_pred": y_losses}
            dict_results = self._create_dict_res(dict_results, dict_vec, dict_out[att]["attributes"], ind_sort_all, ind_sort_best, att, "transformed")

            # Untransformed
            dict_results[att]["untransformed"] = {
                "y_req": y_req_untransf,
                "x_gen": to_df(dict_out[att]["x_gen"], x_cols).iloc[ind_sort_all],
                "x_gen_best": to_df(dict_out[att]["x_gen"], x_cols).iloc[ind_sort_best],
            }
            dict_vec = {"y_samp": to_df(dict_out[att]["y_samp"], y_cols), "y_pred": y_pred_untransf, "y_diff_pred": y_losses_unt}
            dict_results = self._create_dict_res(dict_results, dict_vec, dict_out[att]["attributes"], ind_sort_all, ind_sort_best, att, "untransformed")

        return dict_results

    @staticmethod
    def _create_dict_res(
        dict_out: Dict[str, Dict],
        dict_vect: Dict[str, Union[List, pd.DataFrame]],
        attributes: List[str],
        ind_sort_all: List[int],
        ind_sort_best: List[int],
        att: str,
        block: str = "transformed",
    ) -> Dict[str, Dict]:
        for key in dict_vect.keys():
            vec = dict_vect[key]
            dict_out[att][block][key] = vec[attributes].iloc[ind_sort_all]
            dict_out[att][block][key + "_best"] = vec[attributes].iloc[ind_sort_best]
            dict_out[att][block][key + "_all"] = vec.iloc[ind_sort_all]
            dict_out[att][block][key + "_all_best"] = vec.iloc[ind_sort_best]

        return dict_out

    def _dict_all_tocdn(self, dict_conv: Dict[str, Dict]) -> Dict[str, Dict]:
        """
        Converts iteratively all entries of a dictionary to numpy arrays

        Parameters
        ----------
        dict_conv : Dict[str, Dict]
            Dictionary to convert

        Returns
        -------
        dict_conv : Dict[str, Dict]
            Converted dictionary
        """
        for key in dict_conv.keys():
            if isinstance(dict_conv[key], dict):
                dict_conv[key] = self._dict_all_tocdn(dict_conv[key])
            else:
                dict_conv[key] = self._cdn(dict_conv[key])
        return dict_conv

    def _cdn(self, x: Union[torch.Tensor, np.ndarray]) -> np.ndarray:
        """
        Detachs, moves to cpu, and convert to numpy array

        Parameters
        ----------
        x : Union[torch.Tensor, np.ndarray]
            Entry to convert

        Returns
        -------
        x : np.ndarray
            x in numpy array format
        """
        if isinstance(x, torch.Tensor):
            return x.cpu().detach().numpy()
        return x
