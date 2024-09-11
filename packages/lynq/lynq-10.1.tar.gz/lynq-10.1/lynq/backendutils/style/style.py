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
from lynq.backendutils.style.attribute import StyleAttribute
from lynq.backendutils.errors.handler import handle

class StyledAppAttachment:
    @handle
    def __init__(self, path: Optional[str] = None) -> None:
        self.path: str | None = path
        self.write_later: str = ""
        self.attributes: list[StyleAttribute] = []

    @handle
    def close(self, path: Optional[str] = None) -> None:
        self.path = path or self.path

        for attribute in self.attributes:
            self._write_attrib_contents(attribute)

        self._init_file(path, self.write_later)

    @handle
    def _init_file(self, path: Optional[str] = None, write: Optional[str] = None) -> None:
        with open((self.path or (path or "index.css")), "w") as file:
            file.write(write or "")

    @handle
    def add_attribute(self, key: Optional[str] = None) -> StyleAttribute:
        key = key or "BASE"
        key = "html" if key.lower() == "base" else key

        attribute: StyleAttribute = StyleAttribute(self, key or "html")
        self.attributes.append(attribute)

        return attribute

    @handle
    def _write_attrib_contents(self, attribute: StyleAttribute) -> None:
        self.write_later += f"{attribute.get_written()}\n"

    @handle
    def set_path(self, path: str) -> None:
        self.path = path