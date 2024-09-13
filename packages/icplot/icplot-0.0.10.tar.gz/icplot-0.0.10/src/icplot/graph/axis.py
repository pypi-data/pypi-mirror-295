"""
This module has a plot's axis
"""

from iccore.serialization import Serializable


class Range(Serializable):
    """
    This is a sequence of numbers specified by lower and upper
    bounds and a step size. Eg (1, 5, 1) gives: [1, 2, 3, 4]
    """

    def __init__(self, lower, upper, step):
        self.lower = lower
        self.upper = upper
        self.step = step

    def eval(self) -> list:
        return list(range(self.lower, self.upper, self.step))

    def serialize(self):
        return {"lower": self.lower, "upper": self.upper, "step": self.step}


class PlotAxis(Serializable):
    """
    This is a plot's axis
    """

    def __init__(self, label: str = ""):
        self.label = label
        self.ticks: Range | None = None

    def set_ticks(self, lower: int, upper: int, step: int):
        self.ticks = Range(lower, upper + 1, step)

    def serialize(self):
        return {"label": self.label, "ticks": self.ticks.serialize()}

    def get_resolved_ticks(self) -> list:
        if self.ticks:
            return self.ticks.eval()
        return []
