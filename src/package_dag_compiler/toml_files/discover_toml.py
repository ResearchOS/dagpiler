"""Discover all of the TOML files in the package."""
import os

pyproject_filename = "pyproject.toml"

def discover_pyproject_files(root_folders: str = os.getcwd()) -> list:
    """Discover all of the pyproject.toml files within the specified root folders by .toml files starting with "ros-".
    Input can be folder(s) or pyproject.toml file(s).
    # TODO: Need to also read the TOML files listed as dependencies in each pyproject.toml"""
    if not isinstance(root_folders, list):
        root_folders = [root_folders]
    
    pyproject_files = []    
    for folder in root_folders:
        if os.path.isfile(folder) and folder.endswith('.toml'):
            folder = os.path.dirname(folder)
        elif not os.path.isdir(folder):
            raise ValueError(f"Folder {folder} does not exist.")                        
        for root, dirs, files in os.walk(folder):
            for file_name in files:
                if file_name.endswith('.toml') and file_name==pyproject_filename:
                    full_path = os.path.join(root, file_name)
                    pyproject_files.append(full_path)
    return pyproject_files