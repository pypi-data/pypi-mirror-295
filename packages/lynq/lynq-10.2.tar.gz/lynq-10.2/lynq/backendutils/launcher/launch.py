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

from lynq.backendutils.safety.handler import handle
from lynq.backendutils.safety.safe_input import safe_input
from lynq.backendutils.lynq.lynqserverorrelated import LynqServerOrRelatedObjects

@handle
def launch(server: LynqServerOrRelatedObjects) -> LynqServerOrRelatedObjects:
    try:
        server.open()
        safe_input("\033[1;93mPress enter to exit your Lynq server...\n\033[0m")

    finally:
        server.close()

    return server