import holoviews as hv
import numpy as np

from .axis import Axis
from .figure import Figure

hv.extension("bokeh")


class Scatter(Figure):
    def __init__(
        self,
        data_x: list | np.ndarray | None = None,
        data_y: list | np.ndarray | None = None,
        title: str | None = None,
        axis_x: str | Axis | dict = "X",
        axis_y: str | Axis | dict = "Y",
        width: int | None = None,
        height: int | None = None,
        color: str = "blue",
        label: str = "",
    ):
        # inheritances
        Figure.__init__(
            self,
            title=title,
            width=width,
            height=height,
        )

        self.data_x: list | np.ndarray | None = data_x
        self.data_y: list | np.ndarray | None = data_y
        self.axis_x = Axis.init(axis_x)
        self.axis_y = Axis.init(axis_y)
        self.color: str = color
        self.label: str = label

        return None

    def to_holoviews(self) -> hv.Scatter:
        ret = hv.Scatter(
            (self.data_x, self.data_y),
            kdims=[self.axis_x.hv_dimension],
            vdims=[self.axis_y.hv_dimension],
            label=self.label,
        ).opts(
            width=self.width,
            height=self.height,
            title=self.title,
            color=self.color,
            shared_axes=False,
        )

        return ret
