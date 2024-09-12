"""The local Reflex agent."""

import importlib
import inspect
from pathlib import Path
import types
from types import FunctionType

import reflex as rx
import sys

from reflex_ai import paths, utils


class EditableState(rx.State):
    """Rewrite rx.State imports in copied modules to this new class to avoid conflicts."""

    @classmethod
    def get_name(cls) -> str:
        """Get the name of the state.

        Returns:
            The name of the state.
        """
        module = cls.__module__.replace(".", "___")
        return rx.utils.format.to_snake_case(f"Editable___{module}___{cls.__name__}")


def enable(app: rx.App):
    """Enable the agent on an app.

    Args:
        app: The app to enable the agent on.

    Note:
        For now, this must be called before add_page is called as
        we override the add_page method.
    """
    from reflex.utils.exec import is_prod_mode
    from reflex import reflex

    # Ensure that user logs in before using the app.
    reflex._login()

    # Skip if in production mode.
    if is_prod_mode():
        return

    from .selection import clickable
    from .playground import playground

    # The base path is the directory where the app is defined.
    caller_frame = inspect.stack()[1]
    caller_path = caller_frame.filename

    # We care about the main directory, where the files live, and the parent directory, where .web lives
    base_paths = [Path(caller_path).parent, Path(caller_path).parent.parent]

    # Skip if the base path is a temporary directory.
    if utils.SCRATCH_DIR_NAME in str(base_paths[0]):
        return

    tmp_root_path = utils.create_scratch_dir(base_paths[0])
    paths.base_paths = base_paths
    paths.tmp_root_path = tmp_root_path
    filename = tmp_root_path / base_paths[0].name / "__init__.py"
    spec = importlib.util.spec_from_file_location(
            "tmp" + base_paths[0].name,
            filename,
        )
    new_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(new_module)
    sys.modules["tmp" + base_paths[0].name] = new_module
    
    def add_page(self, component, *args, **kwargs):
        # Skip if the component is not a function.
        if not isinstance(component, FunctionType):
            return

        # Add the page normally.
        route = kwargs.pop("route", rx.utils.format.format_route(component.__name__))
        rx.App.add_page(self, component, *args, route=route, **kwargs)

        # Determine which module the component came from
        module = inspect.getmodule(component)
        if module is None:
            # Skip if the component does not come from a known module.
            return

        # Get the scratch module path.
        module_path = inspect.getfile(component)
        new_module_path = Path(module_path.replace(str(base_paths[0].parent), str(tmp_root_path)))
        spec = importlib.util.spec_from_file_location(
            "tmp" + module.__name__,
            new_module_path,
        )
        new_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(new_module)

        # Add the page on the edit route.
        rx.App.add_page(
            self,
            clickable(base_paths=base_paths)(
                lambda: playground(getattr(new_module, component.__name__))
            ),
            route=f"/{route}/edit" if route != "index" else "/edit",
        )

    app.add_page = types.MethodType(add_page, app)