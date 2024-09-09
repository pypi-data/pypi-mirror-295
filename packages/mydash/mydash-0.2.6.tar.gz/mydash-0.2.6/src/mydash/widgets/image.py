from .base import BaseWidget, BaseContent
import base64

class ImageWidget(BaseWidget):
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
        self.type = "image"
        self.content = ImageContent()

    def set_image(self, data: bytes, fit: str = "cover"):
        self.content.set_image(data, fit)


class ImageContent(BaseContent):
    def __init__(self):
        self.type = "image"
        self.data = ""
        self.fit = "cover"

    def set_image(self, data: bytes, fit: str = "cover"):
        """contain, cover, fill"""
        self.data = base64.b64encode(data).decode()
        self.fit = fit