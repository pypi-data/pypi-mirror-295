# Welcome to Lynq
### This documentation including its installation guide may only be applicable to Lynq 10(.2)

**Documentation for Lynq**

Lynq is a Python-based framework designed to simplify the development and management of web applications.
It provides a set of tools and utilities to streamline the development process,
enhance security, and improve performance.

**Installation**

To install Lynq, you can use either pip or git.

***Recommended*** | Install Lynq v10.2 using pip:
```commandline
pip install lynq
```

*Updated in v10.2* | Download source code for Lynq v10.2 using:
```commandline
git clone https://github.com/elemenom/lynq.git
```

**Download Source Code

**Upgrade**

To upgrade Lynq, you can use either pip or git.

Using pip:
```commandline
pip install lynq --upgrade
```

*Updated in v10.2* | Using git:
```commandline
rm -rf lynq

git clone https://github.com/elemenom/lynq.git
```

**Links**

- GitHub: https://github.com/elemenom/lynq/
- PyPI: https://pypi.org/project/lynq/

**Author**

- Name: Elekk aka Elemenom
- Username: elemenom
- Mail: pixilreal@gmail.com
- GitHub: https://github.com/elemenom/
- PyPI: https://pypi.org/user/elemenom/

**Command-Line Interface (CLI) Usage**

*Most of this section was updated in v10.2*

Lynq provides a command-line interface (CLI) to perform various tasks such as running the application, cleaning pycache files, and running processes directly from the CLI.

To use the CLI, you can run the following commands:

- Run the application with GUI:
```commandline
python -m lynq --rungui
```

- Clean pycache files:
```commandline
python -m lynq --clean
```

- Run a process directly from the CLI:
```commandline
python -m lynq --run_process "<process_command>"
```

**Lynq Configuration**

*Updated in v10.2* | Lynq supports configuration in YAML.

- To link a .yaml file, run your file like this:
```commandline
python main.py -F lynqconfig.yaml
```
or
```commandline
python main.py --File lynqconfig.yaml
```

**Important Note**

Please note that the `backendutils` directory is not intended to be accessed directly. It contains internal utilities and modules used by Lynq. Any code within this directory should not be modified or accessed directly.