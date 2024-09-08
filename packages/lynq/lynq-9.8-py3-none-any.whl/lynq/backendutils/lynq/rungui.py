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

from tkinter import Tk, Label, Entry, Button
from tkinter.messagebox import showerror, showinfo

from typing import Any, Optional

from lynq.backendutils.lynq.msie import pwsh

def run_process(text: str, logger: Any, id: Optional[str] = None) -> None:
    if text == "":
        showerror("Error", "Please enter a value. Trying to specify a FilePath in the terminal? Try running '$$TERMINAL'. (without quotes)")

        return

    elif text.upper() == "$$TERMINAL":
        print("/!\\ Continuing in a terminal does not support '$$' commands, '>' commands, '%' commands, 'lynq://' sites, and custom commands like 'lynqping', 'exit' or 'lynqhelp'.")
        text = ""

    elif text.upper() == "$$HELP":
        text = ">helplynq"
        
    elif text.upper() == "$$PING":
        text = ">pinglynq"

    elif text.upper() == "$$EXIT":
        text = ">exit"

    elif text.upper() == "$$INDEX":
        text = "lynq://app/index.py"

    elif text.upper() == "$$-8000":
        text = "lynq://8000"

    elif text.upper() == "$$-24001":
        text = "lynq://24001"

    if text.startswith("lynq://app/"):
        pwsh(f"python {text.removeprefix("lynq://app/")}.py")

    elif text.startswith("lynq://"):
        text = f"http://localhost:{text.removeprefix("lynq://")}/"

        pwsh(f"start {text}")

    elif (text.strip(">") == "exit") or (text == r"%exit"):
        logger.info("Exited Lynq RUNGUI.")

        entry.master.destroy()

    elif (text.strip(">") == "help") or (text == r"%help"):
        print("> Looking for help regarding Lynq and Lynq RUNGUI? Try '$$HELP'.")

    elif (text.strip(">") == "helplynq") or (text == r"%helplynq"):
        showinfo("Help", r"$$EXIT, %exit, >exit - exit the GUI and end the program. $$PING, %pinglynq, >pinglynq - Ping the terminal from this Lynq RUNGUI. $$TERMINAL - continue in terminal. See the 'README.md' file or run 'import lynq; print(lynq.MyLynq.help())' in a Python command line interface for more help.")

    elif (text.strip(">") == "pinglynq") or (text == r"%pinglynq"):
        logger.info(f"Ping received from Lynq RUNGUI 'id={id or "none (unnamed)"}'.")

    elif text.startswith(">") or text.startswith("%"):
        pwsh(text.strip(">") if text.strip(">") != text else text.removeprefix("%"))

    else:
        pwsh(f"start {text}")

def run_gui(id: Optional[str] = None) -> None:
    from lynq import GLOBAL_LOGGER as logger

    root: Tk = Tk()

    root.title("Run using Lynq")
    root.geometry("400x150")
    root.resizable(False, False)

    Label(root, text="Run a new process using Lynq").pack()
    entry: Entry = Entry(root, width=80)
    entry.pack(padx=10, pady=10)
    Button(root, text="Submit", command=lambda: run_process(entry.get(), logger, id)).pack(pady=10)

    logger.info("Completed dist; launch sequence initiated.")

    root.mainloop()