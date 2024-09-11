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

from typing import Optional, Callable
from lynq.backendutils.errors.handler import handle
from lynq.backendutils.lynq.lynqserverorrelated import LynqServerOrRelatedObjects
from lynq.backendutils.app.appobject import AppObject
from lynq.backendutils.app.supportswith import SupportsWithKeyword
from lynq.backendutils.app.blankslateobject import new

class WebApp(SupportsWithKeyword):
    @handle
    def __init__(self, server: Optional[LynqServerOrRelatedObjects] = None, style_path: Optional[str] = None) -> None:
        from lynq.backendutils.style.style import StyledAppAttachment

        self.style = new("StyledAppAttachmentWithBackAttribute", (StyledAppAttachment,),
            back = lambda _: self
        )(style_path)

        super().__init__()

        self.server: LynqServerOrRelatedObjects | None = server
        self.fn: Callable | None = None

        self._init_root()

    @handle
    def _init_root(self) -> None:
        self.export = new("export", (), # Export methods here:
            standard = self.export_standard,
            void = self.export_void,
            void_without_lambda = self.export_voidnolambda,
            direct = self.export_direct,
            dontpass = self.export_nopass
        )

    @handle
    def export_standard(self, fn: Callable) -> Callable:
        self.fn = fn

        from lynq.backendutils.app.standardappexportobject import StandardAppExportObject

        return lambda *args, **kwargs: StandardAppExportObject(self, *args, object_=AppObject, **kwargs)

    @handle
    def export_void(self, fn: Callable) -> Callable:
        return lambda *args, **kwargs: fn(*args, **kwargs)

    @handle
    def export_voidnolambda(self, fn: Callable) -> None:
        return fn

    @handle
    def export_direct(self, fn: Callable) -> None:
        app_object: AppObject = AppObject(fn.__name__, self)
        app_object.exit()

        try: return fn(app_object)
        finally: app_object.pass_to_server()

    @handle
    def export_nopass(self, fn: Callable) -> None:
        app_object: AppObject = AppObject(fn.__name__, self)
        app_object.exit()

        return fn(app_object)

@handle
def app(server: Optional[LynqServerOrRelatedObjects] = None, style_path: Optional[str] = None) -> WebApp:
    return WebApp(server, style_path)