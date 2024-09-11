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

from typing import Optional, Type
from pathlib import Path
import json
import http.server
import argparse

from lynq.backendutils.server.standard import Server
from lynq.backendutils.lynq.logger import logger
from lynq.backendutils.errors.handler import handle

class ConfigurableServer(Server):
    @handle
    def __init__(self, config_file: Optional[str] = None, directory: Optional[str] = None, handler: Optional[Type[http.server.BaseHTTPRequestHandler]] = None):
        config = self.load_config(config_file)
        port = config.get("port", 8000)  # Default to int
        directory = directory or config.get("directory")
        super().__init__(port, directory, handler)

    @staticmethod
    @handle
    def load_config(config_file: Optional[str]) -> dict:
        if config_file and Path(config_file).exists():
            with open(config_file, 'r') as f:
                try:
                    config = json.load(f)
                    logger.info(f"Loaded configuration from {config_file}")
                    return config
                except json.JSONDecodeError as e:
                    logger.error(f"Error parsing config file: {e}")
        else:
            logger.warning(f"No valid config file found. Using default settings.")