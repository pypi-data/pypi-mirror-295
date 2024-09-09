from .base import BaseWidget, BaseContent


class CustomWidget(BaseWidget):
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
            name,
            title,
            author,
            width,
            height,
            background,
            order,
        )
        self.type = "custom"
        self.content = CustomContent()

    def set_config(self, align: str = "center", cross: str = "center", dir: str = "col"):
        self.content.align = align
        self.content.cross = cross
        self.content.dir = dir

    def add_content(self, content: BaseContent):
        self.content.add_content(content)

class CustomContent(BaseContent):
    def __init__(self):
        self.type = "custom"
        self.align = "center"
        self.cross = "center"
        self.dir = "col"
        self.data: list[BaseContent] = []

    def set_config(self, align: str = "center", cross: str = "center", dir: str = "col"):
        self.align = align
        self.cross = cross
        self.dir = dir

    def add_content(self, content: BaseContent):
        self.data.append(content)

