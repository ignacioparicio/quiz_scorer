"""Implements plotting helper functions."""

from typing import List, Dict
import logging
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import seaborn as sns

logger = logging.getLogger(__name__)

# pylint:disable=too-many-arguments
# pylint:disable=invalid-name
def generate_plot(
    names: List[str],
    scores: List[float],
    output_dir: str,
    title: str = "Game scores",
    bands: Dict = None,
    x_offset: float = 0.1,
    dpi: int = 150,
    palette: str = "Blues",
):
    """
    Creates and saves a scores bar plot.

    Args:
        names: labels for the categories in the x-axis.
        scores: bar height.
        output_dir: path to save.
        title: name of the chart.
        bands: labels and ranges for horizontal colored bands.
        x_offset: separation between chart and band labels.
        dpi: output resolution.
        palette: color palette to be used.

    Returns:
        Nothing, but saves the generated scores bar plot.
    """
    _, ax = plt.subplots(1, 1, figsize=(10, 6), dpi=dpi)
    sns.barplot(
        x=names, y=scores, palette=_get_palette_from_values(palette, scores), ax=ax
    )
    if bands:
        _add_labeled_bands(bands, ax, x_offset)
    _format_output(ax, title)
    save_path = f"{output_dir}/{title.replace(' ', '_')}.png"
    plt.savefig(save_path, bbox_inches="tight")
    logger.info("%s plot saved to %s", title, save_path)


def _add_labeled_bands(bands: Dict, ax: matplotlib.axes, x_offset: float):
    """
    Adds horizontal colored bars and associated labels for different ranges of scores.
    Args:
        bands: mapping from band name to y-range and color.
        ax: axes where to add the bars.
        x_offset: separation between chart and band labels.

    Returns:
        Nothing, modifies ax in place.
    """
    x_max = ax.get_xlim()[1]
    for label, label_params in bands.items():
        y_min, y_max = label_params["range"]
        # Add label on the right of the chart
        ax.annotate(
            label,
            (x_max + x_offset, (y_min + y_max) / 2),
            annotation_clip=False,
            color=label_params["color"],
            style="italic",
        )
        # Create colored bar for the given y-range
        ax.fill_between(
            np.arange(-0.5, x_max + 0.5),
            y_min,
            y_max,
            color=label_params["color"],
            alpha=0.1,
        )


def _format_output(ax: matplotlib.axes, title: str):
    """PFormats matplotlib output figure."""
    _add_value_labels(ax)
    ax.set_title(title)
    ax.grid(False)
    plt.margins(0, 0)
    sns.set_style("ticks", {"xtick.major.size": 1})


def _get_palette_from_values(template_palette: str, values: List[str]):
    """Transforms a given palette to map to the values passed."""
    normalized = (np.array(values) - min(values)) / (max(values) - min(values))
    indices = np.round(normalized * (len(values) - 1)).astype(np.int32)
    palette = sns.color_palette(template_palette, len(values))
    try:
        values_palette = np.array(palette).take(indices, axis=0)
    except IndexError:
        logger.warning(
            "All values are the same, couldn't create values based template."
        )
        values_palette = template_palette
    return values_palette


def _add_value_labels(ax: matplotlib.axes):
    """Adds labels with numeric value on top of each vertical bar."""
    for patch in ax.patches:
        ax.annotate(
            "{:.0f}".format(patch.get_height()),
            (patch.get_x() + patch.get_width() / 2, patch.get_height() + 0.1),
            ha="center",
            va="bottom",
            color="black",
        )
