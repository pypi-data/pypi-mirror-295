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

from typing import Optional
from lynq.backendutils.errors.handler import handle

from lynq.backendutils.app.appobject import AppObject
from lynq.backendutils.app.app import WebApp

class TagObject(AppObject):
    @handle
    def __init__(self, name: str, tag: str, app: WebApp, args: Optional[WebApp] = None) -> None:
        super().__init__(name, app)
        self.tagstr: str = tag
        self.singular(f"<{self.tagstr} {args or ''}>")

    @handle
    def on_run(self) -> None:
        ...

    @handle
    def __exit__(self, *_) -> None:
        self.singular(f"</{self.tagstr}>")