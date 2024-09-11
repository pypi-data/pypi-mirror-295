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

from typing import Generator, Optional, Any, Callable
from contextlib import contextmanager
from lynq.backendutils.script.appendedfile import AppendedFile
from lynq.backendutils.lynq.logger import logger
from lynq.backendutils.errors.handler import handle

class CTRLScript(AppendedFile):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.init_file(f"{name}.js")

    @contextmanager
    @handle
    def function(self, name: str, *args: str) -> Generator:
        self.write(f"function {name}({', '.join(args)}) {{")
        yield
        self.write("}")

    @contextmanager
    @handle
    def export_function(self, name: str, *args: str) -> Generator:
        self.write(f"export function {name}({', '.join(args)}) {{")
        yield
        self.write("}")

    @handle
    def line(self, ln: str) -> None:
        self.write(f"{ln};")

    @handle
    def import_module(self, name: str) -> None:
        self.write(f"import {name};")

    @handle
    def let(self, **kwargs: str) -> None:
        for key, value in kwargs.items():
            self.write(f"let {key} = {value};")

    @handle
    def const(self, **kwargs: str) -> None:
        for key, value in kwargs.items():
            self.write(f"const {key} = {value};")

    @handle
    def safe_let(self, key: str, value: str) -> None:
        self.write(f"let {key} = {value};")

    @handle
    def safe_set(self, key: str, value: str) -> None:
        self.write(f"{key} = {value};")

    @handle
    def safe_const(self, key: str, value: str) -> None:
        self.write(f"const {key} = {value};")

    @handle
    def include(self, cls: type) -> None:
        try:
            actions: dict[str, Callable] = cls.__actions__
        except AttributeError:
            logger.error(f"Error while parsing CTRL module '{cls.__name__}'.")
            return

        for name, action in actions.items():
            logger.info(f"Successfully parsed CTRL module '{cls.__name__}'.")
            self.safe_save(name, lambda *args, **kwargs: action(self, *args, **kwargs))

        logger.info(f"Successfully imported and included '{cls.__name__}'.")

    @handle
    def save(self, **kwargs: Callable) -> None:
        for key, value in kwargs.items():
            self.safe_save(key, value)

    @handle
    def safe_save(self, key: str, value: Callable) -> None:
        self.__setattr__(key, value)

    @contextmanager
    @handle
    def safe_set_open(self, key: str, value: Optional[str] = None) -> Generator:
        self.write(f"{key} = {value or 'null'} {{")
        yield
        self.write("}")

    @contextmanager
    @handle
    def open(self, ln: str) -> Generator:
        self.write(f"{ln} {{")
        yield
        self.write("}")

    @handle
    def set(self, **kwargs: str) -> None:
        for key, value in kwargs.items():
            self.write(f"{key} = {value};")

    @handle
    def increment(self, **kwargs: str) -> None:
        for key, value in kwargs.items():
            self.write(f"{key} += {value};")

    @handle
    def decrement(self, **kwargs: str) -> None:
        for key, value in kwargs.items():
            self.write(f"{key} -= {value};")

    @handle
    def multiply(self, **kwargs: str) -> None:
        for key, value in kwargs.items():
            self.write(f"{key} *= {value};")

    @handle
    def divide(self, **kwargs: str) -> None:
        for key, value in kwargs.items():
            self.write(f"{key} /= {value};")