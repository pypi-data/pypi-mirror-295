"""
This file is part of Lynq (elemenom/lynq).

Lynq is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Lynq is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Lynq. If not, see <https://www.gnu.org/licenses/>.
"""

from typing import Any, Callable
from lynq.backendutils.errors.handler import handle

from lynq.backendutils.app.appobject import AppObject
from lynq.backendutils.app.app import WebApp
from lynq.backendutils.app.supportswith import SupportsWithKeyword

class StandardAppExportObject(SupportsWithKeyword):
    def __init__(self, app_: WebApp, object_: Any = AppObject, *args: Any, **kwargs: Any) -> None:
        self.app: WebApp = app_
        self.object: type[object_] = object_
        self.args: tuple[Any, ...] = args
        self.kwargs: dict[str, Any] = kwargs
        self.postb: Any = None

    def open(self) -> Any:
        app_object: Any = self.object(self.app.fn.__name__, self.app)
        app_object.exit()

        try: return self.app.fn(app_object, *self.args, **self.kwargs)
        finally: app_object.pass_to_server()

    @handle
    def init_postbuilding(self, type_: Callable) -> None:
        self.postb = type_(self.app.fn.__name__, self.app.server)

    @handle
    def get_object_type(self) -> Any:
        return self.object

    @handle
    def get_app(self) -> WebApp:
        return self.app