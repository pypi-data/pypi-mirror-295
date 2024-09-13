from pathlib import Path

from icplot.color import ColorMap

from .plot import Plot


class Plotter:

    def __init__(self, cmap: ColorMap):
        self.cmap = cmap

    def apply_cmap_colors(self, plot: Plot):
        skipped_color = 0
        for idx, series in enumerate(plot.series):
            if not series.color:
                series.color = self.cmap.get_color(idx - skipped_color, plot.series)
            else:
                skipped_color += 1

    def plot(self, plot: Plot, path: Path | None = None):
        pass
