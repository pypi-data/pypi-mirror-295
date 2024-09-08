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

import atexit, os, argparse, logging, json
import inspect

from typing import Any, Final

from lynq.backendutils.lynq.pycache_remover import remove_pycache_from as _remove_pycache_from

from lynq.backendutils.basin.getval import getval
from lynq.backendutils.basin.object import BasinObject

SYSVER: Final[float] = 9.8

VERSION: Final[dict[str, float | int]] = {
    "whole": SYSVER,
    "major": int(str(SYSVER).split(".")[0]),
    "minor": float(str(SYSVER).split(".")[1]) / 10
}

INSTALL: Final[dict[str, str]] = {
    "pip": "pip install lynq",
    "git": "git clone lynq --branch v10"
}

UPGRADE: Final[dict[str, str]] = {
    "pip": "pip install lynq --upgrade",
    "git": "rm -rf lynq; git clone lynq --branch v10"
}

LINKS: Final[dict[str, str]] = {
    "pypi": "https://pypi.org/project/lynq/",
    "github": "https://github.com/elemenom/lynq/",
    "github branch v10": "https://github.com/elemenom/lynq/tree/v10/",
    "github branch v10 pr": "https://github.com/elemenom/lynq/pull/27/"
}

AUTHOR: Final[dict[str, str]] = {
    "name": "Elekk aka Elemenom",
    "user": "elemenom",
    "mail": "pixilreal@gmail.com",
    "github": "https://github.com/elemenom/",
    "pypi": "https://pypi.org/user/elemenom/"
}

run: bool = True

# Checking if pypi_upload_setup.py is running this:
if "pypi_upload_setup.py" in inspect.stack()[-1].filename:
    run = False

# UPDATE RELEASE FOR PYPI (PIP)
# GIT BASH ONLY
# rm -rf dist build *.egg-info; python pypi_upload_setup.py sdist bdist_wheel; twine upload dist/*

GLOBAL_LOGGER: Any = None

launch: Any = None
directlaunch: Any = None
app: Any = None
jsonapp: Any = None
basinapp: Any = None
InternetExplorerInstance: Any = None
LynqServer: Any = None
ConfigurableLynqServer: Any = None
JsonLynqServer: Any = None
BasinLynqServer: Any = None
App: Any = None
ExportedApp: Any = None
CTRLScript: Any = None

def main() -> None:
    warn, warn2 = False, False

    _, _ = warn, warn2 # Bypass 'Redeclared unused variable' warning.

    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Basic config")

    parser.add_argument("--lq.cfile", type=str, help="Path to your lynqconfig file.")
    parser.add_argument("--lq.ctype", type=str, help="Type of your lynqconfig file. Supports 'JSON', 'BASIN' and 'PYTHON'.")

    parser.add_argument("--lq.rungui", action="store_true", help="Start a new instance of Lynq RUNGUI and exit the program.")
    parser.add_argument("--lq.clean", action="store_true", help="Clean pycache files and exit the program.")

    parser.add_argument("--lq.run_process", type=str, help="Run a process like from a Lynq RUNGUI, but presented directly from a CLI.")

    args: argparse.Namespace = parser.parse_args()

    match args.__getattribute__("lq.ctype"):
        case "JSON":
            with open(args.__getattribute__("lq.cfile")) as file:
                data: dict[str, Any] = json.load(file)

            logger = eval(data.get("logger", "None"))
            additional = eval(data.get("loggingConfig", "None"))
            level = data.get("loggingLevel", None)
            format_ = data.get("loggingFormat", None)

            cleanlogger = data.get("cleanLogger", "None")
            clean = data.get("cleanPycache", "None")
            cleanlogfile = data.get("cleanLogFile", "None")

        case "BASIN":
            data: BasinObject = BasinObject(args.__getattribute__("lq.cfile"))

            logger = eval(getval("logger", data))
            additional = eval(getval("loggingConfig", data))
            level = getval("loggingLevel", data)
            format_ = getval("loggingFormat", data)

            cleanlogger = eval(getval("cleanLogger", data, "None").title())
            clean = eval(getval("cleanPycache", data, "None").title())
            cleanlogfile = eval(getval("cleanLogFile", data, "None").title())

        case "PYTHON":
            try:
                from lynqconfig import logger as logger # type: ignore
                from lynqconfig import loggingConfig as additional # type: ignore
                from lynqconfig import loggingLevel as level # type: ignore
                from lynqconfig import loggingFormat as format_ # type: ignore

                from lynqconfig import cleanLogger as cleanlogger # type: ignore
                from lynqconfig import cleanPycache as clean # type: ignore
                from lynqconfig import cleanLogFile as cleanlogfile # type: ignore

                global launch
                global directlaunch
                global app
                global jsonapp
                global basinapp
                global InternetExplorerInstance
                global LynqServer
                global ConfigurableLynqServer
                global JsonLynqServer
                global BasinLynqServer
                global App
                global ExportedApp
                global CTRLScript

                launch = launch
                directlaunch = directlaunch
                app = app
                jsonapp = jsonapp
                basinapp = basinapp
                InternetExplorerInstance = InternetExplorerInstance
                LynqServer = LynqServer
                ConfigurableLynqServer = ConfigurableLynqServer
                JsonLynqServer = JsonLynqServer
                BasinLynqServer = BasinLynqServer
                App = App
                ExportedApp = ExportedApp
                CTRLScript = CTRLScript
            except (ModuleNotFoundError, ImportError):
                logger, \
                additional, \
                level, \
                format_, \
                clean, \
                cleanlogger, \
                cleanlogfile \
                = (None,) * 7

                warn = True

        case _:
            logger, \
            additional, \
            level, \
            format_, \
            clean, \
            cleanlogger, \
            cleanlogfile \
            = None, None, None, None, None, None, None

            warn2 = True

    PYCACHE_REMOVAL_LOCATIONS: tuple[str, ...] = (
        "",
        "backendutils",
        "backendutils.app",
        "backendutils.basin",
        "backendutils.custom",
        "backendutils.dependencies",
        "backendutils.launcher",
        "backendutils.lynq",
        "backendutils.server",
        "backendutils.style",
        "backendutils.script"
    )

    logging.basicConfig(
        level = eval(f"logging.{level}") if level else logging.DEBUG,
        format = format_ or "%(asctime)s ~ %(levelname)s | %(message)s",
        **additional or {}
    )

    global GLOBAL_LOGGER

    GLOBAL_LOGGER = logger or logging.getLogger(__name__)
    CLEAN_CACHE: bool = clean or False
    CLEAN_LOGGER: bool = cleanlogger or True

    GLOBAL_LOGGER.info(f"Started instance of Lynq v{VERSION["major"]}(.{int(VERSION["minor"] * 10)})")

    from lynq.backendutils.launcher.launch import launch
    from lynq.backendutils.launcher.direct import directlaunch
    from lynq.backendutils.app.app import app
    from lynq.backendutils.app.jsonapp import jsonapp
    from lynq.backendutils.app.basinapp import basinapp
    from lynq.backendutils.lynq.msie import InternetExplorerInstance
    from lynq.backendutils.server.standard import LynqServer
    from lynq.backendutils.server.custom import ConfigurableLynqServer
    from lynq.backendutils.server.json import JsonLynqServer
    from lynq.backendutils.server.basin import BasinLynqServer
    from lynq.backendutils.app.appobject import AppObject as App
    from lynq.backendutils.app.standardappexportobject import StandardAppExportObject as ExportedApp
    from lynq.backendutils.script.ctrl import CTRLScript

    if args.__getattribute__("lq.rungui"):
        from lynq.backendutils.lynq.rungui import run_gui

        run_gui("<onstart rungui>")

        exit()

    if args.__getattribute__("lq.clean"):
        for path in PYCACHE_REMOVAL_LOCATIONS:
            _remove_pycache_from(f"./lynq/{path.replace(".", "/")}")

        exit()

    if args.__getattribute__("lq.run_process"):
        from lynq.backendutils.lynq.rungui import run_process

        run_process(args.__getattribute__("lq.run_process"), GLOBAL_LOGGER, "<terminal (ran using lynq CLI)>")

        exit()

    if warn:
        GLOBAL_LOGGER.error("An error occured in your lynqconfig PYTHON file. All config will be ignored (default will be used for everything). Make sure you include ALL configurements, and set them to `None` if you don't need to change them.")
        GLOBAL_LOGGER.error("PLEASE NOTE THAT IF THE CONFIG TYPE IS 'PYTHON', WE ALWAYS USE THE './lynqconfig.py' PATH; THE 'configfile' ARGUMENT IS IGNORED. * This does not apply to JSON and BASIN type lynqconfig files.")

    if warn2:
        GLOBAL_LOGGER.error("None or invalid lynqconfig type provided in args, returned all options to their default values.")

    def _clean_up() -> None:
        logging.shutdown()

        if os.path.exists("throwaway.log") and cleanlogfile:
            os.remove("throwaway.log")

    def _clean_up_cache() -> None:
        GLOBAL_LOGGER.debug("Commencing pycache clean up process.")

        for path_ in PYCACHE_REMOVAL_LOCATIONS:
            _remove_pycache_from(f"./lynq/{path_.replace(".", "/")}")

    def _at_exit_func() -> None:

        GLOBAL_LOGGER.debug("Commencing logger deletion and clean up process.")

        if CLEAN_CACHE:
            _clean_up_cache()

        if CLEAN_LOGGER:
            _clean_up()

        print(f"[Exiting...] Program ended successfully. All active servers terminated.")

    atexit.register(_at_exit_func)

if run:
    main()