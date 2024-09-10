import typing as t
from pathlib import Path

from _typeshed import Incomplete
from flask import Flask

from .config import Config
from .extension.library import ElementLibrary
from .page import Page
from .partial import Partial
from .state import State

class Gui:
    on_action: Incomplete
    on_change: Incomplete
    on_init: Incomplete
    on_navigate: Incomplete
    on_exception: Incomplete
    on_status: Incomplete
    on_user_content: Incomplete
    def __init__(
        self,
        page: str | Page | None = None,
        pages: dict | None = None,
        css_file: str | None = None,
        path_mapping: dict | None = None,
        env_filename: str | None = None,
        libraries: list[ElementLibrary] | None = None,
        flask: Flask | None = None,
    ) -> None: ...
    @staticmethod
    def add_library(library: ElementLibrary) -> None: ...
    @staticmethod
    def register_content_provider(
        content_type: type, content_provider: t.Callable[..., str]
    ) -> None: ...
    @staticmethod
    def add_shared_variable(*names: str) -> None: ...
    @staticmethod
    def add_shared_variables(*names: str) -> None: ...
    def __enter__(self): ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ): ...
    def invoke_callback(
        self,
        state_id: str,
        callback: t.Callable,
        args: t.Sequence[t.Any] | None = None,
        module_context: str | None = None,
    ) -> t.Any: ...
    def broadcast_callback(
        self,
        callback: t.Callable,
        args: t.Sequence[t.Any] | None = None,
        module_context: str | None = None,
    ) -> dict[str, t.Any]: ...
    def broadcast_change(self, var_name: str, value: t.Any): ...
    def broadcast_changes(self, values: dict[str, t.Any] | None = None, **kwargs): ...
    def table_on_edit(self, state: State, var_name: str, payload: dict[str, t.Any]): ...
    def table_on_delete(
        self, state: State, var_name: str, payload: dict[str, t.Any]
    ): ...
    def table_on_add(
        self,
        state: State,
        var_name: str,
        payload: dict[str, t.Any],
        new_row: list[t.Any] | None = None,
    ): ...
    def add_page(self, name: str, page: str | Page, style: str | None = "") -> None: ...
    def add_pages(
        self, pages: t.Mapping[str, str | Page] | str | None = None
    ) -> None: ...
    def add_partial(self, page: str | Page) -> Partial: ...
    def load_config(self, config: Config) -> None: ...
    def get_flask_app(self) -> Flask: ...
    state: Incomplete
    def run(self, _comparator: _ConfigComparator = ...) -> Flask | None: ...
    def reload(self) -> None: ...
    def stop(self) -> None: ...
    def set_favicon(self, favicon_path: str | Path, state: State | None = None): ...
