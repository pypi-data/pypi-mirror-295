import itertools
from typing import Optional, Union, List, Iterator

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.axis import Axis
from matplotlib.colors import Colormap
from matplotlib.figure import Figure
from matplotlib.ticker import AutoMinorLocator, MaxNLocator, LogLocator, FuncFormatter, FormatStrFormatter

# re-import full modules for easier access
from . import const
from . import file
from . import style

# apply default rcParams right after loading
style.set_style()

output_mode = "auto"
"""
"file"        : only produce files
"interactive" : show all plots, including those with filename, produce no files
"both"        : produce files if requested, show all
"auto"        : save if file name given, show if not
"""

output_location = file.get_invoker_dir()
"""
base for relative file paths on output
"""

sizes = {
    "regular": (150 * const.GOLDEN_RATIO, 150),
    "wide": (300, 150)
}
"""
some template sizes for use with new_*, given in millimeters
"""


def default_dpi(save=False):
    if save and mpl.rcParams["savefig.dpi"] != "figure":
        return mpl.rcParams["savefig.dpi"]
    return mpl.rcParams["figure.dpi"]


def new_mm(*args, figsize, **kwargs):
    """Wrapper for plt.subplots, using figsize in millimeters

    :rtype: figure, axes
    """
    return plt.subplots(*args, figsize=(figsize[0] / 25.4, figsize[1] / 25.4), **kwargs)


def new_regular(*args, **kwargs):
    """Create a figure in a commonly used format

    :rtype: figure, axes
    """
    return new_mm(*args, figsize=sizes["regular"], **kwargs)


def new_wide(*args, **kwargs):
    """Create a wide figure, useful for timeseries

    :rtype: figure, axes
    """
    return new_mm(*args, figsize=sizes["wide"], **kwargs)


def set_axis_format(ax: Axis, format: str, use_locale=False):
    if use_locale:
        import locale
        fmt = FuncFormatter(lambda x, pos: locale.format_string(format, x))
    else:
        fmt = FormatStrFormatter(format)
    ax.set_major_formatter(fmt)


def set_ticks(axs: Axes, *, major: Optional[str] = None, minor: Optional[str] = None, maxn: Optional[int] = None,
              multiple: Optional[float] = None):
    """Configure axis ticks

    :param Axes axs: Axes object to manipulate
    :param str major: (optional) string containing xy
    :param str minor: (optional) string containing xy.
        Only modifies axis indicated by the parameter.
        If none of `major` and `minor` are given, assume major="",minor="xy"

    The first parameter present is executed, if none match, an AutoLocator is applied:

    :param int maxn: setup a MaxNLocator
    :param float multiple: setup a MultipleLocator
    """

    if major is None and minor is None:
        minor = "xy"
    if major is None:
        major = ""
    if minor is None:
        minor = ""

    def do_setting(ax, kind):
        setfn = getattr(ax, f"set_{kind}_locator")
        if maxn is not None:
            setfn(plt.MaxNLocator(maxn))
        elif multiple is not None:
            setfn(plt.MultipleLocator(multiple))
        else:
            setfn(plt.AutoLocator() if kind == "major" else AutoMinorLocator())

    "x" in major and do_setting(axs.xaxis, "major")
    "x" in minor and do_setting(axs.xaxis, "minor")
    "y" in major and do_setting(axs.yaxis, "major")
    "y" in minor and do_setting(axs.yaxis, "minor")


def set_same_ticks(axs: Axes):
    """Change locator so that both axis use the same interval, while keeping current autorange

    :param Axes axs: Axes object to manipulate
    """
    xvals = axs.get_xaxis().get_major_locator()()
    yvals = axs.get_yaxis().get_major_locator()()
    spacing = max(xvals[1] - xvals[0], yvals[1] - yvals[0])
    from matplotlib.ticker import MultipleLocator
    axs.get_xaxis().set_major_locator(MultipleLocator(spacing))
    axs.get_yaxis().set_major_locator(MultipleLocator(spacing))


def set_axis_colors(axs: Axes, color):
    side = axs.yaxis.get_label_position() or "left"
    axs.spines[side].set_color(color)
    axs.yaxis.label.set_color(color)
    axs.tick_params(axis="y", colors=color)


def twinx(axs: Axes, offset: Optional[float] = None) -> Axes:
    twin = axs.twinx()
    for spine in axs.spines.keys():
        twin.spines[spine].set_edgecolor(axs.spines[spine].get_edgecolor())
    if offset is not None:
        side = twin.yaxis.get_label_position() or "left"
        twin.spines[side].set_position(("outward", offset))
    return twin


def set_grid(axs: Axes):
    """Apply default grid settings to Axes

    :param Axes axs: Axes object to manipulate
    """
    axs.grid(which="major", linestyle="-")
    axs.grid(which="minor", linestyle=":", linewidth=mpl.rcParams["grid.linewidth"] * 0.5,
             alpha=mpl.rcParams["grid.alpha"] * 0.8)


def get_object_facecolor(obj):
    if isinstance(obj, list):
        return get_object_facecolor(obj[-1])
    if isinstance(obj, mpl.lines.Line2D):
        return obj.get_color()
    if isinstance(obj, mpl.collections.Collection):
        return obj.get_facecolor()[0]
    return None


def _is_jupyter():
    # https://stackoverflow.com/q/15411967
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter


def finalize(fig: Figure, filename: Optional[str] = None):
    """Show and/or save the figure, and close(dispose) it afterwards.

    :param Figure fig: Figure object to manipulate
    :param str filename: (optional) file name to save to
    :return: absolute file name, or None if none was produced
    :rtype: str
    """
    if output_mode == "both":
        raise NotImplementedError(f"Unsupported due to errors with tight_layout")
    do_save = filename and (output_mode == "auto" or output_mode == "file")
    do_show = output_mode == "interactive" or (output_mode == "auto" and not filename)
    if do_show:
        if _is_jupyter():
            from IPython.display import display
            display(fig)
        else:
            fig.show()
    if do_save:
        filename = file.expand_relative(filename, output_location)
        fig.savefig(filename)
    if do_show or do_save:
        plt.close(fig)
    return filename


def get_cmap_cycle(cmap: Union[Colormap, str], k: Optional[int] = None) -> Union[Iterator, List]:
    """Return a cycler for colormaps.

    If *k=None*, return the iterator, otherwise return a list of *k* elements.

    :param (Colormap, str) cmap: colormap instance or cmap identifier
    :param int k: (optional) number of items to return
    :return:
    """
    if isinstance(cmap, str):
        cmap = plt.get_cmap(cmap)
    cycler = itertools.cycle(cmap.colors)
    if k is not None:
        return list(itertools.islice(cycler, k))
    return cycler


def contour_levels(N: int, vmin: Optional[float] = None, vmax: Optional[float] = None,
                   locator: Optional[MaxNLocator] = None, logscale=False, return_dict=True, **kwargs):
    """Return levels (as argument dict) for Axes.contourf using vmin/vmax

    :param int N: number of color steps to create
    :param float vmin: lowest value (inclusive)
    :param float vmax: highest value (inclusive)
    :param Locator locator: (optional) Locator to use
    :param bool logscale: (optional) use logarithmic scale
    :param bool return_dict: (optional) return as argument dict for `contourf`
    :return:
    """
    if vmin is not None and vmax is not None:
        if locator is None:
            if logscale:
                locator = LogLocator()
            else:
                locator = MaxNLocator(N + 1, min_n_ticks=1)
        lev = locator.tick_values(vmin, vmax)
        kwargs["vmin"] = vmin
        kwargs["vmax"] = vmax
        kwargs["locator"] = locator
        kwargs["levels"] = lev
    else:
        kwargs["levels"] = N
    if return_dict:
        return kwargs
    else:
        return kwargs["levels"]
