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
import tkinter.messagebox
from functools import wraps
from traceback import format_exc
from types import FrameType, TracebackType
from typing import Callable, Any

def handle(fn: Callable) -> Callable:
    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        from lynq.backendutils.safety.logger import logger

        from lynq.backendutils.safety.safe_input import safe_input

        try:
            result: Any = fn(*args, **kwargs)
            return result

        except KeyboardInterrupt:
            try:
                logger().warning("Abandoning Lynq while it's still running may cause currently open\n"
                               "servers to continue to take up their address in your memory.\n"
                               "Please exit the program safely or press CTRL+C/CTRL+D again.\n"
                               "Press ENTER to cancel this exit attempt."
                )
                safe_input()

            except KeyboardInterrupt:
                logger().fatal("Exiting program... :: KeyboardInterrupt")

                exit(0)

            return

        except Exception as err:
            logger().warning(f"Lynq encountered an error ({type(err).__name__}), but the system managed to recover.")

            return

    return wrapper