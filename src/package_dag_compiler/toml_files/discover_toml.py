"""Discover all of the TOML files in the package."""
import os

import toml
from package_dag_compiler.constants import PACKAGES_PREFIX

def discover_pyproject_files(root_folders: str = os.getcwd()) -> list:
    """Discover all of the pyproject.toml files within the specified root folders."""
    if not isinstance(root_folders, list):
        root_folders = [root_folders]
    
    pyproject_files = []    
    for folder in root_folders:
        for root, dirs, files in os.walk(folder):
            for file_name in files:
                if file_name.endswith('.toml') and file_name.startswith(PACKAGES_PREFIX):
                    full_path = os.path.join(root, file_name)
                    pyproject_files.append(full_path)
    return pyproject_files