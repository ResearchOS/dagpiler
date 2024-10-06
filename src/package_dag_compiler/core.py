
import networkx as nx

from compile_dag import process_package

# Hard-coded import to load Runnable types for now. In the future this should be read from configuration files.
from runnables.process import Process


def compile_dag(package_name: str) -> nx.MultiDiGraph:
    """Get the dependency graph of packages and their runnables.
    NOTE: This is NOT the final compiled graph, as it still needs to be fully validated and cleaned."""
    processed_packages = {}
    package_dependency_graph = nx.MultiDiGraph()

    # Get the DAG with all packages and their runnables, and bridged edges.
    process_package(package_name, processed_packages, package_dependency_graph)
    
    # Proceed to clean, validate, and create the DAG
    # dag_config = clean_and_validate_configs(all_runnables_dict, all_bridges_dict)
    # package_dag = create_dag(dag_config)
    return package_dependency_graph  # Replace with the actual DAG creation