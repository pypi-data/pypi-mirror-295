from pathlib import Path
import logging
from typing import cast

logging.getLogger("matplotlib").setLevel(logging.WARNING)
import matplotlib as mpl  # NOQA

default_backend = mpl.get_backend()
mpl.use("Agg")
import matplotlib.pyplot as plt  # NOQA

from icplot.color import ColorMap  # NOQA
from .series import PlotSeries, LinePlotSeries, ScatterPlotSeries, ImageSeries  # NOQA
from .plot import Plot, GridPlot  # NOQA
from .plotter import Plotter  # NOQA


class MatplotlibColorMap(ColorMap):
    """
    A matplotlib based colormap
    """

    def __init__(self, label: str):
        super().__init__(label, mpl.colormaps[label])


class MatplotlibPlotter(Plotter):
    """
    A plot backend for matplotlib
    """

    def __init__(self, cmap_label="viridis"):
        super().__init__(MatplotlibColorMap(cmap_label))

    def set_decorations(self, ax, plot: Plot):
        ax.legend(loc="upper left")
        if plot.x_axis.label:
            ax.set_xlabel(plot.x_axis.label)
        if plot.y_axis.label:
            ax.set_ylabel(plot.y_axis.label)
        if plot.x_axis.ticks:
            ax.set_xticks(plot.x_axis.get_resolved_ticks())
        if plot.y_axis.ticks:
            ax.set_yticks(plot.y_axis.get_resolved_ticks())
        if plot.title:
            ax.set_title(plot.title)

    def plot_line(self, ax, series: LinePlotSeries):
        ax.plot(
            series.x,
            series.y,
            label=series.label,
            color=series.get_color().as_list(),
            marker=series.marker,
        )

    def plot_scatter(self, ax, series: ScatterPlotSeries):
        ax.scatter(series.data, label=series.label, color=series.get_color().as_list())

    def plot_image(self, ax, series: ImageSeries):
        ax.imshow(series.data)
        ax.axis("off")

    def plot_series(self, ax, series: PlotSeries):
        if series.series_type == "line":
            self.plot_line(ax, cast(LinePlotSeries, series))
        elif series.series_type == "scatter":
            self.plot_scatter(ax, cast(ScatterPlotSeries, series))
        elif series.series_type == "image":
            self.plot_image(ax, cast(ImageSeries, series))

    def plot(self, plot: Plot, path: Path | None = None):

        self.apply_cmap_colors(plot)

        fig, ax = plt.subplots()

        for series in plot.series:
            self.plot_series(ax, series)

        self.set_decorations(ax, plot)

        self.render(fig, path)

    def plot_grid(self, plot: GridPlot, path: Path | None = None, num_samples: int = 0):

        rows, cols, series = plot.get_subplots(num_samples)
        fig, axs = plt.subplots(rows, cols)

        for ax, series_item in zip(axs, series):
            self.plot_series(ax, series_item)

        self.render(fig, path)

    def render(self, fig, path: Path | None = None):
        if path:
            fig.savefig(path)
        else:
            plt.switch_backend(default_backend)
            fig.show()
            plt.switch_backend("Agg")
