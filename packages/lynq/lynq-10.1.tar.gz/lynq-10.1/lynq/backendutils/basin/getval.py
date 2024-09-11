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

from typing import Any, Optional
from lynq.backendutils.errors.handler import handle

from lynq.backendutils.basin.object import BasinObject

@handle
def getval(key: str, basin: Optional[BasinObject] = None, path: Optional[str] = None, default: Any = None) -> Any:
    return (basin or BasinObject(path)).read_whole().get(key, default)