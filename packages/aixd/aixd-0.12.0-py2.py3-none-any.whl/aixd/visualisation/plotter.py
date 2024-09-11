import base64
import os
import warnings
from itertools import chain
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly import subplots
from sklearn.metrics import accuracy_score, r2_score

import aixd.visualisation.utils_plots as up
from aixd.utils.utils import flatten_dict, flatten_list

if TYPE_CHECKING:
    from aixd.data import DataBlock, DataObject
    from aixd.data.custom_callbacks import AnalysisCallback
    from aixd.data.dataset import Dataset
    from aixd.mlmodel.architecture.cond_ae_model import CondAEModel
    from aixd.mlmodel.data.data_loader import DataModule


class Plotter:
    """
    Main class providing various pre-configured plots for analysis of the dataset and of the model's performance.


    Parameters
    ----------
    dataset : :class:`~aixd.data.dataset.Dataset`, optional, default=None
        A `Dataset` object.
    datamodule : DataModule, optional, default=None
        A DataModule object.
    model : :class:`~aixd.mlmodel.cond_ae_model.CondAEModel` or :class:`~aixd.mlmodel.cond_vae_model.CondVAEModel`, optional, default=None
        A trained machine learning model. Needed only for plots that evaluate the trained model.
    output : str, optional, default=None
        Select the type of the output for all plot methods. Default is None, and there are the following available options:

        * 'show' : opens the interactive plotly figure

        * 'image' : saves a static image in *.png format

        * 'svg' : saves a static image in *.svg format

        * 'png' :  saves a static image in *.png format

        * 'jpg' :  saves a static image in *.jpg format

        * 'html' :  saves an interactive figure as *.html file

        * 'txt' : saves a static bitmap image as a string to *.txt file

        * 'json' : save json file that can be opened again by plotly [Not implemented]

        * 'wandb' : submits figure to associated Weight&Biases account [Not implemented]

        * '' or `None` : plot methods return the :class:`plotly.graph_objects.Figure` object without outputting it anywhere

    output_dir : str, optional, default=None
        If the selected output saves a file (i.e, ), specify the target location for this file here.
    """

    def __init__(self, dataset: "Dataset" = None, datamodule: "DataModule" = None, model: "CondAEModel" = None, output: str = None, output_dir: str = None):
        if dataset is None and datamodule is None:
            raise ValueError("Either a dataset or a datamodule must be provided.")

        self.dataset = dataset
        self.datamodule = datamodule
        self.model = model
        self.output = output

        if dataset is not None:
            self.output_dir = output_dir or os.path.join(dataset.datapath, "plots")
        else:
            self.output_dir = output_dir or os.path.join(os.getcwd(), "plots")

        # Print some information about available data blocks and attributes
        self._print_obj()

    def _print_obj(self):
        """Prints the available data blocks and its attributes."""
        print("### The following blocks with attributes are available in the dataset")

        for name, block in self._available_data_blocks().items():
            extra_msg = (
                " - set `transformed=False` to show in the original domain, but after transformations"
                if name in ["inputML", "outputML"]
                else " - presented in the original data domain"
            )
            print(f"\n   {block.display_name} (={name}){extra_msg}:")
            print("     {}".format(block.info_dobj(flag_only_names=True)))

    def available_block_names(self, except_dataset: bool = False, except_datamodule: bool = False):
        """Returns a list of the names of all available data blocks."""
        return list(self._available_data_blocks(except_dataset, except_datamodule).keys())

    def _available_data_blocks(self, except_dataset: bool = False, except_datamodule: bool = False) -> Dict[str, "DataBlock"]:
        """Returns a dictionary of all available data blocks."""
        blocks = []
        if self.dataset is not None and not except_dataset:
            blocks = flatten_dict(self.dataset.data_blocks)

        if self.datamodule is not None and not except_datamodule:
            blocks += [self.datamodule.input_ml_dblock, self.datamodule.output_ml_dblock]

        return {block.name: block for block in blocks}

    def _check_load_block(self, block: str, load_set: str = "all", transformed: bool = True, **kwargs) -> "DataBlock":
        """Helper method to check if the requested block is available and load it"""
        # Check if block is available
        available_blocks = self._available_data_blocks(**kwargs)
        try:
            block = available_blocks[block]
        except KeyError:
            raise ValueError(
                f"Block {block} is not available. Available blocks are: {self.available_block_names(**kwargs)}. "
                f"Make sure that the dataset and/or datamodule are provided when initializing the Plotter, or provided as arguments to the plotting methods."
            )

        # If block is InputML or OutputML, load it from datamodule
        from aixd.data import InputML, OutputML  # To avoid circular imports, we import here

        assert load_set in ["all", "train", "val", "test"]
        if isinstance(block, InputML):
            data = self.datamodule.x if load_set == "all" else getattr(self.datamodule, f"x_{load_set}")
            return block.to_data_block(data=self.datamodule.inverse_transform_x(data) if not transformed else data, flag_transf=transformed)
        elif isinstance(block, OutputML):
            data = self.datamodule.y if load_set == "all" else getattr(self.datamodule, f"y_{load_set}")
            return block.to_data_block(data=self.datamodule.inverse_transform_y(data) if not transformed else data, flag_transf=transformed)
        else:
            return block

    @staticmethod
    def _check_blocks_attributes(blocks: Union["DataBlock", List["DataBlock"]], attributes: List[str] = None, allow_subdims: bool = False) -> Union[List[str], List[List[str]]]:
        """
        Helper method to check if the requested attributes are available for the given block(s). Preserves the output format of the input blocks. I.e., if the input is a
        single block, the output is a list of attributes, if the input is a list of blocks, the output is a list of lists of attributes. If allow_subdims=True, requested
        attributes can also be subdimensions of the DataObject's.
        """
        return_lists = isinstance(blocks, list)  # If the input is a list of blocks, we return a list of lists of attributes, else we return a list of attributes
        blocks = [blocks] if not isinstance(blocks, list) else blocks

        if allow_subdims:
            blocks_attributes = [block.names_list + [c for dobj in block.dobj_list for c in dobj.columns_df] for block in blocks]
        else:
            blocks_attributes = [block.names_list for block in blocks]
        blocks_names = [block.name for block in blocks]

        if attributes is not None:
            blocks_attributes_filtered = [np.unique([attr for attr in attrs if attr in attributes]).tolist() for attrs in blocks_attributes]
            if len(list(chain(*blocks_attributes_filtered))) == 0:
                raise ValueError(
                    f"None of the requested attributes {attributes} are available for blocks: {blocks_names}. Available attributes are: {list(chain(*blocks_attributes))}"
                )

            attributes_not_found = [attr for attr in attributes if attr not in list(chain(*blocks_attributes_filtered))]
            if len(attributes_not_found) > 0:
                warnings.warn(f"Attributes {attributes_not_found} are not available for blocks {blocks_names}, so they will be ignored.")
        else:
            # If no attributes are provided, we take all attributes. If allow_subdims=True, we also return the names of the data object, as otherwise
            # this would lead to too many traces/plots in the figures
            blocks_attributes_filtered = [block.names_list for block in blocks]

        return blocks_attributes_filtered[0] if not return_lists else blocks_attributes_filtered

    @staticmethod
    def _check_dobj_types(dobj_list: List["DataObject"], allowed_types: List[str] = None) -> List["DataObject"]:
        if allowed_types is None:
            return dobj_list

        dobj_list_filtered = [dobj for dobj in dobj_list if dobj.type in allowed_types]
        dropped_dobjs = [dobj.name for dobj in dobj_list if dobj not in dobj_list_filtered]
        if len(dropped_dobjs) > 0:
            warnings.warn(f"Ignoring the following attributes, because they are not of type {allowed_types}: {dropped_dobjs}")

        return dobj_list_filtered

    def _check_args(
        self, blocks: Union[str, List[str]], attributes: List[str] = None, allow_subdims: bool = False, **kwargs
    ) -> Tuple[Union["DataBlock", List["DataBlock"]], Union[List[str], List[List[str]]]]:
        """Helper method to check if the requested blocks and attributes are available. For blocks, it also loads the block if it is of type InputML or OutputML by default."""
        blocks = self._check_load_block(blocks, **kwargs) if isinstance(blocks, str) else [self._check_load_block(block, **kwargs) for block in blocks]
        attributes = self._check_blocks_attributes(blocks, attributes, allow_subdims)

        return blocks, attributes

    def _check_load_flag_compare_to_error(self, block: "DataBlock", flag_compare_to_error: bool) -> Tuple[bool, np.ndarray]:
        """Helper method to check if the flag_compare_to_error is valid and load the error vector if needed."""
        from aixd.data import DesignParameters, PerformanceAttributes  # To avoid circular imports, we import here

        if flag_compare_to_error and self.dataset is None:
            raise ValueError("Dataset is not available, so flag_compare_to_error=True cannot be used.")

        if flag_compare_to_error and not isinstance(block, (DesignParameters, PerformanceAttributes)):
            warnings.warn(f'Block "{block.name}" is not of type DesignParameters or PerformanceAttributes, so the flag_compare_to_error=True is ignored.')
            flag_compare_to_error = False

        if flag_compare_to_error:
            error_vec = np.asarray(self.dataset.perf_attributes.data["error"])
            if set(np.unique(error_vec)) == {0}:  # check, if there are errors, if not we ignore the flag
                warnings.warn("No samples with errors found in the data, so flag_compare_to_error=True will be ignored.")
                flag_compare_to_error = False
        else:
            error_vec = None

        return flag_compare_to_error, error_vec

    @staticmethod
    def _combine_blocks_to_df_withdims(blocks: List["DataBlock"], attributes: List[List[str]]) -> pd.DataFrame:
        """Helper method to convert blocks to a single pandas dataframe with the selected attributes and correct data types."""

        # Check if we have duplicate attributes across blocks and if yes, append the block name to the attribute name
        all_cols = flatten_list([block.get_cols_dobjs(attrs, combined=True)[1] for block, attrs in zip(blocks, attributes)])
        has_duplicated_cols = len(all_cols) != len(set(all_cols))
        if has_duplicated_cols:
            warnings.warn("Duplicate attributes found across blocks. Appending block name as prefix to attribute names.")

        df_list = []
        for block, attrs in zip(blocks, attributes):
            dobjs, cols_names = block.get_cols_dobjs(attrs, combined=True)

            # Construct the labels and dtypes for the selected data from this particular block
            labels = []
            dtypes = []
            for dobj, cols in zip(dobjs, cols_names):
                if has_duplicated_cols:
                    labels.extend([up.append_unit(f"{block.name}.{col}", dobj.unit) for col in cols])
                else:
                    labels.extend([up.append_unit(col, dobj.unit) for col in cols])
                dtypes.extend([dobj.dtype for _ in cols])

            selected_block_data = block.data[flatten_list(cols_names)].astype(dict(zip(flatten_list(cols_names), dtypes)))
            selected_block_data.columns = labels
            df_list.append(selected_block_data)

        return pd.concat(df_list, axis=1)

    def distrib_attributes(
        self,
        block: str,
        attributes: List[str] = None,
        transformed: bool = False,
        per_column: bool = False,
        n_cols: int = 3,
        sub_figs: bool = False,
        bottom_top: Tuple[float, float] = (0.1, 0.9),
        downsamp: int = 2,
        flag_compare_to_error: bool = False,
        output_name: str = None,
    ) -> Optional[go.Figure]:
        """
        Plots the distribution of all the selected attributes (= DataObject's) in the given data block.

        Parameters
        ----------
        block : str
            Name of the data block to be plotted. The block must be available in the dataset or in the datamodule.
        attributes : List[str], optional, default=None
            List of attributes (= names of DataObject's) to be plotted. If None, all attributes are plotted.
        transformed : bool, optional, default=False
            If True, the data is plotted transformed, while False returns the plots it in its original domain
        per_column : bool, optional, default=False
            If True, each column (= dimension) of a DataObject is plotted as separate trace, otherwise all data is flattened to a single trace.
        n_cols : int, optional, default=3
            Number of columns in the plot. Argument is ignored if sub_figs=True.
        sub_figs : bool, optional, default=False
            If True, each trace is plotted in a separate figure.
        bottom_top : Tuple[float, float], optional, default=(0.1, 0.9)
            Tuple of two floats, defining the percentile lines (bottom and top) to be plotted in the histogram as vertical lines.
        downsamp : int, optional, default=2
            Down-sampling factor for the data.
        flag_compare_to_error : bool, optional, default=False
            If True, the distribution of the selected attributes is plotted for the samples with and without errors separately as two traces.
        output_name : str, optional, default=None
            Name of the output file. If None, the name is automatically generated from the block name.

        Returns
        -------
        Optional[:class:`plotly.graph_objects.Figure`]
            Plotly figure object, if self.output is None, otherwise None.

        """
        if isinstance(block, list):
            block = block[0]
            print("* Only a single block is allowed for this plot. Using the first block in the list.")

        # Check block and attributes compatibility
        block, attributes = self._check_args(block, attributes, transformed=transformed)

        # Check if flag_compare_to_error is valid, and if yes, load error vector
        flag_compare_to_error, error_vec = self._check_load_flag_compare_to_error(block, flag_compare_to_error)

        # Compute number of rows and columns
        dobj_list = block.get_dobjs(dobj_names=attributes)
        n_traces = sum([dobj.dim for dobj in dobj_list]) if per_column else len(dobj_list)

        if len(set([dobj.dtype for dobj in dobj_list])) > 1:
            sub_figs = True  # If we have different data types, we plot each trace in a separate figure

        if sub_figs:
            n_rows, n_cols = (1, n_traces) if n_traces < n_cols else (int(np.ceil(n_traces / n_cols)), n_cols)
        else:
            n_rows, n_cols = 1, 1

        # Plot traces
        fig = self._open_fig((n_rows, n_cols))
        i = 0  # Counter for the traces
        for dobj in dobj_list:
            cols = dobj.columns_df if per_column else [dobj.columns_df]
            for col in cols:
                # Add trace
                pos = (i // n_cols + 1, i % n_cols + 1) if sub_figs else (1, 1)

                trace_name = col if per_column else dobj.name
                trace_name = up.append_unit(trace_name, dobj.unit)
                if flag_compare_to_error:
                    assert error_vec is not None
                    dobj.plot_distrib(fig, data=block.data.iloc[error_vec == 0], cols=col, name_plot=trace_name + " No error", pos=pos, downsamp=downsamp)
                    dobj.plot_distrib(fig, data=block.data.iloc[error_vec == 1], cols=col, name_plot=trace_name + " Error", pos=pos, downsamp=downsamp)
                else:
                    fig = dobj.plot_distrib(fig, data=block.data, cols=col, name_plot=trace_name, pos=pos, downsamp=downsamp)

                # Add bottom and top lines
                if (sub_figs or n_traces == 1) and dobj.type in ["real", "integer"]:
                    fig = up.add_bottom_top(fig, data=np.asarray(block.data[col]), bottom=bottom_top[0], top=bottom_top[1], pos=pos)

                # Add x-axis title
                if sub_figs or n_traces == 1:
                    fig.update_xaxes(title_text=trace_name, row=pos[0], col=pos[1])

                i += 1

        assert i == n_traces  # Check that all traces have been added

        if sub_figs and n_traces > 1:
            fig.update_layout(height=300 * n_rows, width=300 * n_cols)
        else:
            fig.update_layout(barmode="overlay", height=640, width=640)
            fig.update_traces(opacity=0.7)

        fig.update_layout(title=f"Distribution of selected attributes from {block.display_name}")

        return self._output(fig, output_name=output_name or block.name + "_distribution1d")

    def kde_distribution_attributes(
        self,
        block: str,
        attributes: List[str] = None,
        transformed: bool = False,
        per_column: bool = False,
        n_cols: int = 3,
        sub_figs: bool = False,
        cumulative: bool = False,
        output_name: str = None,
    ) -> Optional[go.Figure]:
        """
        Plots the probability density distribution or/and the cumulative density distribution of all the selected attributes (= DataObject's)
        in the given data block using kernel density estimation.

        Parameters
        ----------
        block : str
            Name of the data block to be plotted. The block must be available in the dataset or in the datamodule.
        attributes : List[str], optional, default=None
            List of attributes (= names of DataObject's) to be plotted. If None, all attributes are plotted.
        transformed : bool, optional, default=False
            If True, the data is plotted transformed, while False returns the plots it in its original domain
        per_column : bool, optional, default=False
            If True, each column (= dimension) of a DataObject is plotted as separate trace, otherwise all data is flattened to a single trace.
        n_cols : int, optional, default=3
            Number of columns in the plot. Argument is ignored if sub_figs=True.
        sub_figs : bool, optional, default=False
            If True, each trace is plotted in a separate figure.
        cumulative : str, optional, default=False
            If True, the cumulative density distribution is plotted instead of the probability density distribution.e
        output_name : str, optional, default=None
            Name of the output file. If None, the name is automatically generated from the block name.

        Returns
        -------
        Optional[:class:`plotly.graph_objects.Figure`]
            Plotly figure object, if self.output is None, otherwise None.

        """
        # Check block and attributes compatibility
        block, attributes = self._check_args(block, attributes, transformed=transformed)

        # Compute number of rows and columns
        dobj_list = block.get_dobjs(dobj_names=attributes)
        dobj_list = self._check_dobj_types(dobj_list, allowed_types=["real"])
        n_traces = sum([dobj.dim for dobj in dobj_list]) if per_column else len(dobj_list)

        if sub_figs:
            n_rows, n_cols = (1, n_traces) if n_traces < n_cols else (int(np.ceil(n_traces / n_cols)), n_cols)
        else:
            n_rows, n_cols = 1, 1

        # Plot traces
        fig = self._open_fig((n_rows, n_cols))
        i = 0  # Counter for the traces
        for dobj in dobj_list:
            cols = dobj.columns_df if per_column else [dobj.columns_df]
            for col in cols:
                # Add trace
                pos = (i // n_cols + 1, i % n_cols + 1) if sub_figs else (1, 1)
                trace_name = col if per_column else dobj.name
                trace_name = up.append_unit(trace_name, dobj.unit)
                fig = up.add_kde_trace(fig, data=block.data[col], title=trace_name, cumulative=cumulative, pos=pos)

                # Add x-axis title
                if sub_figs or n_traces == 1:
                    fig.update_xaxes(title_text=trace_name, row=pos[0], col=pos[1])

                i += 1

        assert i == n_traces  # Check that all traces have been added

        if sub_figs and n_traces > 1:
            fig.update_layout(height=300 * n_rows, width=300 * n_cols)
        else:
            fig.update_layout(barmode="overlay", height=640, width=1080)
            fig.update_traces(opacity=0.7)

        if cumulative:
            fig.update_layout(title=f"Cumulative density distribution (CDF) for selected attributes of {block.display_name}")
            return self._output(fig, output_name=output_name or block.name + "_cumulative_distribution")
        else:
            fig.update_layout(title=f"Probability density distribution (PDF) for selected attributes of {block.display_name}")
            return self._output(fig, output_name=output_name or block.name + "_probability_distribution")

    def contours2d(
        self, block: str, attributes: List[str] = None, transformed: bool = False, downsamp: int = 2, smoothing: float = 1, output_name: str = None
    ) -> Optional[go.Figure]:
        """
        Plots the 2D contours of all the selected attributes (= DataObject's) in the given data block.

        Parameters
        ----------
        block : str
            Name of the data block to be plotted. The block must be available in the dataset or in the datamodule.
        attributes : List[str], optional, default=None
            List of attributes (= names of DataObject's) to be plotted. If None, all attributes of the block are plotted.
        transformed : bool, optional, default=False
            If True, the data is plotted transformed, while False returns the plots it in its original domain
        downsamp : int, optional, default=2
            Down-sampling factor for the data.
        smoothing : float, optional, default=1
            Smoothing factor between 0 and 1.3 for the contours lines in the contour plot.
        output_name : str, optional, default=None
            Name of the output file. If None, the name is automatically generated from the data block name.

        Returns
        -------
        Optional[:class:`plotly.graph_objects.Figure`]
            Plotly figure object, if self.output is None, otherwise None.
        """
        # Check block and attributes compatibility
        block, attributes = self._check_args(block, attributes, allow_subdims=True, transformed=transformed)

        n_rows, n_cols = len(attributes), len(attributes)
        fig = self._open_fig((n_rows, n_cols))

        # Get data and data objects for selected attributes
        dobj_list, cols_names = block.get_cols_dobjs(attributes)

        for ir, (dobj_r, cols_r) in enumerate(zip(dobj_list, cols_names)):
            for ic, (dobj_c, cols_c) in enumerate(zip(dobj_list, cols_names)):
                if ir == ic:
                    name = dobj_r.name if len(cols_r) > 1 else cols_r[0]
                    plot_name = up.append_unit(name, dobj_r.unit)
                    fig = dobj_r.plot_distrib(fig, data=block.data[cols_r], name_plot=plot_name, pos=(ir + 1, ic + 1), downsamp=downsamp)
                    fig.update_xaxes(title_text=plot_name, row=ir + 1, col=ic + 1)
                elif ic > ir:
                    flag_v = bool(dobj_r.type in ["categorical", "ordinal"]) + bool(dobj_c.type in ["categorical", "ordinal"])
                    options = [
                        dobj_r.domain.array if dobj_r.type in ["categorical", "ordinal"] else None,
                        dobj_c.domain.array if dobj_c.type in ["categorical", "ordinal"] else None,
                    ]
                    fig = up.contour2d(
                        fig,
                        x=np.asarray(block.data[cols_c])[::downsamp],
                        y=np.asarray(block.data[cols_r])[::downsamp],
                        pos=(ir + 1, ic + 1),
                        flag_v=flag_v,
                        options=options,
                        line={"smoothing": smoothing},
                    )
                else:
                    pass  # no plots in the lower triangle

        fig.update_layout(height=300 * n_rows, width=300 * n_cols, title="1D and 2D distributions for selected attributes")
        return self._output(fig, output_name=output_name or block.name + "_contours2d")

    def distrib_attributes2d(
        self, block: Union[str, List[str]], attributes: List[str] = None, transformed: bool = False, downsamp: int = 2, output_name: str = None
    ) -> Optional[go.Figure]:
        """
        Plots the 2D joint distribution of all the selected attributes (= DataObject's) in the given data blocks.

        Parameters
        ----------
        block : Union[str, List[str]]
            Name or list of names of the data blocks to be plotted. The blocks must be available in the dataset or in the datamodule.
        attributes : List[str], optional, default=None
            List of attributes (= names of DataObject's) to be plotted. If None, all attributes of the blocks are plotted.
        transformed : bool, optional, default=False
            If True, the data is plotted transformed, while False returns the plots it in its original domain
        downsamp : int, optional, default=2
            Down-sampling factor for the data.
        output_name : str, optional, default=None
            Name of the output file. If None, the name is automatically generated from the data block names.

        Returns
        -------
        Optional[:class:`plotly.graph_objects.Figure`]
            Plotly figure object, if self.output is None, otherwise None.
        """
        blocks = [block] if isinstance(block, str) else block
        blocks, blocks_attributes = self._check_args(blocks, attributes, allow_subdims=True, transformed=transformed)
        data = self._combine_blocks_to_df_withdims(blocks, blocks_attributes)

        fig = px.scatter_matrix(data.iloc[::downsamp], dimensions=data.columns)
        fig.update_layout(title="Joint distribution of pairs of selected attributes", height=300 * len(data.columns), width=300 * len(data.columns))

        return self._output(fig, output_name=output_name or "_".join([block.name for block in blocks]) + "_distribution2d")

    def correlation(self, block: Union[str, List[str]], attributes: List[str] = None, output_name: str = None, color_range: str = "unit") -> Optional[go.Figure]:
        """
        Plots the correlation between all the selected attributes (= DataObject's) in the given data blocks. Only numeric attributes are considered.

        Parameters
        ----------
        block : Union[str, List[str]]
            Name or list of names of the data blocks to be plotted. The blocks must be available in the dataset or in the datamodule.
        attributes : List[str], optional, default=None
            List of attributes (= names of DataObject's) to be plotted. If None, all attributes of the blocks are plotted.
        output_name : str, optional, default=None
            Name of the output file. If None, the name is automatically generated from the data block names.
        color_range: str, optional, default='unit'
            The range of the color scale. Possible values are 'unit', 'auto', 'symmetric'.
            If 'unit', the color scale is fixed to [-1, 1].
            If 'auto', the color scale is automatically adjusted to the data [min, max].
            If 'symmetric', the color scale is fixed to the maximum absolute value `a` of the data [-a, a].
        Returns
        -------
        Optional[:class:`plotly.graph_objects.Figure`]
            Plotly figure object, if self.output is None, otherwise None.

        """
        blocks = [block] if isinstance(block, str) else block
        blocks, blocks_attributes = self._check_args(blocks, attributes, allow_subdims=True)
        data = self._combine_blocks_to_df_withdims(blocks, blocks_attributes)

        data_numeric = data.select_dtypes(include=["number"]).astype(float)
        dropped_cols = [col for col in data.columns if col not in data_numeric.columns]
        if len(dropped_cols) > 0:
            warnings.warn(f"Columns {dropped_cols} are not numeric and will be ignored.")

        corr = data_numeric.corr()
        fig = px.imshow(corr, text_auto=True)

        if color_range == "unit":
            cmin, cmax = -1, 1
        elif color_range == "auto":
            cmin, cmax = corr.values.min(), corr.values.max()
        elif color_range == "symmetric":
            minmax = max(abs(corr.values.min()), abs(corr.values.max()))
            cmin, cmax = -minmax, minmax
        else:
            raise ValueError(f"Invalid value for color_range: {color_range}. Possible values are 'unit', 'auto', 'symmetric'.")

        fig.update_layout(
            title="Correlation between pairs of selected attributes",
            height=300 * len(data_numeric.columns),
            width=300 * len(data_numeric.columns),
            coloraxis=dict(colorscale="RdBu", cmin=cmin, cmax=cmax),
        )

        return self._output(fig, output_name=output_name or "_".join([block.name for block in blocks]) + "_correlation")

    def evaluate_training(
        self,
        attributes: List[str] = None,
        range_bins: List[List[Tuple[float, float]]] = None,
        transformed: bool = False,
        per_column: bool = False,
        bottom_top: Tuple[float, float] = (None, None),
        downsamp: int = 2,
        n_bins: int = 10,
        datamodule: "DataModule" = None,
        output_name: str = None,
    ) -> Optional[go.Figure]:
        """
        Compact plot for evaluating the training of the (V)AE model, in which there is a subplot for each selected attribute with the following traces:

            * Density plot of the attribute for the training and validation set.
            * Mean evaluation loss with confidence interval of the attribute for the validation data (= y error) binned across the attributes domain
            * Mean evaluation loss with confidence interval of the input data (= x error) binned across the attributes domain
            * Percentile lines (bottom and top) of the attribute's density for training data (optional)

        Parameters
        ----------
        attributes : List[str], optional, default=None
            List of attributes (= names of DataObject's) to select. If None, all attributes (specified in DataModule.output_ml_dblock) are considered.
        range_bins : List[List[Tuple[float, float]]], optional, default=None
            To specify a custom range where to obtain the bins to evaluate the training. If None, the range is obtained from the training data.
        transformed : bool, optional, default=False
            If True, the data is plotted transformed, while False returns the plots it in its original domain
        per_column : bool, optional, default=False
            If True, multi-dimensional attributes are plotted as separate traces and subplots, otherwise all data is flattened to a single trace.
        bottom_top : Tuple[float, float], optional, default=(None, None)
            Tuple of two floats, defining the percentile lines (bottom and top) to be plotted in the histogram as vertical lines.)
        downsamp : int, optional, default=2
            Down-sampling factor for the data.
        n_bins : int, optional, default=10
            Number of bins used for the error traces.
        datamodule : DataModule, optional, default=None
            A DataModule object used for evaluation. If None, the datamodule provided when creating the plotter is used.
        output_name : str, optional, default=None
            Name of the output file.

        Returns
        -------
        Optional[:class:`plotly.graph_objects.Figure`]
            Plotly figure object, if self.output is None, otherwise None.
        """
        return self._evaluate_train_gen(
            attributes, transformed, per_column, bottom_top, downsamp, range_bins, n_bins, datamodule=datamodule, output_name=output_name, flag_eval_train=True
        )

    def evaluate_generation(
        self,
        attributes: List[str] = None,
        range_bins: List[List[Tuple[float, float]]] = None,
        transformed: bool = False,
        bottom_top: Tuple[float, float] = (None, None),
        downsamp: int = 2,
        n_bins: int = 10,
        n_samples_per_bin=100,
        oversampling_gen: int = 10,
        datamodule: "DataModule" = None,
        output_name: str = None,
        analyzer: "AnalysisCallback" = None,
    ) -> Optional[go.Figure]:
        """
        Compact plot for evaluating the generation capabilities of the (V)AE model, in which there is a subplot for each selected attribute with the following traces:

            * Density plot of the attribute for the training and validation set.
            * Mean design error with confidence interval of the attribute for all generated samples binned across the attributes domain (design error n/n),
              where n := oversampling_gen * n_samples_per_bin
            * Mean design error with confidence interval of the attribute for the best generated samples binned across the attributes domain (design error m/n),
              where m := n_samples_per_bin and n := oversampling_gen * n_samples_per_bin
            * Percentile lines (bottom and top) of the attribute's density for training data (optional)

        Parameters
        ----------
        attributes : List[str], optional, default=None
            List of attributes (= names of DataObject's) to select. If None, all attributes (specified in DataModule.output_ml_dblock) are considered.
        range_bins : List[List[Tuple[float, float]]], optional, default=None
            To specify a custom range where to obtain the bins to evaluate the training. If None, the range is obtained from the training data.
        transformed : bool, optional, default=False
            If True, the data is plotted transformed, while False returns the plots it in its original domain
        bottom_top : Tuple[float, float], optional, default=(None, None)
            Tuple of two floats, defining the percentile lines (bottom and top) to be plotted in the histogram as vertical lines.
        downsamp : int, optional, default=2
            Down-sampling factor for the data.
        n_bins : int, optional, default=10
            Number of bins used for the error traces.
        n_samples_per_bin : int, optional, default=100
            Number of samples per bin used for the error traces.
        oversampling_gen : int, optional, default=10
            Oversampling factor defining the factor of oversampling.
        datamodule : DataModule, optional, default=None
            A DataModule object used for evaluation. If None, the datamodule provided when creating the plotter is used.
        output_name : str, optional, default=None
            Name of the output file.
        analyzer : AnalysisCallback, optional, default=None
            If provided, the generator will use the analyzer to compute the ground truth values. This is
            only possible when the InputML and OutputML are aligned with the DesignParameters and the
            PerformanceAttributes. If not, these values won't be computed.

        Returns
        -------
        Optional[:class:`plotly.graph_objects.Figure`]
            Plotly figure object, if self.output is None, otherwise None.
        """
        return self._evaluate_train_gen(
            attributes, transformed, True, bottom_top, downsamp, range_bins, n_bins, n_samples_per_bin, oversampling_gen, datamodule, output_name, False, analyzer
        )

    @staticmethod
    def _check_r_bin(range_bins: List[List[Tuple[float, float]]], attributes: List[str]) -> List[List[Tuple[float, float]]]:
        if range_bins is not None:
            range_bins = range_bins if isinstance(range_bins[0], list) else [range_bins]
            if len(range_bins) != len(attributes):
                warnings.warn(f"Length of range_bins {len(range_bins)} does not match the number of attributes {len(attributes)}.")
                range_bins = None
            else:
                for indb, rbin in enumerate(range_bins):
                    if len(rbin) != 2:
                        warnings.warn(f"Each range_bin should be a list of two tuples, but got: {rbin}")
                        range_bins = None
                        break
                    if rbin[0] > rbin[1]:
                        warnings.warn(f"First element of the range_bin should be smaller than the second element, but got: {rbin}. Swapping values.")
                        range_bins[indb] = [rbin[1], rbin[0]]

        return range_bins

    def _evaluate_train_gen(
        self,
        attributes: List[str] = None,
        transformed: bool = False,
        per_column: bool = False,
        bottom_top: Tuple[float, float] = (None, None),
        downsamp: int = 2,
        range_bins: List[List[Tuple[float, float]]] = None,
        n_bins: int = 10,
        n_samples_per_bin=100,
        oversampling_gen: int = 10,
        datamodule: "DataModule" = None,
        output_name: str = None,
        flag_eval_train=True,
        analyzer: "AnalysisCallback" = None,
    ):
        """
        Helper method for evaluating the training or generation capabilities of the (V)AE model. See Plotter.evaluate_training() and Plotter.evaluate_generation() for details.
        """
        # Checking it either corresponds to the number of attributes, or it is none
        range_bins = self._check_r_bin(range_bins, attributes)

        self.datamodule = datamodule or self.datamodule
        if self.datamodule is None:
            raise ValueError("No datamodule provided.")

        if self.model is None:
            raise ValueError("No model provided. You need to provide one when creating the plotter.")

        output_ml_dblock = self.datamodule.output_ml_dblock
        attributes = self._check_blocks_attributes(output_ml_dblock, attributes)

        # Get data and data objects for selected attributes
        y_train = self.datamodule.y_train if transformed else self.datamodule.inverse_transform_y(self.datamodule.y_train)
        y_train_df = pd.DataFrame(y_train, columns=self.datamodule.output_ml_dblock.columns_df_transf)
        y_val = self.datamodule.y_val if transformed else self.datamodule.inverse_transform_y(self.datamodule.y_val)
        y_val_df = pd.DataFrame(y_val, columns=output_ml_dblock.columns_df_transf)

        # Get data objects for selected attributes, and check if their types are supported
        dobj_list = output_ml_dblock.to_data_block(flag_transf=True).get_dobjs(dobj_names=attributes)

        if flag_eval_train:
            dobj_list = self._check_dobj_types(dobj_list, ["real", "integer", "ordinal", "categorical"])
        else:
            # Only data objects with domains specified as intervals are supported for now.
            dobj_list = self._check_dobj_types(dobj_list, ["real", "integer"])

        n_plots = sum([dobj.dim for dobj in dobj_list]) if per_column else len(dobj_list)

        if n_plots == 0:
            warnings.warn("No attributes selected. Nothing to plot.")
            return None

        fig = self._open_fig((n_plots, 1))  # single column figure

        if flag_eval_train:
            x_eval_loss, y_eval_loss, _, _ = self.model.evaluate(self.datamodule, not transformed)
            gen = None  # no need to generate samples
            up.make_secondary_yaxis(fig, n_secondary_y=2)  # add two secondary y-axes for the attributes errors
        else:
            x_eval_loss, y_eval_loss = None, None  # no need to compute evaluation loss

            # Init generator for evaluation of the generation
            from aixd.mlmodel.generation.generator import Generator

            gen = Generator(self.model, self.datamodule)
            gen.over_sample = oversampling_gen

            up.make_secondary_yaxis(fig, n_secondary_y=1)  # add one secondary y-axis for the generation errors

        i = 0  # Counter for the plots
        for ind, dobj in enumerate(dobj_list):
            column_list = dobj.columns_df if per_column else [dobj.columns_df]
            for cols in column_list:
                name_plot = cols if per_column else dobj.name
                name_plot_with_unit = up.append_unit(name_plot, dobj.unit)

                # Density for both training and validation set
                fig = up.add_density(fig, [y_train_df], dobj, ["train"], name_plot_with_unit, cols, pos=(i + 1, 1), opacity=0.3, downsamp=downsamp, legend=f"legend{i+1}")

                # Add bottom and top lines computed based on the training data
                fig = up.add_bottom_top(fig, y_train_df[cols], bottom=bottom_top[0], top=bottom_top[1], pos=(i + 1, 1))

                if flag_eval_train:
                    # Line plot with errors, and confidence interval
                    fig = up.attribute_errors(
                        fig,
                        x_eval_loss,
                        y_eval_loss,
                        y_val_df,
                        y_train_df,
                        dobj,
                        name_plot_with_unit,
                        cols,
                        pos=(i + 1, 1),
                        n_bins=n_bins,
                        legend=f"legend{i+1}",
                        range_bins=range_bins[ind] if range_bins is not None else None,
                    )

                else:
                    # Generate samples
                    range_to_compute = range_bins[ind] if range_bins is not None else [np.min(y_train_df[cols]), np.max(y_train_df[cols])]
                    attributes = [cols]
                    y_req = [range_to_compute]
                    dict_out = gen._run(
                        y_req=y_req,
                        attributes=attributes,
                        n_samples=n_samples_per_bin * n_bins,
                        request_orig_range=not transformed,
                        flag_peratt=True,
                        nbins=n_bins,
                        analyzer=analyzer,
                    )

                    # Pick best samples and all samples
                    key_normalization = "untransformed" if not transformed else "transformed"
                    y_d_est = np.asarray(dict_out[name_plot][key_normalization]["y_diff_pred"])
                    y_d_est_best = np.asarray(dict_out[name_plot][key_normalization]["y_diff_pred_best"])
                    y_samp = np.asarray(dict_out[name_plot][key_normalization]["y_samp"])
                    y_samp_best = np.asarray(dict_out[name_plot][key_normalization]["y_samp_best"])

                    # Line plot with errors, and confidence interval
                    fig = up.errors_gen(
                        fig,
                        y_d_est,
                        y_d_est_best,
                        y_samp,
                        y_samp_best,
                        y_train_df[cols],
                        dobj,
                        name_plot_with_unit,
                        pos=(i + 1, 1),
                        n_bins=n_bins,
                        legend=f"legend{i+1}",
                        range_bins=range_bins[ind] if range_bins is not None else None,
                        leg_str="Estimated error",
                    )

                    if analyzer is not None and gen._check_analyzer_sets(analyzer):
                        y_d_gt, y_d_gt_best = np.asarray(dict_out[name_plot][key_normalization]["y_diff_gt"]), np.asarray(dict_out[name_plot][key_normalization]["y_diff_gt_best"])
                        y_samp = np.asarray(dict_out[name_plot][key_normalization]["y_samp"])
                        y_samp_best = np.asarray(dict_out[name_plot][key_normalization]["y_samp_best"])
                        fig = up.errors_gen(
                            fig,
                            y_d_gt,
                            y_d_gt_best,
                            y_samp,
                            y_samp_best,
                            y_train_df[cols],
                            dobj,
                            name_plot_with_unit,
                            pos=(i + 1, 1),
                            n_bins=n_bins,
                            legend=f"legend{i+1}",
                            range_bins=range_bins[ind] if range_bins is not None else None,
                            leg_str="Real error",
                        )

                # Set x-axis title
                fig.update_xaxes(title_text=name_plot_with_unit, row=i + 1, col=1)

                i += 1  # increment counter

        # Add one legend per subplot, in top right corner of each subplot
        legends_ys = [list(fig.select_yaxes(row=i + 1, col=1))[0].domain[1] for i in range(n_plots)]
        legend_options = {f"legend{i+1}": dict(xref="paper", yref="paper", y=y, yanchor="top") for i, y in enumerate(legends_ys)}
        fig = fig.update_layout(**legend_options)

        if flag_eval_train:
            fig.update_layout(height=420 * n_plots, title={"text": "Evaluation errors for selected attributes", "xanchor": "left", "yanchor": "top"})
        else:
            fig.update_layout(height=420 * n_plots, title={"text": "Design errors for selected attributes", "xanchor": "left", "yanchor": "top"})

        return self._output(fig, output_name=output_name or ("EvaluationError" if flag_eval_train else "DesignError"))

    def generation_scatter(
        self, generation_out: Union[List[Dict], Dict], n_samples: int = 3, downsamp: int = 2, smoothing: float = 1, output_name: str = None
    ) -> Optional[go.Figure]:
        """
        Plots the 2D contours of all the selected attributes (= DataObject's) in the given data block.

        Parameters
        ----------
        generation_out : Union[List[Dict], Dict]
            Either the single output of a generation experiment, or a list of outputs of generation experiments.
        n_samples : int, optional, default=3
            The number of samples to be plotted for each generation experiment, among the top ones.
        downsamp : int, optional, default=2
            Down-sampling factor for plotting of the contour lines.
        smoothing : float, optional, default=1
            Smoothing factor between 0 and 1.3 for the contours lines in the contour plot.
        output_name : str, optional, default=None
            Name of the output file. If None, the name is automatically generated from the data block name.

        Returns
        -------
        Optional[:class:`plotly.graph_objects.Figure`]
            Plotly figure object, if self.output is None, otherwise None.
        """

        # Either to extract the single values, or the ranges
        def get_val(vals, indx, indy, dobjx, dobjy):
            if len(vals[indx]) == 1 and len(vals[indy]) == 1:
                return [vals[indx]], [vals[indy]], 0
            elif len(vals[indx]) >= 2 and len(vals[indy]) >= 2:
                if dobjx.type in ["categorical", "ordinal"]:
                    if dobjy.type in ["categorical", "ordinal"]:
                        return [[o] * len(vals[indy]) for o in vals[indx]], [[o] * len(vals[indx]) for o in vals[indy]], 0
                    return [[o] * len(vals[indy]) for o in vals[indx]], [vals[indy]] * len(vals[indx]), 1
                if dobjy.type in ["categorical", "ordinal"]:
                    return [vals[indx]] * len(vals[indy]), [[o] for o in vals[indy]], 1
                else:
                    return (
                        [[vals[indx][0], vals[indx][1], vals[indx][1], vals[indx][0], vals[indx][0]]],
                        [[vals[indy][0], vals[indy][0], vals[indy][1], vals[indy][1], vals[indy][0]]],
                        2,
                    )
            elif len(vals[indx]) >= 2:
                if dobjx.type in ["categorical", "ordinal"]:
                    return [[o] * len(vals[indy]) for o in vals[indx]], [vals[indy]] * len(vals[indx]), 0
                return [vals[indx]], [vals[indy] * len(vals[indx])], 1
            elif len(vals[indy]) >= 2:
                if dobjy.type in ["categorical", "ordinal"]:
                    return [vals[indx]] * len(vals[indy]), [[o] * len(vals[indx]) for o in vals[indy]], 0
                return [vals[indx] * len(vals[indy])], [vals[indy]], 1

        # Auxiliary function for plotting scatter plots
        def fig_sc2d(fig, x, y, tit, lgt, ir, ic, size, marker, color, width, show_leg, opacity=1, mode="markers"):
            color_back = px.colors.sequential.Blues[0]
            for x_a, y_a in zip(x, y):
                fig = up.scatter2d(
                    fig,
                    x_a,
                    y_a,
                    title=tit[1],
                    pos=(ir, ic),
                    marker=dict(size=size, symbol=marker, color=color, line=dict(width=0, color="black")),
                    line=dict(width=width),
                    mode=mode,
                    legendgroup="_".join(tit),
                    legendgrouptitle_text=lgt,
                    showlegend=show_leg,
                    opacity=opacity,
                )
            if ir != ic:
                fig.update_xaxes(minor={"gridcolor": color_back}, gridcolor=color_back, zerolinecolor=color_back, col=ic, row=ir)
                fig.update_yaxes(minor={"gridcolor": color_back}, gridcolor=color_back, zerolinecolor=color_back, col=ic, row=ir)
                fig.update_layout(plot_bgcolor=color_back)
            else:
                fig.update_xaxes(gridwidth=3, zerolinewidth=3, col=ic, row=ir)
                fig.update_yaxes(showticklabels=False, col=ic, row=ir)
            return fig

        if isinstance(generation_out, dict):
            generation_out = [generation_out]

        # Check block and attributes compatibility
        attributes = [i for o in generation_out for i in o["all"]["attributes"]]
        if self.datamodule is None:
            raise ValueError("No datamodule provided.")
        block = self._check_load_block(self.datamodule.output_ml_dblock.name, transformed=False)
        attributes = self._check_blocks_attributes(block, attributes, allow_subdims=True)

        n_rows, n_cols = len(attributes), len(attributes)
        fig = self._open_fig((n_rows, n_cols))

        # Get data and data objects for selected attributes
        dobj_list, cols_names = block.get_cols_dobjs(attributes)

        colors = px.colors.qualitative.Plotly
        colors = colors[1:] + [colors[0]]
        data_aux = []
        for ir, (dobj_r, cols_r) in enumerate(zip(dobj_list, cols_names)):
            for ic, (dobj_c, cols_c) in enumerate(zip(dobj_list, cols_names)):
                if ic > ir:
                    flag_v = bool(dobj_r.type in ["categorical", "ordinal"]) + bool(dobj_c.type in ["categorical", "ordinal"])
                    options = [
                        dobj_r.domain.array if dobj_r.type in ["categorical", "ordinal"] else None,
                        dobj_c.domain.array if dobj_c.type in ["categorical", "ordinal"] else None,
                    ]
                    name_x, name_y = dobj_c.name if len(cols_c) > 1 else cols_c[0], dobj_r.name if len(cols_r) > 1 else cols_r[0]
                    plot_name_x = up.append_unit(name_x, dobj_c.unit)
                    plot_name_y = up.append_unit(name_y, dobj_r.unit)
                    opacity = 1 if np.sum([(name_x in gen["all"]["attributes"] and name_y in gen["all"]["attributes"]) for gen in generation_out]) else 0.3
                    fig = up.contour2d(
                        fig,
                        x=np.asarray(block.data[cols_c])[::downsamp],
                        y=np.asarray(block.data[cols_r])[::downsamp],
                        pos=(ir + 1, ic + 1),
                        flag_v=flag_v,
                        options=options,
                        line={"smoothing": smoothing},
                        opacity=opacity,
                    )
                    if ic == ir + 1:
                        fig.update_xaxes(title_text=plot_name_x, row=ir + 1, col=ic + 1)
                        fig.update_yaxes(title_text=plot_name_y, row=ir + 1, col=ic + 1)
                elif ic == ir:
                    name = dobj_r.name if len(cols_r) > 1 else cols_r[0]
                    plot_name = up.append_unit(name, dobj_r.unit)
                    args_fig = {"marker_color": "blue", "opacity": 0.5, "showlegend": False}
                    args_fig = {**args_fig, "histnorm": ""}  # if dobj_r.domain.domain_type == "Interval" else args_fig

                    data_aux.append(np.asarray(block.data[cols_r]))

                    fig = dobj_r.plot_distrib(fig, data=np.asarray(block.data[cols_r]), name_plot=plot_name, pos=(ir + 1, ic + 1), downsamp=downsamp, **args_fig)
                    fig.update_xaxes(title_text=plot_name, row=ir + 1, col=ic + 1)
                else:
                    pass  # no plots in the lower triangle

        # The following is to add markers to the plots, to show the requested and estimated samples
        count_gen = [0] * len(generation_out)
        for ig, gen in enumerate(generation_out):
            for ir, (dobj_r, cols_r) in enumerate(zip(dobj_list, cols_names)):
                for ic, (dobj_c, cols_c) in enumerate(zip(dobj_list, cols_names)):
                    if ic >= ir:
                        name_x, name_y = dobj_c.name if len(cols_c) > 1 else cols_c[0], dobj_r.name if len(cols_r) > 1 else cols_r[0]
                        if name_x in gen["all"]["attributes"] and name_y in gen["all"]["attributes"]:
                            # Plotting requested samples
                            scale = 1 if dobj_r.type in ["categorical", "ordinal"] else 0.5 * np.max(np.histogram(data_aux[ir], bins=40)[0])
                            gen_exp = gen["all"]["untransformed"]
                            x_ind, y_ind = gen["all"]["attributes"].index(name_x), gen["all"]["attributes"].index(name_y)
                            x, y, range = get_val(gen_exp["y_req"], x_ind, y_ind, dobj_c, dobj_r)
                            y = [[scale * 0.1] * len(x[0])] * len(x) if name_x == name_y else y
                            range = 1 if name_x == name_y and range == 2 else range
                            show_leg = True if count_gen[ig] == 0 else False
                            ma_mo = [["square", "markers", 0], ["square", "lines", 60], ["square", "lines", 2]][range]
                            tit = [f"Experiment {ig + 1}:", "Requested"]
                            fig = fig_sc2d(fig, x, y, tit, tit[0], ir + 1, ic + 1, 20, ma_mo[0], colors[ig % len(colors)], ma_mo[2], show_leg, 0.4, ma_mo[1])
                            x_est, y_est = np.asarray(gen_exp["y_pred_best"])[:n_samples, x_ind], np.asarray(gen_exp["y_pred_best"])[:n_samples, y_ind]
                            y_est = list(scale * np.arange(0.15, 1, 0.05)[: len(x_est)]) if name_x == name_y else y_est

                            if "y_gt_best" in gen_exp.keys():
                                x_gt, y_gt = np.asarray(gen_exp["y_gt_best"])[:n_samples, x_ind], np.asarray(gen_exp["y_gt_best"])[:n_samples, y_ind]
                                y_gt = list(scale * np.arange(0.15, 1, 0.05)[: len(x_gt)]) if name_x == name_y else y_gt
                                x_l, y_l = np.vstack([x_est, x_gt]).T, np.vstack([y_est, y_gt]).T
                                tit = ["", ""]
                                fig = fig_sc2d(
                                    fig,
                                    x_l,
                                    y_l,
                                    tit,
                                    None,
                                    ir + 1,
                                    ic + 1,
                                    8,
                                    "x",
                                    "black",
                                    1,
                                    False,
                                    mode="lines",
                                )
                                tit = [f"Experiment {ig + 1}:", "Ground truth"]
                                fig = fig_sc2d(fig, [x_gt], [y_gt], tit, None, ir + 1, ic + 1, 8, "star", colors[ig % len(colors)], 1, show_leg)

                            tit = [f"Experiment {ig + 1}:", "Estimated"]
                            fig = fig_sc2d(fig, [x_est], [y_est], tit, None, ir + 1, ic + 1, 8, "diamond", colors[ig % len(colors)], 3, show_leg)

                            count_gen[ig] += 1
                    else:
                        pass  # no plots in the lower triangle

        m_height = 300 if len(attributes) > 3 else 450
        fig.update_layout(height=m_height * n_rows, width=m_height * n_cols + 100, title=f"Best {n_samples} samples for generation experiments provided")
        return self._output(fig, output_name=output_name or block.name + "_generation")

    def attributes_obs_vs_pred(
        self,
        block: str,
        attributes: List[str] = None,
        transformed: bool = False,
        per_column: bool = False,
        downsamp: int = 1,
        n_cols: int = 1,
        datamodule: Optional["DataModule"] = None,
    ) -> Optional[go.Figure]:
        """
        Plots the observed (true) vs predicted values for all the selected attributes (= DataObject's) in the given data block of the datamodule. (InputML or OutputML). For
        categorical attributes, a confusion matrix is plotted.

        Parameters
        ----------
        block : str
            Name of the data block to be plotted. The block must be available the datamodule.
        attributes : List[str], optional, default=None
            List of attributes (= names of DataObject's) to be plotted. If None, all attributes of the block are plotted.
        transformed : bool, optional, default=False
            If True, the data is plotted transformed, while False returns the plots it in its original domain
        per_column : bool, optional, default=False
            If True, multi-dimensional attributes are plotted as separate traces and subplots, otherwise all data is flattened to a single trace.
        downsamp : int, optional, default=1
            Down-sampling factor for the data.
        n_cols : int, optional, default=1
            Number of columns in the plot.
        datamodule : DataModule, optional, default=None
            A DataModule object used for evaluation. If None, the datamodule provided when creating the plotter is used.

        Returns
        -------
        Optional[:class:`plotly.graph_objects.Figure`]
            Plotly figure object, if self.output is None, otherwise None.

        Notes
        -----
        The plot is generated using the validation set of the datamodule. Legends of the plot might not be displayed correctly in certain environments,
        see https://github.com/plotly/plotly.py/issues/4489 for more information.

        """
        self.datamodule = datamodule or self.datamodule
        if self.model is None:
            raise ValueError("No model provided. You need to provide one when creating the plotter.")
        block, attributes = self._check_args(block, attributes, load_set="val", transformed=transformed, except_dataset=True)

        dobj_list = block.get_dobjs(dobj_names=attributes)
        dobj_list = self._check_dobj_types(dobj_list, ["real", "integer", "ordinal", "categorical"])

        x_loss, y_loss, x_val_pred, y_val_pred = self.model.evaluate(self.datamodule, not transformed)
        losses = pd.concat([x_loss, y_loss], axis=1)
        preds = pd.concat([x_val_pred, y_val_pred], axis=1)

        subplot_titles = (
            [up.append_unit(col, dobj.unit) for dobj in dobj_list for col in dobj.columns_df] if per_column else [up.append_unit(dobj.name, dobj.unit) for dobj in dobj_list]
        )
        n_plots = len(subplot_titles)
        n_rows, n_cols = (1, n_plots) if n_plots < n_cols else (int(np.ceil(n_plots / n_cols)), n_cols)

        if n_cols > 1:
            fig = self._open_fig((n_rows, n_cols), vertical_spacing=0.3 / n_rows, horizontal_spacing=0.45 / n_cols, subplot_titles=subplot_titles)
        else:
            fig = self._open_fig((n_rows, n_cols), subplot_titles=subplot_titles)

        i = 0  # Counter for the plots
        for dobj in dobj_list:
            column_list = dobj.columns_df if per_column else [dobj.columns_df]
            for cols in column_list:
                pos = (i // n_cols + 1, i % n_cols + 1)
                if dobj.type in ["real", "integer"]:
                    fig = up.attribute_obs_vs_pred(fig, block.data, preds, losses, cols, downsamp=downsamp, pos=pos, legend=f"legend{i+1}")
                elif dobj.type in ["categorical", "ordinal"]:
                    labels = dobj.transform(np.asarray(dobj.domain.array)) if transformed else dobj.domain.array
                    fig = up.confusion_matrix(fig, block.data[cols].to_numpy(), preds[cols].to_numpy(), labels=labels, name=dobj.name, pos=pos)
                else:
                    assert False, "This should not happen."
                i += 1

        width = 420 * (n_cols + 0.45) if n_cols > 1 else None
        fig.update_layout(
            height=420 * n_rows, width=width, title={"text": f"Observed vs predicted values for selected attributes from {block.display_name}", "xanchor": "left", "yanchor": "top"}
        )

        return self._output(fig, output_name="ActualVsPredicted")

    def performance_summary(
        self,
        block: str,
        attributes: List[str] = None,
        per_column: Optional[bool] = False,
        output_name: Optional[str] = None,
        datamodule: Optional["DataModule"] = None,
    ) -> Optional[go.Figure]:
        """
        Plots the performance summary for all the selected attributes (= DataObject's) in the given data block of the datamodule. (InputML or OutputML).

        Parameters
        ----------
        block : str
            Name of the data block to be plotted. The block must be available the datamodule.
        attributes : List[str], optional, default=None
            List of attributes (= names of DataObject's) to be plotted. If None, all attributes of the block are plotted.
        per_column : bool, optional, default=False
            If True, scores for non-categorical multi-dimensional attributes are computed for each column separately.
        output_name : str, optional, default=None
            Name of the output file. If None, the name is automatically generated from the data block name.
        datamodule : DataModule, optional, default=None
            A DataModule object used for evaluation. If None, the datamodule provided when creating the plotter is used.

        Returns
        -------
        Optional[:class:`plotly.graph_objects.Figure`]
            Plotly figure object, if self.output is None, otherwise None.
        """
        datamodule = datamodule or self.datamodule
        if self.model is None:
            raise ValueError("No model provided. You need to provide one when creating the plotter.")
        block, attributes = self._check_args(block, attributes, load_set="val", transformed=True, except_dataset=True)

        dobj_list = block.get_dobjs(dobj_names=attributes)

        _, _, x_val_pred, y_val_pred = self.model.evaluate(datamodule, untransform=False)
        preds = pd.concat([x_val_pred, y_val_pred], axis=1)

        # Create bar plot with scores
        fig = self._open_fig((1, 1))

        # Compute scores for each attribute
        scores = []
        categorical_scores = []
        for dobj in dobj_list:
            if dobj.type != "categorical":
                column_list = dobj.columns_df if per_column else [dobj.columns_df]
                for col in column_list:
                    name = col if per_column else dobj.name
                    scores.append((name, r2_score(block.data[col], preds[col])))
            else:
                categorical_scores.append(
                    (dobj.name, accuracy_score(dobj.inverse_transform(block.get_data_mat(dobj.name)), dobj.inverse_transform(np.asarray(preds[dobj.columns_df]))))
                )

        # Add traces to figure
        if len(categorical_scores) > 0:
            fig.add_trace(go.Bar(x=[score[0] for score in categorical_scores], y=[score[1] for score in categorical_scores], name="Accuracy"), row=1, col=1)
        if len(scores) > 0:
            fig.add_trace(go.Bar(x=[score[0] for score in scores], y=[score[1] for score in scores], name="R2 score"), row=1, col=1)

        fig.update_layout(
            title=f"Performance summary of selected attributes from {block.display_name}",
            yaxis_title="score",
            height=420,
            width=np.max([640, 20 * (len(scores) + len(categorical_scores))]),
        )
        fig.update_layout(showlegend=True)

        return self._output(fig, output_name=output_name or f"PerformanceSummary_{block.name}")

    @staticmethod
    def _open_fig(size: Tuple[int, int] = (1, 1), **kwargs) -> go.Figure:
        """Helper method to open a figure with the desired number of rows and columns."""
        return subplots.make_subplots(rows=int(size[0]), cols=int(size[1]), **kwargs)

    def _output(self, fig: go.Figure, output_name: str) -> Optional[go.Figure]:
        """Helper method to output the figure in the desired format. Supported formats are: 'plot', 'image', 'svg', 'png', 'jpg', 'html', 'txt', 'json', 'wandb'."""
        if self.output is None:
            return fig
        elif self.output == "show":
            fig.show()
        elif self.output in ["txt", "png", "jpg", "svg", "pdf", "html"]:
            os.makedirs(self.output_dir, exist_ok=True)  # create output directory if it does not exist
            output_path = os.path.join(self.output_dir, output_name)
            write_image(fig, output_path, fmt=self.output)
        elif self.output == "json":
            raise NotImplementedError
        elif self.output == "wandb":
            raise NotImplementedError
        else:
            raise Exception(f"Output format {self.output} not supported.")


def write_image(fig: go.Figure, path: str, fmt: str = None) -> None:
    """
    Function to write a plotly figure to an image file.

    Parameters
    ----------
    fig : :class:`plotly.graph_objects.Figure`
        Plotly figure object.
    fmt : str
        Format of the output file. Available options: 'txt', 'png', 'jpg', 'svg', 'pdf', 'html'. If None, the format is inferred from the file extension.
    path : str, optional, default=None
        Path to the output file.
    """
    head, extension = os.path.splitext(path)

    if fmt is None and extension != "":
        fmt = extension
    else:
        fmt = fmt or "png"
        path = head + "." + fmt

    if fmt == "txt":
        img_bytes = base64.b64encode(fig.to_image())
        img_string = img_bytes.decode("utf-8")
        with open(path, "w") as f:
            f.write(img_string)
    elif fmt in ["png", "jpg", "svg", "pdf"]:
        fig.write_image(path, format=fmt)
    elif fmt == "html":
        fig.write_html(path, full_html=False, include_plotlyjs="cdn")
    else:
        raise Exception(f"Format {fmt} not supported.")
