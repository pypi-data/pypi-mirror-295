from iccore.serialization import Serializable

from icplot.color import Color


class PlotSeries(Serializable):
    """
    A data series in a plot, such as a single line in a line-plot
    """

    def __init__(self, label: str = "", color: Color | None = None) -> None:
        self.label = label
        self.color = color
        self.series_type = ""

    def get_color(self) -> Color:
        if self.color:
            return self.color
        return Color()

    def serialize(self):

        color_val = {}
        if self.color:
            color_val = self.color.serialize()

        return {
            "label": self.label,
            "color": color_val,
            "type": self.series_type,
        }


class ImageSeries(PlotSeries):
    """
    A plot data series where the elements are images
    """

    def __init__(
        self,
        data,
        label: str = "",
        transform=None,
    ):
        super().__init__(label)
        self.data = data
        self.series_type = "image"
        self.transform = transform

    def serialize(self):
        ret = super().serialize()
        ret["data"] = self.data
        return ret


class LinePlotSeries(PlotSeries):
    """
    A plot series for line plots
    """

    def __init__(
        self,
        x: list | None = None,
        y: list | None = None,
        label: str = "",
        color: Color | None = None,
        marker: str = "o",
    ) -> None:
        super().__init__(label, color)
        self.marker = marker
        self.series_type = "line"
        if x:
            self.x = x
        else:
            self.x = []
        if y:
            self.y = y
        else:
            self.y = []

    def add_entry(self, x_point: float, y_point: float):
        self.x.append(x_point)
        self.y.append(y_point)

    def sort(self):
        """
        Sorts by x values
        """
        tuples = list(zip(self.x, self.y))
        tuples.sort(key=lambda tup: tup[0])
        for idx, _ in enumerate(tuples):
            self.x[idx] = tuples[idx][0]
            self.y[idx] = tuples[idx][1]

    def serialize(self):
        ret = super().serialize()
        ret["x"] = self.x
        ret["y"] = self.y
        return ret


class ScatterPlotSeries(PlotSeries):
    def __init__(self, data, label: str = "", color: Color | None = None):
        super().__init__(label, color)
        self.data = data
        self.series_type = "scatter"

    def serialize(self):
        ret = super().serialize()
        ret["data"] = self.data
        return ret
