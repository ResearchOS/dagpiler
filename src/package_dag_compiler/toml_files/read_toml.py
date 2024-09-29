"""Module to read all of the TOML files that a package depends on."""

import toml

INDEX_PATH_IN_TOML = "tool.package-dag-compiler.index"
RUNNABLE_PATH_IN_INDEX = "runnable"

def read_toml_files(pyproject_toml_paths: list):
    """Read all the TOML files in the package.
    TODO: The final dict returned needs to be in topological order for attribute replacements."""
    # Read the pyproject.toml file
    if not isinstance(pyproject_toml_paths, list):
        pyproject_toml_paths = [pyproject_toml_paths]

    toml_data = {}
    for pyproject_toml_path in pyproject_toml_paths:
        # Read the pyproject.toml file
        pyproject_data = read_pyproject(pyproject_toml_path)
        # Read the index.toml file
        index_toml_path = subset_toml_data(pyproject_data, INDEX_PATH_IN_TOML)
        index_data = read_index_toml(index_toml_path)
        # Read the runnable.toml file        
        runnable_data = read_runnables(index_data["runnables"])
        bridges_data = read_bridges(index_data["bridges"])

        toml_data[pyproject_toml_path]["pyproject"] = pyproject_data
        toml_data[pyproject_toml_path]["index"] = index_data
        toml_data[pyproject_toml_path]["runnables"] = runnable_data
        toml_data[pyproject_toml_path]["bridges"] = bridges_data
    return toml_data

def read_runnables(index_runnables_dict: dict):
    """Read the runnable.toml files."""
    read_fcns = {}
    read_fcns["process"] = read_runnable_process
    read_fcns["plot"] = read_runnable_plot
    read_fcns["stats"] = read_runnable_stats
    runnables_data = {}
    # For each runnable type, read the runnables' data
    for runnable_type, runnable_path in index_runnables_dict.items():
        runnables_data_of_type = read_fcns[runnable_type](runnable_path)
        runnables_data[runnable_type] = runnables_data_of_type
    return runnables_data

def read_runnable_process(runnable_path: str):
    """Read the process runnable.toml file."""
    runnable_data = load_toml_file(runnable_path)
    return runnable_data

def read_runnable_plot(runnable_path: str):
    """Read the plot runnable.toml file."""
    runnable_data = load_toml_file(runnable_path)
    return runnable_data

def read_runnable_stats(runnable_path: str):
    """Read the stats runnable.toml file."""
    runnable_data = load_toml_file(runnable_path)
    return runnable_data

def read_bridges(index_bridges_dict: dict):
    """Read the bridge.toml files."""
    bridges_data = load_toml_file(index_bridges_dict)
    return bridges_data

def read_pyproject(pyproject_toml_path: str):
    """Read the pyproject.toml file."""
    pyproject_data = load_toml_file(pyproject_toml_path)
    return pyproject_data

def read_index_toml(index_toml_path: str):
    """Read the index.toml file."""
    index = load_toml_file(index_toml_path)
    return index

def subset_toml_data(toml_data: dict, index_path: str):
    """Get the index TOML data from the TOML data."""
    index_path = index_path.split(".")
    for key in index_path:
        toml_data = toml_data[key]
    return toml_data

def load_toml_file(toml_path: str):
    """Load a TOML file."""
    with open(toml_path, "r") as file:
        toml_data = toml.load(file)
    return toml_data