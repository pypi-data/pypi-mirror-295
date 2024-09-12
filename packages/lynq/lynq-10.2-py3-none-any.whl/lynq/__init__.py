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

import atexit, os, argparse, logging, inspect

from typing import Final

from lynq.backendutils.lynq.pycache_remover import remove_pycache_from as _remove_pycache_from

from lynq.backendutils.basin.getval import getval
from lynq.backendutils.basin.object import BasinObject

from lynq.backendutils.safety.logger import init_logger
from lynq.backendutils.yaml.loader import load_yaml_config
from lynq.backendutils.yaml.validator import validate_config

SYSVER: Final[float] = 10.2

run: bool = True

print(inspect.stack()[-1].filename)

# Checking if pypi_upload_setup.py is running this:
if "pypi_upload_setup.py" in inspect.stack()[-1].filename:
    run = False

# UPDATE RELEASE FOR PYPI (PIP)
# GIT BASH ONLY
# ```
# rm -rf dist build lynq.egg-info
# python pypi_upload_setup.py sdist bdist_wheel
# twine upload dist/* --username __token__ --password
# ```

def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Basic config")

    parser.add_argument("-F", "--File", type=str, help="Path to your lynqconfig.yaml file.")

    parser.add_argument("--Rungui", action="store_true", help="Start a new instance of Lynq RUNGUI and exit the program.")
    parser.add_argument("--Clean", action="store_true", help="Clean pycache files and exit the program.")

    parser.add_argument("--Run-Process", type=str, help="Run a process like from a Lynq RUNGUI, but presented directly from a CLI.")

    args, _ = parser.parse_known_args()

    with open(args.File or "lynqconfig.yaml", "r+") as file:
        if file.read().strip() == "":
            file.write("""
logger:
loggingConfig:
loggingLevel:
loggingFormat:

cleanLogger:
cleanPycache:
cleanLogFile:

safety:            
""")

    data = load_yaml_config(args.File or "lynqconfig.yaml")

    logger_ = data.get("logger")
    additional = data.get("loggingConfig")
    level = data.get("loggingLevel")
    format_ = data.get("loggingFormat")

    cleanlogger = data.get("cleanLogger")
    clean = data.get("cleanPycache")
    cleanlogfile = data.get("cleanLogFile")

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
        "backendutils.script",
        "backendutils.yaml",
        "backendutils.safety"
    )

    logging.basicConfig(
        level = eval(f"logging.{level}") if level else logging.DEBUG,
        format = format_ or "%(asctime)s ~ %(levelname)s | %(message)s",
        **additional or {}
    )

    init_logger(logger_ or logging.getLogger(__name__))

    from lynq.backendutils.safety.logger import logger
    
    CLEAN_CACHE: bool = clean or False
    CLEAN_LOGGER: bool = cleanlogger or True

    logger().info(f"Started instance of Lynq {SYSVER}.")

    if args.Rungui:
        from lynq.backendutils.lynq.rungui import run_gui

        run_gui("<onstart rungui>")

        exit()

    if args.Clean:
        for path in PYCACHE_REMOVAL_LOCATIONS:
            _remove_pycache_from(f"./lynq/{path.replace(".", "/")}")

        exit()

    if args.Run_Process:
        from lynq.backendutils.lynq.rungui import run_process

        run_process(args.Run_Process, logger, "<terminal Run-Process instance>")

        exit()

    def _clean_up() -> None:
        logging.shutdown()

        if os.path.exists("throwaway.log") and cleanlogfile:
            os.remove("throwaway.log")

    def _clean_up_cache() -> None:
        logger().debug("Commencing pycache clean up process.")

        for path_ in PYCACHE_REMOVAL_LOCATIONS:
            _remove_pycache_from(f"./lynq/{path_.replace(".", "/")}")

    def _at_exit_func() -> None:

        logger().debug("Commencing logger deletion and clean up process.")

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
from lynq.backendutils.app.appobject import AppObject as SelfApp
from lynq.backendutils.app.standardappexportobject import StandardAppExportObject
from lynq.backendutils.script.ctrl import CTRLScript
from lynq.backendutils.server.yaml import YamlServer
from lynq.backendutils.app.yamlapp import yamlapp
from lynq.backendutils.app.remoteapp import rmtapp