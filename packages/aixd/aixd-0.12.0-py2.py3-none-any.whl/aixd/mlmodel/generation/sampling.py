import copy
from typing import Dict, List, Tuple, Union

import numpy as np
import torch

from aixd.data import DataBlock, DataObject
from aixd.data.data_objects import DataReal
from aixd.data.domain import Interval
from aixd.mlmodel.architecture.cond_ae_model import CondAEModel
from aixd.mlmodel.data.data_loader import DataModule
from aixd.mlmodel.utils_mlmodel import ids_attrib, to_numpy, to_torch
from aixd.sampler.operators import Add, And, Arithmetic, Equal, GreaterOrEqual, LessOrEqual, Negative, Or, Pow, Subtract
from aixd.sampler.sampler_definitions import sampler_conditional_kde, sampler_wrapper
from aixd.utils import logs

logger = logs.get_logger().get_child("mlmodel-sampling")


class GeneratorSampler:
    """
    The Generator class needs to sampled from the outputML, in order to provide these values
    as entry to the decoder. For that, it uses this specific sampler for the generator.

    Parameters
    ----------
    sampling_type : str, optional, default="kde"
        The type of sampling to be used for generation. The options are: `bayesian`, and `kde`. `kde` is the default as it is faster, using a KDE to fitted on the training data. `Bayesian` is more time consuming, as it uses an objective to perform Bayesian optimization.
    datamodule : DataModule optional, default=None
        The LightningDataModule that handles data loading and preprocessing.
    engine : str, optional, default="sobol"
        Engine used by the sampler to generate samples. The options are:
        "bayesian", "sobol", "lhc", and "random".
        Run the method `summary_sampling_types` to obtain more information.

    """

    def __init__(self, sampling_type: str = "kde", datamodule: DataModule = None, engine: str = "sobol") -> None:
        self.sampling_type = sampling_type if sampling_type in ["kde", "bayesian"] else "kde"
        self.datamodule = datamodule

        engine = "bayesian" if sampling_type == "bayesian" else engine
        self.engine = "sobol" if (sampling_type == "kde" and engine not in ["sobol", "lhc", "uniform"]) else engine

        if datamodule is None:
            logger.warning("A data module should be provided")

    def summary_sampling_types(self, flag_print: bool = True) -> Tuple[None, str]:
        """
        Just printing some extra information about the sampling types and the engines

        Parameters
        ----------
        flag_print : bool, optional, default=True
            If True, prints the information. Otherwise, returns the string.
        """

        str_sampling = """
* The sampling types are:
    - kde (default): fitting a KDE and sampling, rejecting those that do not fall in the conditions
    - bayesian: using a sampler with a Bayesian objective. Too time consuming
* Engine:
    - sobol (default), lhc, uniform
    - bayesian: using additionally the Bayesian objective
        """
        if flag_print:
            print(str_sampling)
        else:
            return str_sampling

    def _default_params(self) -> Dict[str, Union[int, float, str]]:
        """Auxiliary function required to later provide the default parameters for the sampling"""
        return {"epsilon_sampler": 0.05, "over_generation": 10}

    def generate(
        self,
        datablock: DataBlock,
        y_req: List[Union[int, float, bool, str, List]],
        attributes_req: List[str] = [],
        n_samples: int = 50,
        request_orig_range: bool = True,
        dobj_req: List[DataObject] = None,
        flag_range: bool = False,
        epsilon_sampler: float = 0.05,
        over_generation: int = 10,
        model: CondAEModel = None,
        sample_z: bool = False,
    ) -> Tuple[torch.Tensor, List]:  # kwargs depending on sampling type
        """
        The Generator class uses the instance provided, and now call generate to obtain the samples
        required to be passed to the decoder. All the possible methods for generating this samples
        are implemented here.

        Parameters:
        -----------
        self : object
            The instance of the class containing this method.

        y_req : List[int, float, bool, str, List[int, float, bool, str]]
            The values requested for each of the attributes specified. Depending on the type of attribute,
            we can have to provide an specific type. Besides, if we want to generate in an interval, we can
            alternatively provide a List.

        attributes_req : List[str]
            The list of attribute names used to run the generative process.

        n_samples : int, optional (default=50)
            The number of samples of design parameters to generate.

        request_orig_range : bool, optional (default=False)
            If True, the `y_req` is specified within the original range of the real data.

        dobj_req : List[DataObject]
            DataObject instances for the attributes requested, to be used in later steps

        flag_range : bool, optional (default=False)
            If True, indicates if the list of requests include intervals or not

        epsilon_sampler : float, optional (default=0.05)
            When using "kde" method, for specific requests, in reality we create a range
            around it for the condition, as if not we will never get samples perfectly satisfying the value.

        over_generation : int, optional (default=10)
            When using "bayesian" or "kde" method, the number of samples generated is
            n_samples * over_generation. This is because we will reject some of them, and this accelerates
            the process.

        model : CondAEModel, optional
            Required to obtain the z_train to fit the KDE

        sample_z : bool, optional (default=False)
            Flag to indicate if we want to also sample z jointly with y

        Returns:
        --------
        y_samp : torch.Tensor
            The samples generated, in a torch.Tensor format.

        y_req : List
            The requested values, in the same format as the input.
        """

        # We operate with the column indices, as it is easier to handle
        list_attr = self.datamodule.output_ml_dblock.columns_df_transf
        ids_att = ids_attrib(list_attr, attributes_req)

        # For the max number of iterations
        count_it, max_it = 1, 10

        # Start the sampling process, of y, and also z if required
        y_train = self.datamodule.inverse_transform_y(self.datamodule.y_train)

        # Getting the requested y in the required format
        y_req, y_req_transf = self._transf_untransf_y_req(y_req, ids_att, request_orig_range)

        aux_dobj = copy.copy(datablock.dobj_list_transf)

        # Assembling dobj and latent data, depending on sample_z flag
        if sample_z:
            z_train = to_numpy(model.encode(to_torch(self.datamodule.x_train, torch.float32))["z"])
            z_obj = DataReal(name="z", dim=z_train.shape[1], domain=Interval(-10, 10))
            aux_dobj.append(z_obj)
        else:
            z_train = np.array([])

        # Concatenating the latent data with the y data
        latent_train = np.concatenate([y_train, z_train], axis=1) if len(z_train) else y_train

        # Definition of objects for the y, and update of their domains
        dblock_dummy = DataBlock(name="y_z", dobj_list=aux_dobj)
        list_dom = self._get_domains_perdim(latent_train, dblock_dummy.dobj_list)
        aux_dobj = self._update_domain_dummy(list_dom, dblock_dummy.dobj_list)

        # Redo it with the updated domains
        dblock_dummy = DataBlock(name="y_z", dobj_list=aux_dobj)

        """
        In principle, the sampling for the Generator has two loops and two stopping conditions:
        1. Inner loop: the generate method of the sampler already includes a max_it condition that
        breaks the loop, even if the number of samples is not reached.
        2. Outer loop: the reason for an outer loop is that in some cases the request can be challenging.
        In this situations, we allow the epsilon sampler to increase, and try again. Still, there is a
        max_it condition, just in case.
        """

        # Starting the sampling process
        samp = np.array([])

        while True:
            # Create the condition for the sampler
            condition = self._create_condition(dobj_req, y_req, epsilon_sampler)
            objective = self._create_objective(dobj_req, y_req) if self.sampling_type == "bayesian" else None
            sampler = sampler_wrapper(aux_dobj, self.engine, objective, condition, latent_train)

            # Sampling from distribution
            y_samp_aux = sampler.generate(n_samples, output_type="numpy", over_generation=over_generation, verbose=False)
            if len(y_samp_aux):
                samp = np.vstack([samp, y_samp_aux]) if len(samp) else y_samp_aux

            count_it += 1
            if len(samp) > n_samples * 0.9:
                break
            elif count_it > max_it:
                logger.warning(f"Interrupting the generation with only {len(samp)} generated samples out of  {n_samples}")
            else:
                epsilon_sampler += epsilon_sampler * 0.2
                logger.warning("Not enough samples generated. Trying again with an epsilon for the sampler of {:.3f}".format(epsilon_sampler))

        # Assembling the final sets of y samples
        samp = samp[:n_samples, :]
        samp = self._set_req_value(samp, y_req, ids_att, flag_range)

        if sample_z:
            indexyz = [dblock_dummy.dobj_list[-1].position_index, z_obj.dim]
            y = samp[: indexyz[0]]
            z = samp[indexyz[0] :]
            return y, z, y_req_transf
        else:
            return samp, [], y_req_transf

    def generate_z(
        self,
        datablock: DataBlock,
        y_req: Union[List, np.ndarray],
        n_samples: int = 1,
        epsilon_sampler: float = 0.1,
        over_generation: int = 10000,
        model: CondAEModel = None,
    ) -> Tuple[torch.Tensor, List]:  # kwargs depending on sampling type
        """
        The Generator class uses the instance provided, and now call generate to obtain the samples
        required to be passed to the decoder. All the possible methods for generating this samples
        are implemented here.

        Parameters:
        -----------
        self : object
            The instance of the class containing this method.

        y_req : Union[List, np.ndarray]
            The values requested for each of the attributes specified. Depending on the type of attribute,
            we can have to provide an specific type. Besides, if we want to generate in an interval, we can
            alternatively provide a List.

        n_samples : int, optional (default=50)
            The number of samples of design parameters to generate.

        epsilon_sampler : float, optional (default=0.05)
            When using "kde" method, for specific requests, in reality we create a range
            around it for the condition, as if not we will never get samples perfectly satisfying the value.

        over_generation : int, optional (default=10)
            When using "bayesian" or "kde" method, the number of samples generated is
            n_samples * over_generation. This is because we will reject some of them, and this accelerates
            the process.

        model : CondAEModel
            Required to obtain the z_train to fit the KDE

        Returns:
        --------
        y_samp : torch.Tensor
            The samples generated, in a torch.Tensor format.

        y_req : List
            The requested values, in the same format as the input.
        """

        # Definition of objective given the attributes and requested values

        z_train = model.encode(to_torch(self.datamodule.x_train, torch.float32))["z"]
        z_obj = DataReal(name="z", dim=z_train.shape[1], domain=Interval(-10, 10))
        latent_train = np.concatenate([self.datamodule.y_train, to_numpy(z_train)], axis=1)

        aux_dobj = copy.copy(datablock.dobj_list_transf)
        aux_dobj.append(z_obj)
        dblock_dummy = DataBlock(name="y_z", dobj_list=aux_dobj)

        # Updating domains for dummy data objects and data blocks
        list_dom = self._get_domains_perdim(latent_train, dblock_dummy.dobj_list)
        aux_dobj = self._update_domain_dummy(list_dom, dblock_dummy.dobj_list)

        # Redo it with the updated domains
        dblock_dummy = DataBlock(name="y_z", dobj_list=aux_dobj)

        z_all = []
        max_it = 10
        for ind, y_s in enumerate(y_req):
            count = 0
            while True:
                y_s_l = [[o] for o in y_s]
                condition = self._create_condition(dblock_dummy.dobj_list[: len(datablock.dobj_list_transf)], y_s_l, epsilon_sampler)
                sampler = sampler_conditional_kde(dblock_dummy.dobj_list, self.engine, condition, latent_train)
                y_z = sampler.generate(n_samples, output_type="numpy", over_generation=over_generation, verbose=False)
                index_z = [dblock_dummy.dobj_list[-1].position_index, dblock_dummy.dobj_list[-1].position_index + z_obj.dim]
                count += 1
                if len(y_z):
                    z_all.append(y_z[:, index_z[0] : index_z[1]])

                    break
                elif count > max_it:
                    logger.info("Creating non conditioned z")
                    sampler = sampler_conditional_kde(dblock_dummy.dobj_list, self.engine, latent_train)
                    y_z = sampler.generate(n_samples, output_type="numpy", over_generation=over_generation, verbose=False)
                    z_all.append(y_z[:, index_z[0] : index_z[1]])
                    break
                else:
                    epsilon_sampler += epsilon_sampler * 0.2
                    logger.info("Increasing the epsilon for the sampler to {:.3f}".format(epsilon_sampler))

        return to_torch(np.concatenate(z_all, axis=0), torch.float32), []

    def _get_domains_perdim(self, data: np.ndarray, dobj: List[DataObject]) -> List:
        list_dom = []
        for ind, att in enumerate(dobj):
            dim_ind = [att.position_index, att.position_index + att.dim]
            if att.domain.domain_type == "Interval":
                list_dom.append([float(np.min(data[:, dim_ind[0] : dim_ind[1]])), float(np.max(data[:, dim_ind[0] : dim_ind[1]]))])
            elif att.domain.domain_type == "Options":
                list_dom.append([o for o in np.unique(data[:, dim_ind[0] : dim_ind[1]])])
        return list_dom

    def _update_domain_dummy(self, list_dom: List, dobj: List[DataObject]) -> List[DataObject]:
        for ind, att in enumerate(dobj):
            if att.domain.domain_type == "Interval":
                dobj[ind].domain.min_value = list_dom[ind][0]
                dobj[ind].domain.max_value = list_dom[ind][1]
            elif att.domain.domain_type == "Options":
                dobj[ind].domain.array = list_dom[ind]
        return dobj

    def _set_req_value(self, y_samp_unnorm: np.ndarray, y_req: List[Union[int, float, bool, str, List]], ids_att: List[int], flag_range: bool) -> np.ndarray:
        """
        Just sets back the requested values to the samples generated, as as a results of the sampling
        these are not exactly the ones requested.

        Parameters:
        -----------
        y_samp_unnorm : np.ndarray
            The samples generated, in a numpy.ndarray format.

        y_req : List[Union[int, float, bool, str, List]]
            The requested values.

        ids_att : List[int]
            The indices of the attributes requested.

        flag_range : bool
            If True, indicates if the list of requests include intervals or not

        Returns:
        --------
        y_samp_unnorm : np.ndarray
            The samples generated, in a numpy.ndarray format, with the requested values set.
        """

        if not flag_range:
            y_samp_unnorm[:, ids_att] = np.asarray(y_req).reshape(1, -1)
        else:
            for ind, req in enumerate(y_req):
                if len(req) == 1:
                    y_samp_unnorm[:, ids_att[ind]] = np.asarray(req).reshape(1, -1)
        return y_samp_unnorm

    def _transf_untransf_y_req(self, y_req: List[Union[int, float, bool, str, List]], ids_att: List[int], request_orig_range: bool) -> List:
        """
        Normalize or unnormalize the requested values, depending on the flag provided
        for request_orig_range

        Parameters:
        -----------
        y_req : List[Union[int, float, bool, str, List]]
            The requested values.

        ids_att : List[int]
            The indices of the attributes requested.

        request_orig_range : bool, optional (default=False)
            If True, the `y_req` is specified within the original range of the real data.

        Returns:
        --------
        y_req_conv: List
            The requested values, returned as required, as indicated by request_orig_range
        """

        norm_unorm_y_func = self.datamodule.transform_y if request_orig_range else self.datamodule.inverse_transform_y

        list_attr = self.datamodule.output_ml_dblock.columns_df_transf

        y_req_conv = []
        for ind, req in enumerate(y_req):
            y_n_un = np.zeros((len(req), len(list_attr))).astype(object)
            y_n_un[:, ids_att[ind]] = np.asarray(req).reshape(
                -1,
            )
            y_n_un = norm_unorm_y_func(y_n_un)[:, ids_att[ind]].transpose()
            y_req_conv.append(list(np.asarray(y_n_un).reshape(len(req))))

        if request_orig_range:
            return y_req, y_req_conv
        else:
            return y_req_conv, y_req

    def _create_objective(self, attributes: List[str], y_req: List[Union[int, float, bool, str, List]]) -> Arithmetic:
        """
        Provides a condition instance using the intervals of the features

        Parameters:
        -----------
        attributes : List[str]
            The list of attribute names used to run the generative process.

        y_req : List[Union[int, float, bool, str, List]]
            The requested values.

        Returns:
        --------
        condition : Arithmetic
            An arithmetic condition instance, to be used to select the valid samples
        """
        vec_conds = []
        for ind, att in enumerate(attributes):
            y_req_i = y_req[ind]
            if len(y_req_i) == 1:
                vec_conds.append(self._mse_loss(att.name, y_req_i))
        return Add(*vec_conds)

    def _create_condition(self, attributes: List[str], y_req: List[Union[int, float, bool, str, List]], epsilon_sampler: float, list_dom: List[List] = None) -> Arithmetic:
        """
        Provides a condition instance using the intervals of the features

        Parameters:
        -----------
        attributes : List[str]
            The list of attribute names used to run the generative process.

        y_req : List[Union[int, float, bool, str, List]]
            The requested values.

        epsilon_sampler : float, optional (default=0.05)
            When using "kde" method, for specific requests, in reality we create a range
            around it for the condition, as if not we will never get samples perfectly satisfying the value.

        Returns:
        --------
        objective : Arithmetic
            An arithmetic objective instance, to be used to compute performances
        """
        vec_conds = []
        for ind, att in enumerate(attributes):
            y_req_i = y_req[ind]
            # TODO @luis another condition for the categorical values
            if att.domain.domain_type == "Interval":
                if len(y_req_i) == 1:
                    list_dom_s = list_dom[ind] if list_dom is not None else None
                    range_vec = self._get_range_epsilon(att, y_req_i[0], epsilon_sampler, list_dom_s)
                else:
                    range_vec = [float(o) for o in y_req_i]
                vec_conds.append(self._condition_range(att.name, range_vec[0], range_vec[1]))
            elif att.domain.domain_type == "Options":
                vec_conds.append(self._condition_fix_val(att.name, y_req_i))

        return And(*vec_conds)

    @staticmethod
    def _get_range_epsilon(attribute: DataObject, val: Union[int, float], epsilon: float, list_dom: List = None) -> Tuple[Union[int, float], Union[int, float]]:
        """
        Just provides a range around the value provided, to be used for the creation
        of the condition
        """
        # NOTE, here we allow overflowing out of the domain. In any case,
        # the calue we will set later up
        # NOTE, we will also request the value with some epsilon for the
        # categorical values
        if list_dom is not None:
            mod_range = (np.max(list_dom[1]) - np.min(list_dom[0])) * epsilon
        else:
            mod_range = (attribute.domain.max_value - attribute.domain.min_value) * epsilon
        return [val - mod_range, val + mod_range]

    @staticmethod
    def _condition_range(name: str, min: Union[int, float], max: Union[int, float]) -> Arithmetic:
        """
        Creates condition for a range of values
        """
        return And(LessOrEqual(name, max), GreaterOrEqual(name, min))

    @staticmethod
    def _condition_fix_val(name: str, values: List) -> Arithmetic:
        """
        Creates and equal condition for a list of values
        """
        vec_conds = []
        for val in values:
            vec_conds.append(Equal(name, val))
        return Or(*vec_conds)

    @staticmethod
    def _mse_loss(name: str, values: List) -> Arithmetic:
        """
        Arithmetic operator to compute the mse loss
        """
        vec_conds = []
        for val in values:
            vec_conds.append(Negative(Pow(Subtract(name, val), 2)))
        if len(vec_conds) > 1:
            return Add(*vec_conds)
        return vec_conds[0]
