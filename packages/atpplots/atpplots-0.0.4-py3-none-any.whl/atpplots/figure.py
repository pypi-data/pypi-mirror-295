class Figure:
    def __init__(
        self,
        title: str | None = None,
        width: int | None = None,
        height: int | None = None,
    ):
        if title is None:
            title = ""
        if width is None:
            width = 1000
        if height is None:
            height = 600

        self.title: str = title
        self.width: int = width
        self.height: int = height
        return None
