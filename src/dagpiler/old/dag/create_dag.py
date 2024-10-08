"""Create the DAG from the loaded TOML data."""
import networkx as nx

from dagpiler.toml_files.discover_toml import edge_list_to_vector_list
from dagpiler.toml_files.read_toml import load_toml_file, INDEX_PATH_IN_TOML, subset_toml_data, get_package_dag_from_index_dict
from dagpiler.toml_files.index import clean_index_dict

def create_dag_from_edge_list_of_toml_files(sorted_edge_list: list) -> nx.DiGraph:
    """High level function to create the DAG from the edge list of TOML file paths.
    The DAG contains the following types of nodes:
    1. Package nodes: Denoted by path names to the pyproject.toml files
    2. Runnable nodes: Denoted by the runnable type and name
    3. Variable nodes: Denoted by the variable name"""    
    # Convert the edge list to a vector list
    ordered_pyproject_toml_files = edge_list_to_vector_list(sorted_edge_list) 

    # Create the DAG
    G = nx.MultiDiGraph()

    # May help to have a root and final node that nodes with indegree or outdegree of 0, respectively can connect to
    G.add_node("root")  # Add the root node
    G.add_node("final")  # Add the final node

    # Add the project nodes. These are the pyproject.toml files
    G.add_edges_from(sorted_edge_list)
    if not nx.is_directed_acyclic_graph(G):
        raise ValueError("The packages do not constitute a directed acyclic graph.")

    G = add_runnable_and_variable_nodes(G, ordered_pyproject_toml_files)
    return G

def add_runnable_and_variable_nodes(G: nx.MultiDiGraph, ordered_pyproject_toml_files: list) -> nx.DiGraph:
    # Add the runnable and variable nodes
    for pyproject_path in ordered_pyproject_toml_files:
        # Add the runnable nodes, and the edges between them.
        runnables_and_variables_edge_list = get_package_edge_list(pyproject_path)
        G.add_edges_from(runnables_and_variables_edge_list)
        if not nx.is_directed_acyclic_graph(G):
            raise ValueError(f"The runnables and variables do not constitute a directed acyclic graph. Package: {pyproject_path}. ")
        # Add the edges between the project nodes and the runnable & variable nodes
        for source, target in runnables_and_variables_edge_list:
            G.add_edge(pyproject_path, source)
            G.add_edge(pyproject_path, target)
    return G

def get_package_edge_list(pyproject_path: str) -> list:
    """Get the edge list for the package."""    
    # 1. Read the pyproject.toml file
    toml_data = load_toml_file(pyproject_path)
    index_path = subset_toml_data(toml_data, INDEX_PATH_IN_TOML)
    index_dict = load_toml_file(index_path)
    # Clean up the index dictionary
    cleaned_index_dict = clean_index_dict(index_dict)
    package_dag = get_package_dag_from_index_dict(cleaned_index_dict)    
    return nx.to_edgelist(package_dag)