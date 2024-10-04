"""Discover all of the TOML files in the package."""
import os
from pathlib import Path

import networkx as nx

# from package_dag_compiler.toml_files.read_toml import load_toml_file, subset_toml_data
# from package_dag_compiler.toml_files.venv_handler import package_name_to_toml_path

PYPROJECT_FILENAME = "pyproject.toml"

TOOL_DEPENDENCIES = "tool.researchos.dependencies"
PROJECT_DEPENDENCIES = "project.dependencies"

def discover_pyproject_files(pyproject_folder: str, dependencies_edge_list: list = None) -> list:
    """Discover all of the pyproject.toml files - including dependencies - within the specified project.
    Input can be folder (containing one pyproject.toml file) or a pyproject.toml file.
    NOTE: Assumes that all packages have already been installed."""    

    # Input validation
    if dependencies_edge_list is None:
        dependencies_edge_list = tuple()

    # Handle pathlib Path objects
    if isinstance(pyproject_folder, Path):
        pyproject_folder = str(pyproject_folder)
    
    # Ensure that the input is a string
    if not isinstance(pyproject_folder, str):
        raise ValueError("Input must be a string path name.")
    
    # Ensure that the input is a valid path
    if not os.path.exists(pyproject_folder):
        raise ValueError(f"Path: {pyproject_folder} does not exist.")
    
    if os.path.isfile(pyproject_folder):
        # Convert the pyproject_folder to a folder, if it is a file
        if os.path.basename(pyproject_folder) != PYPROJECT_FILENAME:
            raise ValueError("Input must be a pyproject.toml file.")
        pyproject_folder = os.path.dirname(pyproject_folder)
    
    pyproject_file_path = os.path.join(pyproject_folder, PYPROJECT_FILENAME)

    if not os.path.exists(pyproject_file_path):
        raise ValueError(f"Path: {pyproject_file_path} does not exist.")
    
    # Now have a validated pyproject.toml file path.
    # Dependencies can be listed in either the [tool.researchos.dependencies] or [project.dependencies] sections.
    # [tool.researchos.dependencies] consists of absolute paths for unpublished packages, bypassing pypi and pip. Less common
    # [project.dependencies] is better for published packages, using pypi and pip. Most packages will use this.

    # Generate the dependencies edge list for the pyproject.toml file
    # The edge list is a tuple of tuples, where each tuple is a dependency relationship (dependency, dependent). 
    # Optionally, a third element can be added, which is the path for that package's pyproject.toml file (tool.researchos.dependencies only)
    pyproject_data = load_toml_file(pyproject_file_path)    
    # package_name = read_package_name(pyproject_data)
    tool_dependencies_paths = subset_toml_data(pyproject_data, TOOL_DEPENDENCIES) # Absolute file paths

    # Ensure that each path is to a pyproject.toml file, and not just a folder.
    for dep in tool_dependencies_paths:
        if os.path.isdir(dep):
            dep = os.path.join(dep, PYPROJECT_FILENAME)
        if not os.path.exists(dep):
            raise ValueError(f"From pyproject.toml file: {pyproject_file_path} Dependency path: {dep} does not exist.")        
        if os.path.basename(dep) != PYPROJECT_FILENAME:
            raise ValueError(f"Dependency path: {dep} is not a pyproject.toml file.")
    project_dependencies_names = subset_toml_data(pyproject_data, PROJECT_DEPENDENCIES) # Package names
    # project_dependencies_paths = [package_name_to_toml_path(name) for name in project_dependencies_names]
    project_dependencies_paths = []

    # Dependencies list consists of absolute .toml file paths
    tmp_deps = []
    all_dependency_paths = tool_dependencies_paths + project_dependencies_paths # Concatenate the two lists    
    for dep_pyproject_file_path in all_dependency_paths:
        tmp_deps.append(dep_pyproject_file_path, pyproject_file_path)
        dependencies_edge_list = discover_pyproject_files(dep_pyproject_file_path, dependencies_edge_list) # Recursively build the dependencies edge list

    dependencies_edge_list = dependencies_edge_list + tuple(tmp_deps) # Add the current dependencies to the edge list 
    return dependencies_edge_list

def sort_dependencies_edge_list(dependencies_edge_list: tuple) -> list:
    """Sort the dependencies edge list in topological order.
    Returns a tuple of tuples, where each tuple is a dependency relationship (dependency, dependent).
    TODO: Right now it returns a list, but it needs to be a sorted edge list."""
    # Dependencies edge list is a list of tuples, where each tuple is a dependency relationship (dependency, dependent)
    # Sort the list in topological order, where the first element is the dependency, and the second element is the dependent
    # This is a recursive function that will sort the list
    G = nx.MultiDiGraph()
    G.add_edges_from(dependencies_edge_list)

    # To ensure that the list is in the same order every time, alphabetize the list within each generation of G
    # 1. Get each generation of G
    generations_sets = list(nx.topological_generations(G)) # Returns a list of sets
    # 2. Sort each generation
    sorted_edge_list = []
    for generation in generations_sets:
        # Convert the set to a list
        generation_list = list(generation)
        generation_list.sort()
        for item in generation_list:
            predecessors = list(G.predecessors(item))
            predecessors.sort()
            for pred in predecessors:
                sorted_edge_list.append((pred, item))
    return sorted_edge_list

def edge_list_to_vector_list(edge_list: list):
    """Convert a list of tuples (an edge list) to a single list of nodes."""
    vector_list = []
    for edge in edge_list:
        for node in edge:
            if node not in vector_list:
                vector_list.append(node)
    return vector_list