import json

class Object:
    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
        )

class BaseWidget(Object):
    def __init__(
        self,
        name: str,
        title: str,
        author: str,
        width: int,
        height: int,
        background: str,
        order: int,
    ):
        self.name = name
        self.title = title
        self.author = author
        self.w = width
        self.h = height
        self.background = background
        self.order = order

    def set_author(self, author: str):
        self.author = author

    def set_size(self, *, w: int, h: int):
        self.w = w
        self.h = h

    def set_background(self, color: str):
        self.background = color

    def set_order(self, order: int):
        self.order = order

class BaseContent(Object):
    def __init__(self):
        self.type = "base"
