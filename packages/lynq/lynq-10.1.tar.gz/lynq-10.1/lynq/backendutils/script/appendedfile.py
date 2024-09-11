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
from lynq.backendutils.lynq.logger import logger

class AppendedFile:
    def __init__(self) -> None:
        self.path: Optional[str] = None

    def init_file(self, path: str) -> None:
        self.path = path
        self.write()  # Initialize with an empty line

    def write(self, cont: Optional[str] = None) -> None:
        if self.path is None:
            logger.fatal("Cannot write to file appendant when file was not initialized.")
            raise ValueError("File path is not initialized.")

        try:
            with open(self.path, "a") as file:
                file.write((cont or "") + "\n")
        except IOError as e:
            logger.error(f"Failed to write to file '{self.path}': {e}")
            raise

    def read(self) -> str:
        if self.path is None:
            logger.fatal("Cannot read from file appendant when file was not initialized.")
            raise ValueError("File path is not initialized.")

        try:
            with open(self.path) as file:
                return file.read()
        except IOError as e:
            logger.error(f"Failed to read from file '{self.path}': {e}")
            raise