"""Module to read all of the TOML files that a package depends on."""

import toml
import networkx as nx

from package_dag_compiler.toml_files.index import clean_and_validate_runnable

INDEX_PATH_IN_TOML = "tool.package-dag-compiler.index"
RUNNABLE_TABLE_NAME = "runnable"

def get_package_dag_from_index_dict(index_dict: dict) -> nx.DiGraph:
    """Get the package DAG from the index dictionary.
    NOTE: The index dict in the index.toml file can have any dictionary structure that suits the person, where each final value is the relative path to a TOML file.
    Within each toml file, there will be a list of [[runnable]] tables."""
    package_dag = nx.MultiDiGraph()
    # The index dict can be potentially infinitely nested. Flatten it here to a list of paths
    index_paths_list = flatten_index_dict(index_dict)
    for path in index_dict.items():
        toml_file_data = load_toml_file(path)
        runnables = toml_file_data.get(RUNNABLE_TABLE_NAME, [])
        for runnable in runnables:
            runnable = clean_and_validate_runnable(runnable)
            runnable_type = runnable["type"]
                
        # reader_fcn = get_index_reader(key)
        path_list = []
        for runnable_toml_path in path_list:
            toml_data = load_toml_file(runnable_toml_path)
            # runnables_dag = reader_fcn(toml_data)
            runnables_dag = nx.DiGraph()
            package_dag = nx.compose(package_dag, runnables_dag)
    return package_dag
    
def flatten_index_dict(index_dict: dict) -> list:
    """Flatten the index dictionary to a list of paths."""
    # Flatten the dictionary. This is a recursive function.
    def flatten_dict(d: dict, parent_key: str = "", sep: str = ".") -> dict:
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    return flatten_dict(index_dict)

def read_package_name(pyproject_toml_path: str):
    """Read the name of the package from the pyproject.toml file."""
    with open(pyproject_toml_path, "r") as file:
        pyproject_data = toml.load(file)
    if "project" not in pyproject_data:
        raise ValueError(f"Project section not found in {pyproject_toml_path}.")
    if "name" not in pyproject_data["project"]:
        raise ValueError(f"Name not found in project section of {pyproject_toml_path}.")
    package_name = pyproject_data["project"]["name"]
    return package_name

def read_runnable_process(runnable_toml_data: str):
    """Read the process runnable.toml file."""
    # Clean the runnable TOML data, ensuring it has the required fields
    process_required_fields = ["name", "inputs", "outputs", "command"]
    return runnable_toml_data

def read_runnable_plot(runnable_toml_data: str):
    """Read the plot runnable.toml file."""
    return runnable_toml_data

def read_runnable_stats(runnable_toml_data: str):
    """Read the stats runnable.toml file."""
    return runnable_toml_data

def read_bridges(bridges_toml_data: dict):
    """Read the bridge.toml files."""
    return bridges_toml_data

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