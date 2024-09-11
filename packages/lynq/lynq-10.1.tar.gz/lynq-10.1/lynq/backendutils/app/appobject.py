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

from typing import Optional, Any
from lynq.backendutils.errors.handler import handle

from lynq.backendutils.lynq.logger import logger
from lynq.backendutils.launcher.launch import launch
from lynq.backendutils.app.supportswith import SupportsWithKeyword
from lynq.backendutils.lynq.lynqserverorrelated import LynqServerOrRelatedObjects
from lynq.backendutils.app.supportedtags import supported_tags
from lynq.backendutils.script.ctrl import CTRLScript
from lynq.backendutils.style.style import StyledAppAttachment

class AppObject(SupportsWithKeyword):
    @handle
    def __init__(self, name: Optional[str], app: Any = None) -> None:
        from lynq.backendutils.app.app import app as app_

        if app is None:
            logger.fatal("Please provide a parent app.")
            exit(1)

        self.server: Any = app.server
        self.name: str = f"{name}.html"
        self.app: app_ = app
        self.style_: StyledAppAttachment | None = app.style
        self.new_stylesheet_path: str = f"{self.app.fn.__name__}.css"
        self.ctrl: CTRLScript | None = None

        self.init_supported_tags(supported_tags)
        self.init_ctrlscript()

        self.on_run()

    @handle
    def on_run(self) -> None:
        logger.info("Please wait while we build your HTML file for you.")

        self.singular("<!DOCTYPE html>")
        self.singular("<html>")
        self.singular(f"<link rel=\"stylesheet\" href=\"{self.new_stylesheet_path}\">")
        self.singular(f"<script src=\"{self.app.fn.__name__}.js\"></script>")

    @handle
    def init_ctrlscript(self) -> None:
        self.ctrl = CTRLScript(self.app.fn.__name__)

    @handle
    def init_supported_tags(self, supported_tags_: list[str]) -> None:
        for tag in supported_tags_:
            exec(f"self.{tag} = lambda **args: self.tag({repr(tag)}, **args)", {"self": self})

    @handle
    def tag(self, type_: str, **kwargs: str | int) -> Any:
        from lynq.backendutils.app.tagobject import TagObject

        final_kwargs = ""

        for key, value in list(kwargs.items()):
            final_kwargs += f"{key}=\"{value}\" "

        return TagObject(self.name.removesuffix(".html"), type_, self.app, final_kwargs)

    @handle
    def singular(self, ln: str) -> None:
        with open(self.name, "a") as file:
            file.write(ln + "\n")

    @handle
    def __exit__(self, *_) -> None:
        self.exit()

    @handle
    def exit(self) -> None:
        self.singular("</html>")

        logger.info("Building has been finished successfully.")

    @handle
    def pass_to_server(self) -> None:
        if self.server is None:
            logger.fatal("Cannot pass lynq app script to server when no server was provided.")
            exit(1)

        logger.info(f"Passed '{self.name}' lynq app script to host '{type(self.server).__name__}'")

        if self.style is not None:
            logger.info(f"Passed stylesheet '{self.new_stylesheet_path}' to pebl script '{self.name}'.")

            self.style_.close()

        launch(self.server)

        logger.info("Continuing in pebl app to clear cache.")

        try: os.remove(self.name)
        except FileNotFoundError:
            logger.warn(f"Could not find '{self.name}', so it cannot be cleaned.")

        try: os.remove(self.ctrl.path)
        except FileNotFoundError:
            logger.warn(f"Could not find '{self.name}', so it cannot be cleaned.")

        if self.style_ is not None:
            try: os.remove(self.new_stylesheet_path)
            except FileNotFoundError:
                logger.warn(f"Could not find '{self.new_stylesheet_path}', so it cannot be cleaned.")