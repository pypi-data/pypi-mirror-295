"""
This module has content for generating plots
"""

import random

from iccore.serialization import Serializable

from .axis import PlotAxis
from .series import PlotSeries


class Plot(Serializable):
    """
    A generic plot with optional axis ticks
    """

    def __init__(
        self,
        title: str = "",
        x_label: str = "",
        y_label: str = "",
        legend_label: str = "",
    ) -> None:
        self.series: list[PlotSeries] = []
        self.title = title
        self.size: tuple | None = None
        self.plot_type = ""
        self.x_axis = PlotAxis(x_label)
        self.y_axis = PlotAxis(y_label)
        self.legend_label = legend_label

    def set_x_ticks(self, lower, upper, step):
        self.x_axis.set_ticks(lower, upper, step)

    def set_y_ticks(self, lower, upper, step):
        self.y_axis.set_ticks(lower, upper, step)

    def add_series(self, series):
        self.series.append(series)

    def serialize(self):
        return {
            "series": [s.serialize() for s in self.series],
            "title": self.title,
            "type": self.plot_type,
            "x_axis": self.x_axis.serialize(),
            "y_axis": self.y_axis.serialize(),
            "legend_label": self.legend_label,
        }


class GridPlot(Plot):
    """
    Make a grid of plots
    """

    def __init__(
        self, data, title: str = "", stride: int = 4, size: tuple = (25, 20)
    ) -> None:
        super().__init__(title)
        self.data = data
        self.stride = stride
        self.size = size

    def get_series_indices(self, num_samples: int = 0):
        rows = num_samples // self.stride
        cols = num_samples // rows
        len_data = len(self.data)

        if num_samples == 0:
            indices = list(range(0, len_data))
        else:
            indices = [random.randint(0, len_data - 1) for _ in range(num_samples)]
        return rows, cols, indices

    def get_subplots(self, num_samples: int = 0):
        rows, cols, indices = self.get_series_indices(num_samples)

        subplots = []
        count = 1
        for index in indices:
            if num_samples > 0 and count == num_samples + 1:
                break
            if isinstance(self.data[index], list):
                for series in self.data[index]:
                    subplots.append(series)
                    count += 1
            else:
                subplots.append(self.data[index])
                count += 1
        return rows, cols, subplots
