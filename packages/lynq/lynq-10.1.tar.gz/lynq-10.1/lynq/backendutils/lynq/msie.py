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

from subprocess import run
from typing import Callable, Optional
from lynq.backendutils.errors.handler import handle
from lynq.backendutils.lynq.pwsh import pwsh

from lynq.backendutils.lynq.logger import logger

class InternetExplorerInstance:
    def __init__(self) -> None:
        self.pwie: Callable = lambda cmd: pwsh(f"$ie = New-Object -ComObject \"InternetExplorer.Application\"; {cmd}")

    @handle
    def open(self) -> None:
        self.pwie("$ie.Visible = $true")
        logger.info("Launched new internet explorer instance.")

    @handle
    def navigate(self, link: Optional[str]) -> None:
        self.pwie(f"$ie.Navigate({repr(link) or 'http://localhost'})")
        logger.info(f"Navigated internet explorer into {link}")

    @handle
    def refresh(self) -> None:
        self.pwie("$ie.Refresh()")
        logger.info("Refresh internet explorer")