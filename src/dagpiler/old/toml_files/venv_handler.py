import os

VENV_PATHS = {}
VENV_PATHS["conda"] = "envs"
VENV_PATHS["venv"] = os.path.join("venv", "lib", "python3.12", "site-packages")

def package_name_to_toml_path(pyproject_folder: str, package_name: str, venv_type: str = "venv") -> str:
    """Convert a package name to a path."""
    from toml_files.discover_toml import PYPROJECT_FILENAME
    return os.path.join(pyproject_folder, VENV_PATHS[venv_type], package_name, PYPROJECT_FILENAME)