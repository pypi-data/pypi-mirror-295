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

import http.server
import socketserver
import webbrowser
import threading
from pathlib import Path
from typing import Optional, Type

from lynq.backendutils.lynq.logger import logger
from lynq.backendutils.errors.handler import handle

class Server:
    @handle
    def __init__(self, port: int, directory: Optional[str] = None, handler: Optional[Type[http.server.BaseHTTPRequestHandler]] = None):
        self.port: int = port
        self.directory: Path = Path(directory) if directory else Path.cwd()
        self.handler: Type[http.server.BaseHTTPRequestHandler] = handler or self._create_handler()
        try:
            self.httpd: socketserver.TCPServer = socketserver.TCPServer(("localhost", self.port), self.handler)
            self.httpd.directory = str(self.directory)  # type: ignore
            logger.info(f"Server initialized on port {self.port} with directory {self.directory}")
        except OSError as e:
            logger.error(f"Could not start server on port {self.port}: {e}")
            exit(1)

    @handle
    def _create_handler(self) -> Type[http.server.BaseHTTPRequestHandler]:
        class CustomHandler(http.server.SimpleHTTPRequestHandler):
            def translate_path(self, path: str) -> str:
                # Removes query parameters, etc., from the URL path
                path = path.split('?', 1)[0]
                path = path.split('#', 1)[0]
                path = Path(path).relative_to('/')

                # Combine the requested path with the server's directory
                full_path = self.server.directory / path # type: ignore

                # Resolve the final absolute path
                return str(full_path.resolve())
        return CustomHandler

    @handle
    def _start_server(self) -> None:
        server_thread: threading.Thread = threading.Thread(target=self.httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        logger.info(f"Server started on port {self.port}")

    @handle
    def open(self) -> None:
        self._start_server()
        url = f"http://localhost:{self.port}"
        logger.info(f"Opening browser at {url}")
        webbrowser.open(url)

    @handle
    def _stop_server(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        logger.info(f"Server on port {self.port} stopped")

    @handle
    def close(self) -> None:
        self._stop_server()