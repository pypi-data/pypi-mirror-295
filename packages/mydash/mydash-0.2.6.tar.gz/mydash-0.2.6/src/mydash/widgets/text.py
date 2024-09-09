from .base import BaseWidget, BaseContent


class TextWidget(BaseWidget):
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
        super().__init__(
            name=name,
            title=title,
            author=author,
            width=width,
            height=height,
            background=background,
            order=order,
        )
        self.type = "text"
        self.content = TextContent()

    def align(self, x: str, y: str = "center"):
        """left, right, center"""
        self.content.halign = x
        self.content.valign = y

    def clear_text(self):
        self.content.text.clear()

    def append_text(
        self,
        text: str,
        *,
        background: str = "#00ffffff",
        bold: bool = False,
        color: str = "#000000",
        italic: bool = False,
        size: int = 15,
        underline: bool = False,
    ):
        self.content.append_text(
            text=text,
            background=background,
            bold=bold,
            color=color,
            italic=italic,
            size=size,
            underline=underline,
        )


class TextData(object):
    def __init__(
        self,
        text: str,
        *,
        background,
        bold,
        color,
        italic,
        size,
        underline,
    ):
        self.content = text
        self.background = background
        self.bold = bold
        self.color = color
        self.italic = italic
        self.size = size
        self.underline = underline


class TextContent(BaseContent):
    def __init__(self):
        self.type = "text"
        self.halign = "center"
        self.text: list[TextData] = []
        self.valign = "center"

    def append_text(
        self,
        text: str,
        *,
        background: str = "#00ffffff",
        bold: bool = False,
        color: str = "#000000",
        italic: bool = False,
        size: int = 15,
        underline: bool = False,
    ):
        self.text.append(
            TextData(
                text=text,
                background=background,
                bold=bold,
                color=color,
                italic=italic,
                size=size,
                underline=underline,
            )
        )
