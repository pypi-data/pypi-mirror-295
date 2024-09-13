import numpy as np


class DataVector:
    def __init__(
        self,
        data_x: list | np.ndarray | None = None,
        data_y: list | np.ndarray | None = None,
        color: str = "blue",
        label: str = "",
        interpolation: str = "linear",
    ):
        if interpolation not in ["linear", "ffill", "bfill"]:
            raise ValueError(
                f"Interpolation method '{interpolation}' is not supported."
            )
        self.data_x: list | np.ndarray | None = data_x
        self.data_y: list | np.ndarray | None = data_y

        self.color: str = color
        self.label: str = label
        self.interpolation: str = interpolation

        return None
