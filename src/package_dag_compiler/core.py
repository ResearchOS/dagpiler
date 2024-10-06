
import networkx as nx

from compile_dag import process_package

# Hard-coded import to load Runnable types for now. In the future this should be read from configuration files.
from runnables.process import Process


def compile_dag(package_name: str) -> nx.MultiDiGraph:
    """Get the dependency graph of packages and their runnables.
    NOTE: This is NOT the final compiled graph, as it still needs to be fully validated and cleaned."""
    processed_packages = {}
    dag = nx.MultiDiGraph()

    # Get the DAG with all packages and their runnables, and bridged edges.
    process_package(package_name, processed_packages, dag)
    unspecified_input_variables = [n for n in dag.nodes if n.__class__.__name__=="UnspecifiedInputVariable"]
    if len(unspecified_input_variables) > 0:
        for unspecified_input_variable in unspecified_input_variables:
            print(f"Unspecified input variable found in the DAG: {unspecified_input_variable}")
        raise ValueError("Unspecified input variables found in the DAG. Please specify all inputs.")
    
    # TODO: Apply package attributes to the DAG in topological order (e.g. subset names, levels, etc.)

    # TODO: Polyfurcate the DAG as needed if multiple variables input into a single variable
    
    return dag  # Replace with the actual DAG creation