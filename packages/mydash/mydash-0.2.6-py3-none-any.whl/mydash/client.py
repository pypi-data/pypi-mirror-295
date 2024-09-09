from enum import Enum
from typing import Callable
import atexit
import requests
import signal
import sys
import threading
from pytz import timezone
import time
import schedule
import json
from .widgets import (
    BarGraphWidget,
    TextWidget,
    BaseWidget,
    ImageWidget,
    CustomWidget,

    BarGraphContent,
    TextContent,
    ImageContent,
    CustomContent,
)


class WidgetType(Enum):
    TEXT = 1
    IMAGE = 2
    BAR_GRAPH = 3
    LINE_GRAPH = 4
    CUSTOM = 0


class Client:
    def __init__(
        self, *, id: str, password: str, endpoint: str = "https://dashboard-api.llms.kr"
    ):
        self.session = requests.session()
        self.endpoint = endpoint
        result = requests.post(
            f"{endpoint}/api/collections/users/auth-with-password",
            json={
                "identity": id,
                "password": password,
            },
        )
        self.widgets: dict[str, BaseWidget] = {}
        self.builders: dict[str, Callable[[BaseWidget], BaseWidget]] = {}
        response = result.json()
        if "token" not in response:
            raise Exception("Login failed. Check your identiy and password.")
        self.token = response["token"]
        self.uid = response["record"]["id"]
        self.session.headers["Authorization"] = self.token
        self.session.headers["Content-Type"] = "application/json"
        atexit.register(self.shutdown)
        print("Login success!")

    def _get_widgets_list(self, n: int = 50):
        result = self.session.get(
            f"{self.endpoint}/api/collections/widgets/records",
            params={
                "perPage": n,
                "sort": "order",
                "filter": f'author = "{self.uid}"',
            },
            headers={},
        )
        return result["items"]

    def get(self, name: str):
        result = self.session.get(
            f"{self.endpoint}/api/collections/storage/records",
            params={
                "filter": f'name = "{name}"',
            },
        )
        result = result.json()
        items = result["items"]
        if len(items) == 0:
            return None
        id = items[0]["id"]
        result = self.session.get(
            f"{self.endpoint}/api/collections/storage/records/{id}",
        )
        result = result.json()
        result = result["data"]
        return result

    def set(self, name: str, data):
        result = self.session.get(
            f"{self.endpoint}/api/collections/storage/records",
            params={
                "filter": f'name = "{name}"',
            },
        )
        result = result.json()
        items = result["items"]
        if len(items) == 0:
            result = self.session.post(
                f"{self.endpoint}/api/collections/storage/records",
                json={
                    "name": name,
                    "data": json.dumps(data),
                },
            )
            if not result.ok:
                raise Exception(result.text)
            return
        id = items[0]["id"]
        result = self.session.patch(
            f"{self.endpoint}/api/collections/storage/records/{id}",
            json={
                "name": name,
                "data": json.dumps(data),
            },
        )
        if not result.ok:
            raise Exception(result.text)
        return

    def create_text_widget(self, name: str, title: str) -> TextWidget:
        widget = TextWidget(name=name, title=title, author=self.uid)
        return widget

    def create_bar_graph_widget(self, name: str, title: str) -> BarGraphWidget:
        widget = BarGraphWidget(name=name, title=title, author=self.uid)
        return widget

    def create_image_widget(self, name: str, title: str) -> ImageWidget:
        widget = ImageWidget(name=name, title=title, author=self.uid)
        return widget
    
    def create_layout_widget(self, name: str, title: str) -> CustomWidget:
        widget = CustomWidget(name=name, title=title, author=self.uid)
        return widget

    def add_text_content(self):
        content = TextContent()
        return content
    
    def add_bar_graph_content(self):
        content = BarGraphContent()
        return content
    
    def add_image_content(self):
        content = ImageContent()
        return content
    
    def add_custom_content(self):
        content = CustomContent()
        return content

    def push_widget(self, widget: BaseWidget):
        exists = self.session.get(
            f"{self.endpoint}/api/collections/widgets/records",
            params={
                "filter": f'name = "{widget.name}"',
            },
        )
        if not exists.ok:
            raise Exception(exists.text)
        data = exists.json()
        if data["totalItems"] >= 1:
            id = data["items"][0]["id"]
            result = self.session.patch(
                f"{self.endpoint}/api/collections/widgets/records/{id}",
                data=widget.toJSON(),
            )
            if not result.ok:
                raise Exception(result.text)
        else:
            result = self.session.post(
                f"{self.endpoint}/api/collections/widgets/records", data=widget.toJSON()
            )
            if not result.ok:
                raise Exception(result.text)()

    def remove_widget(self, name: str):
        # self.widgets.pop(name, None)
        exists = self.session.get(
            f"{self.endpoint}/api/collections/widgets/records",
            params={
                "filter": f'name = "{name}"',
            },
        )
        if not exists.ok:
            raise Exception(exists.text)
        data = exists.json()
        if data["totalItems"] >= 1:
            id = data["items"][0]["id"]
            result = self.session.delete(
                f"{self.endpoint}/api/collections/widgets/records/{id}"
            )
            if not result.ok:
                raise Exception(result.text)

    def shutdown(self):
        for k in self.widgets.keys():
            self.remove_widget(k)
        self.widgets.clear()

    def widget(
        self,
        type: WidgetType,
        name: str,
        title: str,
        interval: int = 1,
        every: str = "minute",
        at: str = ":00",
    ):
        if type == WidgetType.TEXT:
            widget = self.create_text_widget(name=name, title=title)
        elif type == WidgetType.BAR_GRAPH:
            widget = self.create_bar_graph_widget(name, title)
        elif type == WidgetType.IMAGE:
            widget = self.create_image_widget(name, title)
        elif type == WidgetType.CUSTOM:
            widget = self.create_layout_widget(name, title)
        else:
            widget = BaseWidget(name, title, self.uid, 1, 1, "#e3e3e3", 10)

        def decorator(f):
            # @wraps(f)
            # def wrapper(*args, **kwargs):
            #     print(f)
            result = f(widget)
            self.push_widget(result)
            self.widgets[name] = result
            job = schedule.every(interval)
            tz = timezone("Asia/Seoul")
            if interval > 1:
                if every == "seconds":
                    job = job.seconds
                elif every == "minutes":
                    job = job.minutes
                elif every == "hours":
                    job = job.hours
                else:
                    print(f"Error({name}): interval > 1: seconds, minutes, hours")
                    return
            elif interval == 1:
                if every == "second":
                    job = job.second
                elif every == "minute":
                    job = job.minute.at(at, tz)
                elif every == "hour":
                    job = job.hour.at(at, tz)
                elif every == "day":
                    job = job.day.at(at, tz)
                else:
                    print(f"Error({name}): interval == 1: second, minute, hour, day")
                    return
            job.do(self._run_threaded, self._execute, f, name).tag(name)
            # return result
            # return wrapper
        return decorator

    def _execute(self, f, name):
        if name not in self.widgets:
            schedule.clear(name)
            return
        result = f(self.widgets[name])
        self.push_widget(result)
        self.widgets[name] = result

    def _run_threaded(self, job_func, func, name):
        job_thread = threading.Thread(target=job_func, args=(func, name))
        job_thread.start()

    def run(self):
        while True:
            schedule.run_pending()
            time.sleep(1)


signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))
