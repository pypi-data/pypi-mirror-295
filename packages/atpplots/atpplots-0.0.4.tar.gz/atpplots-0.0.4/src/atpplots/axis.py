from __future__ import annotations

import holoviews as hv


class Axis:
    def __init__(
        self,
        title: str,
        id: str = "",
        unit: str | None = None,
        shared: bool = False,
    ):
        self.id = id
        self.title = title
        self.unit = unit
        self.shared = shared
        # self.range
        return None

    @property
    def label(self) -> str:
        if self.unit is None:
            return self.title

        return f"{self.title} [{self.unit}]"

    @property
    def hv_dimension(self) -> hv.Dimension:
        return hv.Dimension(self.id, label=self.label)

    @classmethod
    def init(cls, input: str | dict | Axis) -> Axis:
        if isinstance(input, Axis):
            return input
        elif isinstance(input, str):
            return Axis(id=input, title=input)
        elif isinstance(input, dict):
            return Axis(**input)
        else:
            raise ValueError(f"Invalid axis type: {type(input)}")
