"""
# Welcome to Lynq
### This documentation including its installation guide may only be applicable to Lynq 9(.6)

**Documentation for Lynq**

Lynq is a Python-based framework designed to simplify the development and management of web applications. It provides a set of tools and utilities to streamline the development process, enhance security, and improve performance.

**Installation**

To install Lynq, you can use either pip or git.

Using pip:
```
pip install lynq
```

Using git:
```
git clone https://github.com/elemenom/lynq.git --branch v10
```

**Upgrade**

To upgrade Lynq, you can use either pip or git.

Using pip:
```
pip install lynq --upgrade
```

Using git:
```
rm -rf lynq; git clone https://github.com/elemenom/lynq.git --branch v10
```

**Links**

- PyPI: https://pypi.org/project/lynq/
- GitHub: https://github.com/elemenom/lynq/
- GitHub branch v10: https://github.com/elemenom/lynq/tree/v10/
- GitHub branch v10 Pull Request: https://github.com/elemenom/lynq/pull/27/

**Author**

- Name: Elekk aka Elemenom
- User: elemenom
- Mail: pixilreal@gmail.com
- GitHub: https://github.com/elemenom/
- PyPI: https://pypi.org/user/elemenom/

**Command-Line Interface (CLI) Usage**

Lynq provides a command-line interface (CLI) to perform various tasks such as running the application, cleaning pycache files, and running processes directly from the CLI.

To use the CLI, you can run the following commands:

- Run the application with GUI:
```
python -m lynq --lq.rungui
```

- Clean pycache files:
```
python -m lynq --lq.clean
```

- Run a process directly from the CLI:
```
python -m lynq --lq.run_process "<process_command>"
```

**Lynq Configuration**

Lynq supports different types of configuration files, such as JSON, BASIN, and PYTHON. You can specify the configuration file and type using command-line arguments.

To use a JSON configuration file:
```
python myproject.py --lq.cfile "path_to_config_file.json" --lq.ctype "JSON"
```

To use a BASIN configuration file:
```
python myproject.py --lq.cfile "path_to_config_file.basin" --lq.ctype "BASIN"
```

To use a PYTHON configuration file:
```
python myproject.py lq.cfile "" --lq.ctype "PYTHON"
```

(i) The `lq.cfile` argument is ignored and can be blank when PYTHON is used as `lq.ctype`.

**Lynq Components**

Lynq consists of several components that provide various functionalities. Some of the key components are:

- `launch`: A module for launching web applications.
- `directlaunch`: A module for launching web applications directly without having to explicitly define a `Server`.
- `app`: An app decorator for managing web application objects.
- `jsonapp`: An app decorator for managing web application objects using JSON.
- `basinapp`: An app decorator for managing web application objects using BASIN.
- `InternetExplorerInstance`: A class for managing Internet Explorer instances.
- `Server`: A class for managing standard Lynq servers.
- `ConfigurableServer`: A class for managing customizable Lynq servers.
- `JsonServer`: A class for managing Lynq servers using JSON.
- `BasinServer`: A class for managing Lynq servers using BASIN.
- `App`: A class for representing web application objects.
- `ExportedApp`: A class for representing exported web application objects.

**Important Note**

Please note that the `backendutils` directory is not intended to be accessed directly. It contains internal utilities and modules used by Lynq. Any code within this directory should not be modified or accessed directly.

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

from typing import Any, Final, Callable

from lynq.backendutils.lynq.pycache_remover import remove_pycache_from as _remove_pycache_from

from lynq.backendutils.basin.getval import getval
from lynq.backendutils.basin.object import BasinObject

from lynq.backendutils.lynq.logger import init_logger

SYSVER: Final[float] = 10.1

run: bool = True

error_type: str | None = None

# Checking if pypi_upload_setup.py is running this:
if "pypi_upload_setup.py" in inspect.stack()[-1].filename:
    run = False

# UPDATE RELEASE FOR PYPI (PIP)
# GIT BASH ONLY
# rm -rf dist build lynq.egg-info; python pypi_upload_setup.py sdist bdist_wheel; twine upload dist/*

def main() -> None:
    warn, warn2 = False, False

    _, _ = warn, warn2 # Bypass 'Redeclared unused variable' warning.

    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Basic config")

    parser.add_argument("--lq_cfile", type=str, help="Path to your lynqconfig file.")
    parser.add_argument("--lq_ctype", type=str, help="Type of your lynqconfig file. Supports 'JSON', 'BASIN' and 'PYTHON'.")

    parser.add_argument("--lq_rungui", action="store_true", help="Start a new instance of Lynq RUNGUI and exit the program.")
    parser.add_argument("--lq_clean", action="store_true", help="Clean pycache files and exit the program.")

    parser.add_argument("--lq_run_process", type=str, help="Run a process like from a Lynq RUNGUI, but presented directly from a CLI.")
    parser.add_argument("--lq_errors", type=str, help="Choose how errors will display. "
                                                      "Supports 'disable' (errors will not show and lynq will try to recover as best as it can), "
                                                      "'legacy' (python's default error handling), "
                                                      "'external (uses lynq's modern external window handling), "
                                                      "'default' (default option when the argument isn't provided, provides a user-friendly error handling experience)"
    )

    args, _ = parser.parse_known_args()

    global error_type

    error_type = (args.__getattribute__("lq_errors") or "default").lower()

    match args.__getattribute__("lq_ctype"):
        case "JSON":
            with open(args.__getattribute__("lq_cfile")) as file:
                data: dict[str, Any] = json.load(file)

            logger_ = eval(data.get("logger", "None"))
            additional = eval(data.get("loggingConfig", "None"))
            level = data.get("loggingLevel", None)
            format_ = data.get("loggingFormat", None)

            cleanlogger = data.get("cleanLogger", "None")
            clean = data.get("cleanPycache", "None")
            cleanlogfile = data.get("cleanLogFile", "None")

        case "BASIN":
            basin_data: BasinObject = BasinObject(args.__getattribute__("lq_cfile"))

            logger_ = eval(getval("logger", basin_data))
            additional = eval(getval("loggingConfig", basin_data))
            level = getval("loggingLevel", basin_data)
            format_ = getval("loggingFormat", basin_data)

            cleanlogger = eval(getval("cleanLogger", basin_data, "None").title())
            clean = eval(getval("cleanPycache", basin_data, "None").title())
            cleanlogfile = eval(getval("cleanLogFile", basin_data, "None").title())

        case "PYTHON":
            try:
                from lynqconfig import logger as logger_ # type: ignore
                from lynqconfig import loggingConfig as additional # type: ignore
                from lynqconfig import loggingLevel as level # type: ignore
                from lynqconfig import loggingFormat as format_ # type: ignore

                from lynqconfig import cleanLogger as cleanlogger # type: ignore
                from lynqconfig import cleanPycache as clean # type: ignore
                from lynqconfig import cleanLogFile as cleanlogfile # type: ignore

            except (ModuleNotFoundError, ImportError):
                logger_, \
                additional, \
                level, \
                format_, \
                clean, \
                cleanlogger, \
                cleanlogfile \
                = (None,) * 7

                warn = True

        case _:
            logger_, \
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

    init_logger(logger_ or logging.getLogger(__name__))

    from lynq.backendutils.lynq.logger import logger
    
    CLEAN_CACHE: bool = clean or False
    CLEAN_LOGGER: bool = cleanlogger or True

    logger.info(f"Started instance of Lynq {SYSVER}.")

    if args.__getattribute__("lq_rungui"):
        from lynq.backendutils.lynq.rungui import run_gui

        run_gui("<onstart rungui>")

        exit()

    if args.__getattribute__("lq_clean"):
        for path in PYCACHE_REMOVAL_LOCATIONS:
            _remove_pycache_from(f"./lynq/{path.replace(".", "/")}")

        exit()

    if args.__getattribute__("lq_run_process"):
        from lynq.backendutils.lynq.rungui import run_process

        run_process(args.__getattribute__("lq_run_process"), logger, "<terminal (ran using lynq CLI)>")

        exit()

    if warn:
        logger.error("An error occured in your lynqconfig PYTHON file. All config will be ignored (default will be used for everything). Make sure you include ALL configurements, and set them to `None` if you don't need to change them.")
        logger.error("PLEASE NOTE THAT IF THE CONFIG TYPE IS 'PYTHON', WE ALWAYS USE THE './lynqconfig.py' PATH; THE 'configfile' ARGUMENT IS IGNORED. * This does not apply to JSON and BASIN type lynqconfig files.")

    if warn2:
        logger.error("None or invalid lynqconfig type provided in args, returned all options to their default values.")

    def _clean_up() -> None:
        logging.shutdown()

        if os.path.exists("throwaway.log") and cleanlogfile:
            os.remove("throwaway.log")

    def _clean_up_cache() -> None:
        logger.debug("Commencing pycache clean up process.")

        for path_ in PYCACHE_REMOVAL_LOCATIONS:
            _remove_pycache_from(f"./lynq/{path_.replace(".", "/")}")

    def _at_exit_func() -> None:

        logger.debug("Commencing logger deletion and clean up process.")

        if CLEAN_CACHE:
            _clean_up_cache()

        if CLEAN_LOGGER:
            _clean_up()

        print(f"[Exiting...] Program ended successfully. All active servers terminated.")

    atexit.register(_at_exit_func)

if run:
    main()

from lynq.backendutils.launcher.launch import launch
from lynq.backendutils.launcher.direct import directlaunch
from lynq.backendutils.app.app import app
from lynq.backendutils.app.jsonapp import jsonapp
from lynq.backendutils.app.basinapp import basinapp
from lynq.backendutils.lynq.msie import InternetExplorerInstance
from lynq.backendutils.server.standard import Server
from lynq.backendutils.server.custom import ConfigurableServer
from lynq.backendutils.server.json import JsonServer
from lynq.backendutils.server.basin import BasinServer
from lynq.backendutils.app.appobject import AppObject
from lynq.backendutils.app.standardappexportobject import StandardAppExportObject
from lynq.backendutils.script.ctrl import CTRLScript