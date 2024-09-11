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

from typing import Self, Any, Callable
from lynq.backendutils.lynq.logger import logger
from lynq.backendutils.app.supportswith import SupportsWithKeyword
from lynq.backendutils.errors.handler import handle

class StyleAttribute(SupportsWithKeyword):
    @handle
    def __init__(self, style: Any, tag_name: str) -> None:
        self.style: Any = style
        self.name: str = tag_name
        self.written: str = ""
        self._init_attribute()

    @handle
    def _init_attribute(self) -> None:
        self._write_line(f"{self.name} " + "{")

    @handle
    def _write_line(self, contents: str) -> None:
        self.written += f"{contents}\n"

    @handle
    def add_singular(self, contents: str) -> Self:
        self._write_line(contents)
        return self

    @handle
    def add_option(self, **kwargs) -> Self:
        for key, value in kwargs.items():
            self._write_line(f"{key.replace('_', '-')}: {value};")
        return self

    @handle
    def safe_add_option(self, option: str, value: str) -> Self:
        self._write_line(f"{option}: {value};")
        return self

    @handle
    def include(self, cls: type) -> None:
        try:
            actions: dict[str, str] = cls.__style__
        except AttributeError:
            logger.error(f"Error while parsing Lynq Style module '{cls.__name__}'.")
            return

        for option, value in actions.items():
            logger.info(f"Successfully parsed Lynq Style module '{cls.__name__}'.")
            self.safe_add_option(option, value)

        logger.info(f"Successfully imported and included '{cls.__name__}'.")

    @handle
    def __exit__(self, *_) -> None:
        self.back()

    @handle
    def back(self) -> Self:
        self._write_line("}")
        return self.style

    @handle
    def get_written(self) -> str:
        return self.written