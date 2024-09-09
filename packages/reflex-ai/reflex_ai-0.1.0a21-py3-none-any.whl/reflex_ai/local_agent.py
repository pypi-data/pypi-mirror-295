"""The agent that runs on the user's local client."""

import ast
import functools
import importlib
import importlib.util
import inspect
import filecmp
import difflib
from pathlib import Path

import black
from flexai import Agent
from flexai.message import Message, UserMessage
from flexai.tool import ToolResult
from pydantic import BaseModel
from reflex_ai import paths


# NOTE: using BaseModel here instead of rx.Base due to FastAPI not liking the v1 models
class InternRequest(BaseModel):
    """The request to the AI intern."""

    prompt: str
    selected_code: str
    selected_module: str
    selected_function: str


class InternResponse(BaseModel):
    """The response from the AI intern."""

    request_id: str
    messages: list[Message]


class ToolRequestResponse(BaseModel):
    """The response from the tool to the AI intern."""

    request_id: str
    messages: list[ToolResult]


class EditResult(BaseModel):
    """The result of an edit."""

    request_id: str
    diff: str
    accepted: bool


def get_agent() -> Agent:
    """Get an instance of an intern."""
    return Agent(
        tools=[
            get_module_source,
            add_python_element,
            update_python_element,
            delete_python_element,
        ],
    )


@functools.lru_cache
def import_module_from_tmp(module_name: str):
    """Import the module from the scratchpad."""
    module = importlib.import_module(module_name)
    module_file = inspect.getsourcefile(module)
    module_tmp_file = module_file.replace(str(paths.base_paths[0].parent), str(paths.tmp_root_path))
    spec = importlib.util.spec_from_file_location(
        module.__name__,
        module_tmp_file,
    )
    new_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(new_module)
    return new_module

def diff_directories(dir1, dir2):
    """
    Compare two directories recursively. Files in each directory are
    assumed to be equal if their names and contents are equal.
    Returns a dictionary with file paths as keys and their diffs as values.
    """
    print("diffing", dir1, dir2)

    diffs = {}

    def compare_dirs(dcmp):
        for name in dcmp.diff_files:
            if not name.endswith(".py"):
                continue
            file1 = Path(dcmp.left) / name
            file2 = Path(dcmp.right) / name
            with file1.open() as f1, file2.open() as f2:
                f1_lines = f1.read().splitlines()
                f2_lines = f2.read().replace("EditableState", "rx.State").replace("from reflex_ai import rx.State\n", "").splitlines()
                diff = list(difflib.unified_diff(
                    f1_lines,
                    f2_lines,
                    fromfile=str(file1),
                    tofile=str(file2)
                ))
                diffs[file1] = diff
        for sub_dcmp in dcmp.subdirs.values():
            compare_dirs(sub_dcmp)

    dirs_cmp = filecmp.dircmp(dir1, dir2)
    compare_dirs(dirs_cmp)

    return diffs

def directory_diff():
    """Diff the scratchpad and the base directories."""
    return diff_directories(paths.base_paths[0].parent, paths.tmp_root_path)

def get_module_ast(module_name: str) -> ast.Module:
    """Get the AST of a module.

    Args:
        module_name: The name of the module.

    Returns:
        The AST of the module.
    """
    # Import the module
    module_source = get_module_source(module_name)

    # Parse the module source code into an AST
    module_ast = ast.parse(module_source)
    return module_ast


def write_module_source(module_name: str, source_code: str):
    """Write the source code of a module.

    Args:
        module_name: The name of the module.
        source_code: The source code of the module.
    """
    # Import the module.
    module = import_module_from_tmp(module_name)

    # Get the source code of the module.
    module_file = inspect.getsourcefile(module)

    # Format the source code using Black.
    source_code = black.format_str(source_code, mode=black.FileMode())

    # Write the new source code back to the module file.
    with open(module_file, "w") as file:
        file.write(source_code)


def get_module_source(module_name: str) -> str:
    """Get the source code of a module."""
    # Import the module
    module = import_module_from_tmp(module_name)

    # Get the source code of the module
    module_file = inspect.getsourcefile(module)
    with open(module_file, "r") as file:
        module_source = file.read()
    return module_source


def _find_node(tree, element_type: str, element_name: str):
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.FunctionDef)
            and element_type == "function"
            and node.name == element_name
        ):
            return node
        elif (
            isinstance(node, ast.ClassDef)
            and element_type == "class"
            and node.name == element_name
        ):
            return node
        elif isinstance(node, ast.Assign) and element_type == "variable":
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == element_name:
                    return node
    return None

import astor

def update_python_element(
    module_name: str,
    element_type: str,
    element_name: str,
    new_content: str,
    class_name: str = None,
) -> list[str]:
    """Update the source code of an element (class, function, or variable) in a module.
    
    Args:
        module_name: The name of the module.
        element_type: One of "class", "function", or "variable".
        element_name: The name of the element to update.
        new_content: The new source code of the element.
        class_name: The name of the class containing the element (if applicable).
    """
    if element_type not in ["class", "function", "variable"]:
        raise ValueError(f"Invalid element type {element_type} - must be one of 'class', 'function', or 'variable'")
    previous_source = get_module_source(module_name)
    tree = get_module_ast(module_name)

    if class_name:
        class_node = _find_node(tree, "class", class_name)
        if not class_node:
            raise ValueError(f"Class {class_name} not found. Perhaps you need to add it first?")
        target_node = _find_node(
            class_node, element_type, element_name
        )
    else:
        target_node = _find_node(tree, element_type, element_name)

    if not target_node:
        raise ValueError(
            f"{element_type.capitalize()} {element_name} not found"
        )

    new_node = ast.parse(new_content).body[0]

    if element_type == "variable":
        target_node.value = new_node.value
    else:
        for i, item in enumerate(target_node.body):
            if isinstance(item, ast.Expr) and isinstance(item.value, ast.Str):
                # Preserve docstring
                new_node.body.insert(0, item)
                break
        target_node.body = new_node.body
    
    
    return list(difflib.ndiff(previous_source, astor.to_source(tree)))

def delete_python_element(
    module_name: str, element_type: str, element_name: str, class_name: str = None
) -> list[str]:
    """Delete an element (class, function, or variable) from a module.
    
    Args:
        module_name: The name of the module.
        element_type: One of "class", "function", or "variable".
        element_name: The name of the element to delete.
        class_name: The name of the class containing the element (if applicable).
    """
    previous_source = get_module_source(module_name)
    tree = get_module_ast(module_name)

    if class_name:
        class_node = _find_node(tree, "class", class_name)
        if not class_node:
            raise ValueError(f"Class {class_name} not found")
        class_node.body = [
            node
            for node in class_node.body
            if not (
                (
                    isinstance(node, ast.FunctionDef)
                    and element_type == "function"
                    and node.name == element_name
                )
                or (
                    isinstance(node, ast.Assign)
                    and element_type == "variable"
                    and any(
                        t.id == element_name
                        for t in node.targets
                        if isinstance(t, ast.Name)
                    )
                )
            )
        ]
    else:
        tree.body = [
            node
            for node in tree.body
            if not (
                (
                    isinstance(node, ast.FunctionDef)
                    and element_type == "function"
                    and node.name == element_name
                )
                or (
                    isinstance(node, ast.ClassDef)
                    and element_type == "class"
                    and node.name == element_name
                )
                or (
                    isinstance(node, ast.Assign)
                    and element_type == "variable"
                    and any(
                        t.id == element_name
                        for t in node.targets
                        if isinstance(t, ast.Name)
                    )
                )
            )
        ]

    
    return list(difflib.ndiff(previous_source, astor.to_source(tree)))

def add_python_element(
    module_name: str,
    content: str,
    class_name: str = None,
) -> list[str]:
    """Add a new element (class, function, or variable) to a Python file after the imports.
    
    Args:
        filename: The name of the file to add the element to.
        content: The source code of the element.
        class_name: The name of the class containing the element (if applicable).
    """
    previous_source = get_module_source(module_name)
    tree = get_module_ast(module_name)
    new_element = ast.parse(content).body[0]

    if class_name:
        class_node = _find_node(tree, "class", class_name)
        if not class_node:
            raise ValueError(f"Class {class_name} not found")
        target_body = class_node.body
    else:
        target_body = tree.body

    # Find the position after the last import statement
    insert_position = 0
    for i, node in enumerate(target_body):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            insert_position = i + 1
        else:
            break
    target_body.insert(insert_position, new_element)

    
    return list(difflib.ndiff(previous_source, astor.to_source(tree)))
