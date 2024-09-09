from .base import BaseWidget, BaseContent

class BarGraphWidget(BaseWidget):
    def __init__(
        self,
        name: str,
        title: str,
        author: str,
        *,
        width: int = 1,
        height: int = 1,
        background: str = "#e3e3e3",
        order: int = 10,
    ):
        super().__init__(name, title, author, width, height, background, order)
        self.type = "bar"
        self.content = BarGraphContent()

    def add_data(
        self,
        x: int,
        y: float,
        width: float = 10,
        background: str = "#00ffffff",
        foreground: str = "#000000",
    ):
        self.content.add_data(x, y, width, background, foreground)

    def align(self, align: str = "around"):
        """around, space, left, right, center"""
        self.content.align(align)

    def set_label(self, pos: int, text: str, color: str = "#000000"):
        self.content.set_label(pos, text, color)
    
    def label_visibility(self, visible: bool = True):
        self.content.label_visibility(visible)


class BarGraphContent(BaseContent):
    def __init__(self):
        self.type = "bar"
        self.alignment = "around"
        self.data: list[BarGraphData] = []
        self.description = ""
        self.foreground = "#85a7fd"
        self.showYLabel = True
        self.xlabels: list[BarGraphXLabel] = []

    def add_data(
        self,
        x: int,
        y: float,
        width: float = 10,
        background: str = "#00ffffff",
        foreground: str = "#000000",
    ):
        self.data.append(
            BarGraphData(
                x=x,
                y=y,
                width=width,
                background=background,
                foreground=foreground,
            )
        )

    def align(self, align: str = "around"):
        """around, space, left, right, center"""
        self.alignment = align

    def set_label(self, pos: int, text: str, color: str = "#000000"):
        self.xlabels.append(
            BarGraphXLabel(
                color=color,
                pos=pos,
                text=text,
            )
        )
    
    def label_visibility(self, visible: bool = True):
        self.showYLabel = visible


class BarGraphXLabel(object):
    def __init__(self, color: str, pos: int, text: str):
        self.color = color
        self.pos = pos
        self.text = text


class BarGraphData(object):
    def __init__(
        self,
        x: int,
        y: float,
        width: float,
        background: str,
        foreground: str,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.background = background
        self.foreground = foreground
