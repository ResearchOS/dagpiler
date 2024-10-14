
import networkx as nx

from .read_and_compile_dag import process_package, check_no_unspecified_variables
from .dag.furcate import polyfurcate_dag
from .dag.printer import json_to_graph
from .config_reader import CONFIG_READER_FACTORY

# Hard-coded import to load Runnable types for now. In the future this should be read from configuration files.
from .runnables.process import Process


def compile_dag(package_name: str, file_path: str = None) -> nx.MultiDiGraph:
    """Get the dependency graph of packages and their runnables."""    
    if file_path:
        # Create a config reader, read the config file, and convert it to DAG.
        return json_to_graph(CONFIG_READER_FACTORY.get_config_reader(file_path).read_config(file_path))
    
    processed_packages = {}
        
    dag = nx.MultiDiGraph()

    # Get the DAG with all packages and their runnables, and bridged edges.
    process_package(package_name, processed_packages, dag)
    check_no_unspecified_variables(dag)

    # Polyfurcate the DAG as needed if multiple variables input into a single variable
    dag = polyfurcate_dag(dag)

    return dag