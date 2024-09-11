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

import os
from typing import Optional
from lynq.backendutils.errors.handler import handle

@handle
def remove_pycache_from(path: Optional[str] = None) -> None:
    from lynq.backendutils.lynq.logger import logger

    if path is None:
        logger.error("Please provide a Pycache removal location as arg 'path'.")
        return

    path = f"{path.strip('/')}/__pycache__"

    logger.debug(f"Now clearing cache in '{path}'")

    try:
        for item in [i for i in os.listdir(path) if i.endswith(".pyc")]:
            os.remove(f"{path}/{item}")

        os.rmdir(path)
    except FileNotFoundError:
        logger.warning(f"Could not find cache item in {path}")

    else:
        logger.info(f"Successfully cleared cache item in {path}")