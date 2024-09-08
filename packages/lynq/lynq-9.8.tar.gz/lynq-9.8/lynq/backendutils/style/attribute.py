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

from typing import Self, Any

from lynq.backendutils.app.supportswith import SupportsWithKeyword

class StyleAttribute(SupportsWithKeyword):
    def __init__(self, style: Any, tag_name: str) -> None:
        self.style: Any = style

        self.name: str = tag_name

        self.written: str = ""

        self._init_attribute()

    def _init_attribute(self) -> None:
        self._write_line(f"{self.name} " + "{")

    def _write_line(self, contents: str) -> None:
        self.written += f"{contents}\n"

    def add_singular(self, contents: str) -> Self:
        self._write_line(contents)

        return self

    def add_option(self, **kwargs) -> Self:
        for key, value in list(kwargs.items()):
            self._write_line(f"{key.replace("_", "-")}: {value};")

        return self

    def __exit__(self, *_) -> None:
        self.close()

    def back(self) -> Self:
        self._write_line("}")

        return self.style

    def get_written(self) -> str:
        return self.written