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
git clone https://github.com/elemenom/lynq.git
```

**Upgrade**

To upgrade Lynq, you can use either pip or git.

Using pip:
```
pip install lynq --upgrade
```

Using git:
```
rm -rf lynq; git clone https://github.com/elemenom/lynq.git
```

**Links**

- PyPI: https://pypi.org/project/lynq/
- GitHub: https://github.com/elemenom/lynq/

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

**Lynq Error Handling**

Lynq offers a total of 4 modes you can use to handle errors:
- 'disable' (errors will not show and lynq will try to recover as best as it can)
- 'legacy' (python's default error handling)
- 'external (uses lynq's modern external window handling)
- 'default' (default option when the argument isn't provided, provides a user-friendly error handling experience)

To select a handling type,

We recommend using the 'default' option.

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