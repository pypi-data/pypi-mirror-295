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

from typing import Generator

from contextlib import contextmanager

from lynq.backendutils.script.appendedfile import AppendedFile

class CTRLScript(AppendedFile):
    def __init__(self, name: str):
        super().__init__()

        self.init_file(f"{name}.js")

    @contextmanager
    def function(self, name: str, *args: str) -> Generator:
        self.write(f"function {name}({", ".join(list(args))}) ""{")

        yield

        self.write("}")

    @contextmanager
    def export_function(self, name: str, *args: str) -> Generator:
        self.write(f"function {name}({", ".join(list(args))}) ""{")

        yield

        self.write("}")

    def line(self, ln: str) -> None:
        self.write(f"{ln};")

    def import_module(self, name: str) -> None:
        self.write(f"import {name};")

    def let(self, **kwargs: str) -> None:
        for kwarg in list(kwargs.items()):
            self.write(f"let {kwarg[0]} = {kwarg[1]};")

    def safelet(self, key: str, value: str) -> None:
        self.write(f"let {key} = {value};")

    def safeset(self, key: str, value: str) -> None:
        self.write(f"{key} = {value};")

    def set(self, **kwargs: str) -> None:
        for kwarg in list(kwargs.items()):
            self.write(f"{kwarg[0]} = {kwarg[1]};")

    def increment(self, **kwargs: str) -> None:
        for kwarg in list(kwargs.items()):
            self.write(f"{kwarg[0]} += {kwarg[1]};")

    def decrement(self, **kwargs: str) -> None:
        for kwarg in list(kwargs.items()):
            self.write(f"{kwarg[0]} -= {kwarg[1]};")

    def multiply(self, **kwargs: str) -> None:
        for kwarg in list(kwargs.items()):
            self.write(f"{kwarg[0]} *= {kwarg[1]};")

    def divide(self, **kwargs: str) -> None:
        for kwarg in list(kwargs.items()):
            self.write(f"{kwarg[0]} /= {kwarg[1]};")