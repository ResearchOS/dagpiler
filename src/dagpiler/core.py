
import networkx as nx

from compile_dag import process_package, check_no_unspecified_variables
from dag.furcate import polyfurcate_dag

# Hard-coded import to load Runnable types for now. In the future this should be read from configuration files.
from runnables.process import Process


def compile_dag(package_name: str) -> nx.MultiDiGraph:
    """Get the dependency graph of packages and their runnables.
    NOTE: This is NOT the final compiled graph, as it still needs to be fully validated and cleaned."""
    processed_packages = {}
    dag = nx.MultiDiGraph()

    # Get the DAG with all packages and their runnables, and bridged edges.
    process_package(package_name, processed_packages, dag)
    check_no_unspecified_variables(dag)
    
    # TODO: Apply package attributes to the DAG in topological order (e.g. subset names, levels, etc.)

    # Polyfurcate the DAG as needed if multiple variables input into a single variable
    dag = polyfurcate_dag(dag)

    return dag