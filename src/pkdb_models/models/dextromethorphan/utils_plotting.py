"""Colors and style of the figures of the dextromethorphan manuscript.

The colormap of the CYP2D6 activity scores is used by the scans of
dextromethorphan and chlorzoxazone. `MPL_STYLE` is the matplotlib style of the
figures which are drawn with matplotlib directly (`figures_mpl`); it is applied
per figure with `matplotlib.rc_context` and never to the global settings, which
would restyle every figure drawn afterwards.
"""

from typing import Any

import matplotlib as mpl
import seaborn as sns
from matplotlib.figure import Figure
from matplotlib.typing import RcKeyType

UNKNOWN_COLOR = (0.66275, 0.66275, 0.66275, 0.7)
CMAP = sns.color_palette("Spectral", as_cmap=True)
CBAR_MAX = 3

#: matplotlib style of the `figures_mpl`, applied with `matplotlib.rc_context`
MPL_STYLE: dict[RcKeyType, Any] = {
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.labelsize": "15",
    "axes.labelweight": "bold",
    "axes.titlesize": "medium",
    "axes.titleweight": "bold",
    "legend.fontsize": "20",
    "xtick.labelsize": "20",
    "ytick.labelsize": "20",
    "figure.facecolor": "1.00",
}


def keep_tick_label_sizes(figure: Figure) -> None:
    """Keep the tick label sizes of the current style in a figure.

    matplotlib takes the size of the tick labels from the global settings when
    it places the ticks, i.e. when the figure is drawn, which is outside the
    `rc_context` of `MPL_STYLE`: the figure would get the ticks of the default
    labels. Setting the sizes on the axes, inside the context, keeps them.

    Args:
        figure: the figure, created inside `matplotlib.rc_context(MPL_STYLE)`.
    """
    for ax in figure.axes:
        ax.tick_params(
            axis="x", which="both", labelsize=mpl.rcParams["xtick.labelsize"]
        )
        ax.tick_params(
            axis="y", which="both", labelsize=mpl.rcParams["ytick.labelsize"]
        )
