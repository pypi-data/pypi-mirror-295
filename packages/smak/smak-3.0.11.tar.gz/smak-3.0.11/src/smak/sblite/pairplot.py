import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import math

from distutils.version import LooseVersion

from .palettes import color_palette
from . import utils


def variable_type(vector, boolean_type="numeric"):
    """Determine whether a vector contains numeric, categorical, or dateime data.

    This function differs from the pandas typing API in two ways:

    - Python sequences or object-typed PyData objects are considered numeric if
      all of their entries are numeric.
    - String or mixed-type data are considered categorical even if not
      explicitly represented as a :class:pandas.api.types.CategoricalDtype`.

    Parameters
    ----------
    vector : :func:`pandas.Series`, :func:`numpy.ndarray`, or Python sequence
        Input data to test.
    binary_type : 'numeric' or 'categorical'
        Type to use for vectors containing only 0s and 1s (and NAs).

    Returns
    -------
    var_type : 'numeric', 'categorical', or 'datetime'
        Name identifying the type of data in the vector.

    """
    # Special-case all-na data, which is always "numeric"
    if pd.isna(vector).all():
        return "numeric"

    # Special-case binary/boolean data, allow caller to determine
    # This triggers a numpy warning when vector has strings/objects
    # https://github.com/numpy/numpy/issues/6784
    # Because we reduce with .all(), we are agnostic about whether the
    # comparison returns a scalar or vector, so we will ignore the warning.
    # It triggers a separate DeprecationWarning when the vector has datetimes:
    # https://github.com/numpy/numpy/issues/13548
    # This is considered a bug by numpy and will likely go away.
    with warnings.catch_warnings():
        warnings.simplefilter(
            action='ignore', category=(FutureWarning, DeprecationWarning)
        )
        if np.isin(vector, [0, 1, np.nan]).all():
            return boolean_type

    # Defer to positive pandas tests
    if pd.api.types.is_numeric_dtype(vector):
        return "numeric"

    if pd.api.types.is_categorical_dtype(vector):
        return "categorical"

    if pd.api.types.is_datetime64_dtype(vector):
        return "datetime"

    # --- If we get to here, we need to check the entries

    # Check for a collection where everything is a number

    def all_numeric(x):
        for x_i in x:
            if not isinstance(x_i, Number):
                return False
        return True

    if all_numeric(vector):
        return "numeric"

    # Check for a collection where everything is a datetime

    def all_datetime(x):
        for x_i in x:
            if not isinstance(x_i, (datetime, np.datetime64)):
                return False
        return True

    if all_datetime(vector):
        return "datetime"

    # Otherwise, our final fallback is to consider things categorical

    return "categorical"

def categorical_order_smw(data, order=None):
    u = 1
    m = max(np.ravel(data)) + 1
    b = np.mod(np.ravel(data), 1)
    if m > 31: u = 0
    if sum(abs(b)) > 0: u = 0
    if len(np.where(data < 0)[0]) > 1: u = 0
    if u == 0:
        print('not a cluster set')
        return None
    else:
        return list(range(int(m)))

def categorical_order(vector, order=None):
    """Return a list of unique data values.

    Determine an ordered list of levels in ``values``.

    Parameters
    ----------
    vector : list, array, Categorical, or Series
        Vector of "categorical" values
    order : list-like, optional
        Desired order of category levels to override the order determined
        from the ``values`` object.

    Returns
    -------
    order : list
        Ordered list of category levels not including null values.

    """
    if order is None:
        if hasattr(vector, "categories"):
            order = vector.categories
        else:
            try:
                order = vector.cat.categories
            except (TypeError, AttributeError):

                try:
                    order = vector.unique()
                except AttributeError:
                    order = pd.unique(vector)

                if variable_type(vector) == "numeric":
                    order = np.sort(order)

        order = list(filter(pd.notnull, order))
    return list(order)




class Grid(object):
    """Base class for grids of subplots."""
    _margin_titles = False
    _legend_out = True

    def __init__(self):

        self._tight_layout_rect = [0, 0, 1, 1]

    def set(self, **kwargs):
        """Set attributes on each subplot Axes."""
        for ax in self.axes.flat:
            ax.set(**kwargs)
        return self

    def savefig(self, *args, **kwargs):
        """Save the figure."""
        kwargs = kwargs.copy()
        kwargs.setdefault("bbox_inches", "tight")
        self.fig.savefig(*args, **kwargs)

    def tight_layout(self, *args, **kwargs):
        """Call fig.tight_layout within rect that exclude the legend."""
        kwargs = kwargs.copy()
        kwargs.setdefault("rect", self._tight_layout_rect)
        self.fig.tight_layout(*args, **kwargs)

    def add_legend(self, legend_data=None, title=None, label_order=None,
                   **kwargs):
        """Draw a legend, maybe placing it outside axes and resizing the figure.

        Parameters
        ----------
        legend_data : dict, optional
            Dictionary mapping label names (or two-element tuples where the
            second element is a label name) to matplotlib artist handles. The
            default reads from ``self._legend_data``.
        title : string, optional
            Title for the legend. The default reads from ``self._hue_var``.
        label_order : list of labels, optional
            The order that the legend entries should appear in. The default
            reads from ``self.hue_names``.
        kwargs : key, value pairings
            Other keyword arguments are passed to the underlying legend methods
            on the Figure or Axes object.

        Returns
        -------
        self : Grid instance
            Returns self for easy chaining.

        """
        # Find the data for the legend
        if legend_data is None:
            legend_data = self._legend_data

        if legend_data=={}: return self

        if label_order is None:
            if self.hue_names is None:
                label_order = list(legend_data.keys())
            else:
                label_order = list(map(utils.to_utf8, self.hue_names))

        blank_handle = mpl.patches.Patch(alpha=0, linewidth=0)
        handles = [legend_data.get(l, blank_handle) for l in label_order]
        title = self._hue_var if title is None else title
        if LooseVersion(mpl.__version__) < LooseVersion("3.0"):
            try:
                title_size = mpl.rcParams["axes.labelsize"] * .85
            except TypeError:  # labelsize is something like "large"
                title_size = mpl.rcParams["axes.labelsize"]
        else:
            title_size = mpl.rcParams["legend.title_fontsize"]

        # Unpack nested labels from a hierarchical legend
        labels = []
        for entry in label_order:
            if isinstance(entry, tuple):
                _, label = entry
            else:
                label = entry
            labels.append(label)

        # Set default legend kwargs
        kwargs.setdefault("scatterpoints", 1)

        if self._legend_out:

            kwargs.setdefault("frameon", False)
            kwargs.setdefault("loc", "center right")

            # Draw a full-figure legend outside the grid
            if self.hue_legend is not None:
                labels=self.hue_legend
            figlegend = self.fig.legend(handles, labels, **kwargs)

            self._legend = figlegend
            figlegend.set_title(title, prop={"size": title_size})

            # Draw the plot to set the bounding boxes correctly
            if hasattr(self.fig.canvas, "get_renderer"):
                self.fig.draw(self.fig.canvas.get_renderer())

            # Calculate and set the new width of the figure so the legend fits
            legend_width = figlegend.get_window_extent().width / self.fig.dpi
            fig_width, fig_height = self.fig.get_size_inches()
            self.fig.set_size_inches(fig_width + legend_width, fig_height)

            # Draw the plot again to get the new transformations
            if hasattr(self.fig.canvas, "get_renderer"):
                self.fig.draw(self.fig.canvas.get_renderer())

            # Now calculate how much space we need on the right side
            legend_width = figlegend.get_window_extent().width / self.fig.dpi
            space_needed = legend_width / (fig_width + legend_width)
            margin = .04 if self._margin_titles else .01
            self._space_needed = margin + space_needed
            right = 1 - self._space_needed

            # Place the subplot axes to give space for the legend
            self.fig.subplots_adjust(right=right)
            self._tight_layout_rect[2] = right

        else:
            # Draw a legend in the first axis
            ax = self.axes.flat[0]
            kwargs.setdefault("loc", "best")

            leg = ax.legend(handles, labels, **kwargs)
            leg.set_title(title, prop={"size": title_size})
            self._legend = leg

        return self

    def _clean_axis(self, ax):
        """Turn off axis labels and legend."""
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.legend_ = None
        return self

    def _update_legend_data(self, ax):
        """Extract the legend data from an axes object and save it."""
        handles, labels = ax.get_legend_handles_labels()
        data = {l: h for h, l in zip(handles, labels)}
        self._legend_data.update(data)

    def _get_palette(self, hue, hue_order, palette):
        """Get a list of colors for the hue variable."""
        if hue is None:
            palette = color_palette(n_colors=1)

        else:
            hue_names = categorical_order_smw(hue, hue_order)
            if hue_names is None:
                palette = color_palette(n_colors=1)
                return palette
            n_colors = len(hue_names)

            # By default use either the current color palette or HUSL
            if palette is None:
                current_palette = utils.get_color_cycle()
                if n_colors > len(current_palette):
                    colors = color_palette("husl", n_colors)
                else:
                    colors = color_palette(n_colors=n_colors)

            # Allow for palette to map from hue variable names
            elif isinstance(palette, dict):
                color_names = [palette[h] for h in hue_names]
                colors = color_palette(color_names, n_colors)

            # Otherwise act as if we just got a list of colors
            else:
                colors = color_palette(palette, n_colors)

            palette = color_palette(colors, n_colors)

        return palette


class PairGrid(Grid):
    """Subplot grid for plotting pairwise relationships in a dataset.

    This class maps each variable in a dataset onto a column and row in a
    grid of multiple axes. Different axes-level plotting functions can be
    used to draw bivariate plots in the upper and lower triangles, and the
    the marginal distribution of each variable can be shown on the diagonal.

    It can also represent an additional level of conditionalization with the
    ``hue`` parameter, which plots different subsets of data in different
    colors. This uses color to resolve elements on a third dimension, but
    only draws subsets on top of each other and will not tailor the ``hue``
    parameter for the specific visualization the way that axes-level functions
    that accept ``hue`` will.

    See the :ref:`tutorial <grid_tutorial>` for more information.

    """
    #@_deprecate_positional_args
    def __init__(
        self, data, vars,
        hue=None, hue_order=None, palette=None,
        hue_kws=None, xlabels=None, ylabels=None,
        corner=False, diag_sharey=True, height=2.5, aspect=1,
        layout_pad=0, despine=True, dropna=False, size=None
    ):
        """Initialize the plot figure and PairGrid object.

        Parameters
        ----------
        data : DataFrame
            Tidy (long-form) dataframe where each column is a variable and
            each row is an observation.
        hue : string (variable name), optional
            Variable in ``data`` to map plot aspects to different colors. This
            variable will be excluded from the default x and y variables.
        hue_order : list of strings
            Order for the levels of the hue variable in the palette
        palette : dict or seaborn color palette
            Set of colors for mapping the ``hue`` variable. If a dict, keys
            should be values  in the ``hue`` variable.
        hue_kws : dictionary of param -> list of values mapping
            Other keyword arguments to insert into the plotting call to let
            other plot attributes vary across levels of the hue variable (e.g.
            the markers in a scatterplot).
        vars : list of variable names, optional
            Variables within ``data`` to use, otherwise use every column with
            a numeric datatype.
        {x, y}_vars : lists of variable names, optional
            Variables within ``data`` to use separately for the rows and
            columns of the figure; i.e. to make a non-square plot.
        corner : bool, optional
            If True, don't add axes to the upper (off-diagonal) triangle of the
            grid, making this a "corner" plot.
        height : scalar, optional
            Height (in inches) of each facet.
        aspect : scalar, optional
            Aspect * height gives the width (in inches) of each facet.
        layout_pad : scalar, optional
            Padding between axes; passed to ``fig.tight_layout``.
        despine : boolean, optional
            Remove the top and right spines from the plots.
        dropna : boolean, optional
            Drop missing values from the data before plotting.

        See Also
        --------
        pairplot : Easily drawing common uses of :class:`PairGrid`.
        FacetGrid : Subplot grid for plotting conditional relationships.

        Examples
        --------

        Draw a scatterplot for each pairwise relationship:

        .. plot::
            :context: close-figs

            >>> import matplotlib.pyplot as plt
            >>> import seaborn as sns; sns.set()
            >>> iris = sns.load_dataset("iris")
            >>> g = sns.PairGrid(iris)
            >>> g = g.map(plt.scatter)

        Show a univariate distribution on the diagonal:

        .. plot::
            :context: close-figs

            >>> g = sns.PairGrid(iris)
            >>> g = g.map_diag(plt.hist)
            >>> g = g.map_offdiag(plt.scatter)

        (It's not actually necessary to catch the return value every time,
        as it is the same object, but it makes it easier to deal with the
        doctests).

        Color the points using a categorical variable:

        .. plot::
            :context: close-figs

            >>> g = sns.PairGrid(iris, hue="species")
            >>> g = g.map_diag(plt.hist)
            >>> g = g.map_offdiag(plt.scatter)
            >>> g = g.add_legend()

        Use a different style to show multiple histograms:

        .. plot::
            :context: close-figs

            >>> g = sns.PairGrid(iris, hue="species")
            >>> g = g.map_diag(plt.hist, histtype="step", linewidth=3)
            >>> g = g.map_offdiag(plt.scatter)
            >>> g = g.add_legend()

        Plot a subset of variables

        .. plot::
            :context: close-figs

            >>> g = sns.PairGrid(iris, vars=["sepal_length", "sepal_width"])
            >>> g = g.map(plt.scatter)

        Pass additional keyword arguments to the functions

        .. plot::
            :context: close-figs

            >>> g = sns.PairGrid(iris)
            >>> g = g.map_diag(plt.hist, edgecolor="w")
            >>> g = g.map_offdiag(plt.scatter, edgecolor="w", s=40)

        Use different variables for the rows and columns:

        .. plot::
            :context: close-figs

            >>> g = sns.PairGrid(iris,
            ...                  x_vars=["sepal_length", "sepal_width"],
            ...                  y_vars=["petal_length", "petal_width"])
            >>> g = g.map(plt.scatter)

        Use different functions on the upper and lower triangles:

        .. plot::
            :context: close-figs

            >>> g = sns.PairGrid(iris)
            >>> g = g.map_upper(sns.scatterplot)
            >>> g = g.map_lower(sns.kdeplot, color="C0")
            >>> g = g.map_diag(sns.kdeplot, lw=2)

        Use different colors and markers for each categorical level:

        .. plot::
            :context: close-figs

            >>> g = sns.PairGrid(iris, hue="species", palette="Set2",
            ...                  hue_kws={"marker": ["o", "s", "D"]})
            >>> g = g.map(sns.scatterplot, linewidths=1, edgecolor="w", s=40)
            >>> g = g.add_legend()

        """

        super(PairGrid, self).__init__()


        # Sort out the variables that define the grid

        x_vars = list(vars)
        y_vars = list(vars)

        self.x_vars = list(x_vars)
        self.y_vars = list(y_vars)
        self.square_grid = self.x_vars == self.y_vars


        # Create the figure and the array of subplots
        figsize = len(x_vars) * height * aspect, len(y_vars) * height
        #print height,aspect,figsize
        fig, axes = plt.subplots(len(y_vars), len(x_vars),
                                 #figsize=figsize,
                                 sharex="col", sharey="row",
                                 squeeze=False)
        #axes.set_axis_bgcolor('white')
        #axes.set_facecolor('white')
        #axes.set_edgecolor('white')
        fig.set_facecolor('white')
        for ax in list(np.ravel(axes)):
            ax.tick_params(axis='x',colors='black')#mplot.rcParams['xtick.color'] = '0.80'
            ax.tick_params(axis='y',colors='black')#mplot.rcParams['ytick.color'] = '0.80'
            ax.xaxis.label.set_color('black')
            ax.yaxis.label.set_color('black')
            ax.spines['left'].set_color('black')
            ax.spines['bottom'].set_color('black')

        # Possibly remove upper axes to make a corner grid
        # Note: setting up the axes is usually the most time-intensive part
        # of using the PairGrid. We are foregoing the speed improvement that
        # we would get by just not setting up the hidden axes so that we can
        # avoid implementing plt.subplots ourselves. But worth thinking about.
        self._corner = corner
        if corner:
            hide_indices = np.triu_indices_from(axes, 1)
            for i, j in zip(*hide_indices):
                axes[i, j].remove()
                axes[i, j] = None

        self.fig = fig
        self.axes = axes
        self.data = data
        self.hue=hue
        self.hue_legend=None
        self.xlabels=xlabels
        self.ylabels=ylabels
        if xlabels is not None and ylabels is None:
            self.ylabels=xlabels


        # Save what we are going to do with the diagonal
        self.diag_sharey = diag_sharey
        self.diag_vars = None
        self.diag_axes = None

        self._dropna = dropna

        # Label the axes
        self._add_axis_labels()

        # Sort out the hue variable
        self._hue_var = hue
        if hue is None:
            self.hue_legend = ["_nolegend_"]
            self.hue_names = ["_nolegend_"]
            self.hue_vals = ["_nolegend_"] * len(data[0])
        else:
            hue_names = categorical_order_smw(hue, hue_order)
            if hue_names is None:
                self.hue_legend = ["_nolegend_"]
                self.hue_names = ["_nolegend_"]
                self.hue_vals = ["_nolegend_"] * len(data[0])
                self.hue=None
                self._hue_var=None
            else:
                l = []
                for it in hue_names:
                    l.append('CL' + str(it))

                self._hue_var='Cluster'
                self.hue_legend = l
                self.hue_names = hue_names
                self.hue_vals = hue

        # Additional dict of kwarg -> list of values for mapping the hue var
        self.hue_kws = hue_kws if hue_kws is not None else {}

        self.palette = self._get_palette(hue, hue_order, palette)
        self._legend_data = {}

        # Make the plot look nice
        if despine:
            self._despine = True
            utils.despine(fig=fig)
        self.tight_layout(pad=layout_pad)

    def map(self, func, **kwargs):
        """Plot with the same function in every subplot.

        Parameters
        ----------
        func : callable plotting function
            Must take x, y arrays as positional arguments and draw onto the
            "currently active" matplotlib Axes. Also needs to accept kwargs
            called ``color`` and  ``label``.

        """
        row_indices, col_indices = np.indices(self.axes.shape)
        indices = list(zip(row_indices.flat, col_indices.flat))
        self._map_bivariate(func, indices, **kwargs)
        return self

    def map_lower(self, func, **kwargs):
        """Plot with a bivariate function on the lower diagonal subplots.

        Parameters
        ----------
        func : callable plotting function
            Must take x, y arrays as positional arguments and draw onto the
            "currently active" matplotlib Axes. Also needs to accept kwargs
            called ``color`` and  ``label``.

        """
        indices = list(zip(*np.tril_indices_from(self.axes, -1)))
        self._map_bivariate(func, indices, **kwargs)
        return self

    def map_upper(self, func, **kwargs):
        """Plot with a bivariate function on the upper diagonal subplots.

        Parameters
        ----------
        func : callable plotting function
            Must take x, y arrays as positional arguments and draw onto the
            "currently active" matplotlib Axes. Also needs to accept kwargs
            called ``color`` and  ``label``.

        """
        indices = list(zip(*np.triu_indices_from(self.axes, 1)))
        self._map_bivariate(func, indices, **kwargs)
        return self

    def map_offdiag(self, func, **kwargs):
        """Plot with a bivariate function on the off-diagonal subplots.

        Parameters
        ----------
        func : callable plotting function
            Must take x, y arrays as positional arguments and draw onto the
            "currently active" matplotlib Axes. Also needs to accept kwargs
            called ``color`` and  ``label``.

        """

        self.map_lower(func, **kwargs)
        if not self._corner:
            self.map_upper(func, **kwargs)
        return self

    def map_diag(self, func, yax=None, limits=True, lowerlimit=1, **kwargs):
        """Plot with a univariate function on each diagonal subplot.

        Parameters
        ----------
        func : callable plotting function
            Must take an x array as a positional argument and draw onto the
            "currently active" matplotlib Axes. Also needs to accept kwargs
            called ``color`` and  ``label``.

        """
        # Add special diagonal axes for the univariate plot

        if yax is not None:
            if yax=='Linear':
                yax='linear'
            else:
                yax='log'
        else:
            yax='linear'

        if self.diag_axes is None:
            diag_vars = []
            diag_axes = []
            for i, y_var in enumerate(self.y_vars):
                for j, x_var in enumerate(self.x_vars):
                    if x_var == y_var:

                        # Make the density axes
                        diag_vars.append(x_var)
                        ax = self.axes[i, j]
                        diag_ax = ax.twinx()
                        diag_ax.set_axis_off()
                        diag_axes.append(diag_ax)

                        # Work around matplotlib bug
                        # https://github.com/matplotlib/matplotlib/issues/15188
                        if not plt.rcParams.get("ytick.left", True):
                            for tick in ax.yaxis.majorTicks:
                                tick.tick1line.set_visible(False)

                        # Remove main y axis from density axes in a corner plot
                        if self._corner:
                            ax.yaxis.set_visible(False)
                            if self._despine:
                                utils.despine(ax=ax, left=True)
                            # TODO add optional density ticks (on the right)
                            # when drawing a corner plot?

            if self.diag_sharey:
                # This may change in future matplotlibs
                # See https://github.com/matplotlib/matplotlib/pull/9923
                group = diag_axes[0].get_shared_y_axes()
                for ax in diag_axes[1:]:
                    group.join(ax, diag_axes[0])

            self.diag_vars = np.array(diag_vars, np.object)
            self.diag_axes = np.array(diag_axes, np.object)

        # Plot on each of the diagonal axes
        fixed_color = kwargs.pop("color", None)

        for var, ax in zip(self.diag_vars, self.diag_axes):
            #hue_grouped = self.data[var].groupby(self.hue_vals)

            plt.sca(ax)

            for k, label_k in enumerate(self.hue_names):

                # Attempt to get data for this level, allowing for empty
                #try:
                #    # TODO newer matplotlib(?) doesn't need array for hist
                #    data_k = np.asarray(hue_grouped.get_group(label_k))
                #except KeyError:
                #    data_k = np.array([])
                if self.hue is None:
                    data_k = self.data[var]
                else:
                    data_k=self.data[var][np.where(self.hue==label_k)]
                if limits:
                    data_k=data_k[data_k > lowerlimit]
                if fixed_color is None:
                    color = self.palette[k]
                else:
                    color = fixed_color

                func(data_k, label=str(label_k), color=color, **kwargs)
                ax.set_yscale(yax)
            self._clean_axis(ax)

        self._add_axis_labels()

        return self

    def _map_bivariate(self, func, indices, **kwargs):
        """Draw a bivariate plot on the indicated axes."""
        #print 'plot',indices
        kws = kwargs.copy()  # Use copy as we insert other kwargs
        kw_color = kws.pop("color", None)
        for i, j in indices:
            x_var = self.x_vars[j]
            y_var = self.y_vars[i]
            ax = self.axes[i, j]
            self._plot_bivariate(x_var, y_var, ax, func, kw_color, **kws)
        self._add_axis_labels()

    def _plot_bivariate(self, x_var, y_var, ax, func, kw_color, **kwargs):
        """Draw a bivariate plot on the specified axes."""
        plt.sca(ax)
        if x_var == y_var:
            axes_vars = [x_var]
        else:
            axes_vars = [x_var, y_var]
        #hue_grouped = self.data.groupby(self.hue_vals)
        for k, label_k in enumerate(self.hue_names):

            # Attempt to get data for this level, allowing for empty
            #try:
            #    data_k = hue_grouped.get_group(label_k)
            #except KeyError:
            #    data_k = pd.DataFrame(columns=axes_vars,
            #                          dtype=np.float)
            if self.hue is None:
                x=self.data[x_var]
                y=self.data[y_var]
            else:
                x=self.data[x_var][np.where(self.hue==label_k)]
                y=self.data[y_var][np.where(self.hue==label_k)]
            #print label_k,x,y
            #x = data_k[x_var]
            #y = data_k[y_var]

            for kw, val_list in list(self.hue_kws.items()):
                kwargs[kw] = val_list[k]
            color = self.palette[k] if kw_color is None else kw_color

            func(x, y, label=label_k, color=color, **kwargs)

        self._clean_axis(ax)
        self._update_legend_data(ax)

    def _add_axis_labels(self):
        """Add labels to the left and bottom Axes."""
        for ax, label in zip(self.axes[-1, :], self.xlabels):
            ax.set_xlabel(label)
        for ax, label in zip(self.axes[:, 0], self.ylabels):
            ax.set_ylabel(label)
        if self._corner:
            self.axes[0, 0].set_ylabel("")

class GridPlot(Grid):
    def __init__(self,plotsize,palette=None,despine=True,layout_pad=0):

        super(GridPlot,self).__init__()

        ncols=int(math.sqrt(plotsize))
        if ncols!=math.sqrt(plotsize):
            ncols+=1
        nrows=int(plotsize)/ncols
        if int(plotsize)%ncols>0:
            nrows+=1
        nrows=int(nrows)
        ncols=int(ncols)
        print(nrows,ncols)
        fig, axes = plt.subplots(nrows, ncols,
                                 squeeze=False)
        fig.set_facecolor('white')
        for ind,ax in enumerate(list(np.ravel(axes))):
            if ind<plotsize:
                ax.tick_params(axis='x',colors='black')#mplot.rcParams['xtick.color'] = '0.80'
                ax.tick_params(axis='y',colors='black')#mplot.rcParams['ytick.color'] = '0.80'
                ax.xaxis.label.set_color('black')
                ax.yaxis.label.set_color('black')
                ax.spines['left'].set_color('black')
                ax.spines['bottom'].set_color('black')
            else:
                ax.xaxis.set_visible(False)
                ax.yaxis.set_visible(False)
                ax.spines['left'].set_color('white')
                ax.spines['bottom'].set_color('white')

        self.fig = fig
        self.axes = axes
        self.plotsize=plotsize
        self._plotindex=0
        self._ncols=ncols
        self._nrows=nrows

        # Label the axes
        #self._add_axis_labels()

        self.palette = self._get_palette(None, None, palette)
        self._legend_data = {}

        # Make the plot look nice
        if despine:
            self._despine = True
            utils.despine(fig=fig)

        self.tight_layout(pad=layout_pad)

    def add(self,data,labels,name,func,**kwargs):

        if self._plotindex>=self.plotsize:
            print('maximum plottage achieved')
            return self

        #get axis
        axi=int(self._plotindex/self._ncols)
        axj=int(self._plotindex%self._ncols)
        ax=self.axes[axi,axj]
        plt.sca(ax)

        kws = kwargs.copy()  # Use copy as we insert other kwargs
        kw_color = kws.pop("color", None)

        color = self.palette[0] if kw_color is None else kw_color
        #make graph
        func(data[0],data[1],color=color,**kwargs)
        self._clean_axis(ax)
        ax.set_title(name,fontsize=8)
        ax.set_xlabel(labels[0])
        ax.set_ylabel(labels[1])
        self._plotindex+=1

        return self


from scipy.stats import gaussian_kde

def plot_scpkde(data, label=None, color=None, **kwargs):
    density = gaussian_kde(data)
    xs= np.linspace(min(data),max(data),100)
    density.covariance_factor = lambda : 0.25
    density._compute_covariance()
    plt.plot(xs,density(xs),color=color, **kwargs)