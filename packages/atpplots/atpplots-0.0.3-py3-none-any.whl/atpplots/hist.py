import holoviews as hv
import numpy as np

from .axis import Axis
from .figure import Figure


class Histogram(Figure):
    def __init__(
        self,
        counts: list | np.ndarray | None = None,
        bin_edges: list | np.ndarray | None = None,
        title: str | None = None,
        axis_x: str | Axis | dict = "X",
        axis_y: str | Axis | dict = "Y",
        width: int | None = None,
        height: int | None = None,
        color: str = "blue",
    ):
        # inheritances
        Figure.__init__(
            self,
            title=title,
            width=width,
            height=height,
        )

        self.hist: list | np.ndarray | None = counts
        self.bin_edges: list | np.ndarray | None = bin_edges
        self.axis_x = Axis.init(axis_x)
        self.axis_y = Axis.init(axis_y)
        self.color: str = color

        return None

    def to_holoviews(self) -> hv.Histogram:
        ret = hv.Histogram(
            (self.hist, self.bin_edges),
            kdims=[self.axis_x.hv_dimension],
            vdims=[self.axis_y.hv_dimension],
        ).opts(
            width=self.width,
            height=self.height,
            title=self.title,
            color=self.color,
        )

        return ret
