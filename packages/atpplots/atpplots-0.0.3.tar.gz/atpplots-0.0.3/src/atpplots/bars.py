import holoviews as hv
import numpy as np

from .axis import Axis
from .figure import Figure


class Bars(Figure):
    def __init__(
        self,
        counts: list | np.ndarray,
        ticks: list[str],
        title: str | None = None,
        axis_x: str | Axis | dict = "X",
        axis_y: str | Axis | dict = "Y",
        width: int | None = None,
        height: int | None = None,
        color: str | list[str] = "blue",
        labels: list[str] | None = None,
    ):
        # inheritances
        Figure.__init__(
            self,
            title=title,
            width=width,
            height=height,
        )

        self.counts: list | np.ndarray = counts
        self.ticks: list[str] = ticks
        self.labels: list[str] | None = labels

        self.axis_x = Axis.init(axis_x)
        self.axis_y = Axis.init(axis_y)
        self.color: str | list[str] = color

        return None

    def to_holoviews(self) -> hv.Overlay:
        bars = []
        for i in range(len(self.counts)):
            bars.append(
                hv.Bars(
                    [(self.ticks[i], self.counts[i])],
                    self.axis_x.hv_dimension,
                    vdims=[self.axis_y.hv_dimension],
                    label=self.labels[i] if self.labels is not None else None,
                ).opts(
                    color=self.color[i] if self.color is not None else None,
                )
            )

        return hv.Overlay(bars).opts(
            width=self.width,
            height=self.height,
            title=self.title,
        )
