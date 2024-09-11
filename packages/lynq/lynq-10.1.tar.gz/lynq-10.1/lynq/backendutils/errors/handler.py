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
from types import FrameType
from typing import Callable, Any

from mypy.ipc import TracebackType

def handle(fn: Callable) -> Callable:
    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        from lynq.backendutils.lynq.logger import logger
        from lynq import error_type

        try:
            result: Any = fn(*args, **kwargs)
            return result

        except KeyboardInterrupt:
            logger.warning("Abandoning Lynq while it's still running may cause currently open\n"
                           "servers to continue to take up their address in your memory.\n"
                           "Please exit the program safely or press CTRL+C/CTRL+D again.\n"
                           "Press ENTER to cancel this exit attempt."
            )
            input()
            return None  # Optionally return None here

        except Exception as err:
            traceback: TracebackType | None = err.__traceback__.tb_next

            if traceback is None:
                logger.error("An unexpected exception was raised and caught by lynq @handle,\n"
                             "but no traceback could be returned in time which cancelled the handling.\n"
                             "The source error will be handled in 'legacy' error mode.")
                raise err

            while traceback is not None:
                tb: FrameType = traceback.tb_frame

                message = (
                    f"An uncaught error has occurred while running Lynq.\n"
                    f"\n"
                    f"ERROR LOCATION: {tb.f_code.co_filename}:{tb.f_lineno} in function '{tb.f_code.co_name}'\n"
                    f"\n"
                    f"{str(err)}\n"
                    f"\n"
                    f"MORE INFO:\n"
                    f"{format_exc()}"
                )

                match error_type:
                    case "disable":
                        # Do nothing if error handling is disabled
                        pass

                    case "legacy":
                        # Re-raise the original error in legacy mode
                        raise err

                    case "default":
                        # Log fatal error and handle user input
                        logger.fatal(f"Uncaught Error: {type(err).__name__}\n\n{message}")
                        try:
                            user_input: str = input("\n\nType 1 (or press ENTER) to exit the program.\n"
                                                    "Type 2 to raise the aforementioned error.\n"
                                                    "Type 3 to submit an issue for Lynq on GitHub (will open your default browser).\n"
                                                    "Note: typing anything else which wasn't mentioned will\n"
                                                    "also exit the program.\n\n"
                                                    "[1|2|3] => ")
                        except KeyboardInterrupt:
                            user_input = "1"

                        match int(user_input or "1"):
                            case 1:
                                exit(1)

                            case 2:
                                raise err

                            case 3:
                                logger.info("Opening https://github.com/elemenom/lynq/issues/new in your default browser...")
                                os.system("start https://github.com/elemenom/lynq/issues/new")

                        exit(1)

                    case "external":
                        # Show error message using a GUI message box
                        tkinter.messagebox.showerror(f"Uncaught Error: {type(err).__name__}", message)
                        exit(1)

                traceback = traceback.tb_next

    return wrapper