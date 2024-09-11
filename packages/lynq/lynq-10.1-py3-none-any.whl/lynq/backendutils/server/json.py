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

import json

from typing import Any

from lynq.backendutils.server.standard import Server
from lynq.backendutils.errors.handler import handle

class JsonServer(Server):
    @handle
    def __init__(self, name: str) -> None:
        with open(name) as file:
            data: Any = json.load(file)

        super().__init__(
            port=data.get("port", 8000),
            directory=data.get("directory", "./")
        )