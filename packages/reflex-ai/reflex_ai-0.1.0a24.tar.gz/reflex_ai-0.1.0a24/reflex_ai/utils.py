"""Utility functions for the reflex_ai package."""

import os
import shutil
from pathlib import Path


SCRATCH_DIR_NAME = "reflex_ai_tmp"

def get_scratch_dir(app_dir: Path) -> Path:
    """Get the location of the scratch directory where the agent makes changes.

    Args:
        app_dir: The directory of the app that was copied into the scratch directory.
    
    Returns:
        The path to the scratch directory.
    """
    return app_dir.parent / ".web" / SCRATCH_DIR_NAME


def create_scratch_dir(app_dir: Path, overwrite: bool = False) -> Path:
    """Create a scratch directory for the agent to make changes to.

    Args:
        app_dir: The directory of the app to copy into the scratch directory.
        overwrite: Whether to overwrite the scratch directory if it already exists.

    Returns:
        The path to the created directory.
    """
    scratch_dir = get_scratch_dir(app_dir)

    # If the scratch directory already exists, skip.
    if scratch_dir.exists() and not overwrite:
        return scratch_dir

    # Copy the app directory to a temporary path for modifications.
    shutil.copytree(
        app_dir,
        scratch_dir / app_dir.name,
        dirs_exist_ok=True,
    )

    # Perform search and replace on the copied files
    for root, _, files in os.walk(scratch_dir):
        print(files)
        for file in files:
            if not file.endswith(".py") or "rxconfig" in file:
                continue
            # Construct full file path
            file_path = os.path.join(root, file)

            # Read the file content
            with open(file_path, "r") as f:
                content = f.read()

            # Perform replacements
            content = content.replace("(rx.State)", "(EditableState)")
            content = f"from reflex_ai import EditableState\n{content}"

            # Write the modified content to the file
            print("writing to", file_path)
            with open(file_path, "w") as f:
                f.write(content)

    return scratch_dir


def commit_scratch_dir(app_dir: Path, files: list[str]):
    """Copy all files from the scratch directory back to the corresponding app directory.

    Args:
        app_dir: The original app directory to copy files back to.
        files: The list of files to copy back.
    """
    scratch_dir = get_scratch_dir(app_dir)
    for file in files:
        # Construct corresponding file path in app directory
        print("checking file", file)
        relative_path = os.path.relpath(file, app_dir.parent)
        # Copy the file
        # Read the file content
        with open(scratch_dir / relative_path, "r") as f:
            content = f.read()

        # Perform replacements
        content = content.replace("(EditableState)", "(rx.State)")
        content = content.replace("from reflex_ai import EditableState\n", "")

        # Write the modified content to the file
        print("writing to", file)
        with open(file, "w") as f:
            f.write(content)

        print(f"Copied {file} to {file}")
