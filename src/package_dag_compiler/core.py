

import networkx as nx

from index.index_processor import IndexLoaderFactory, IndexProcessor
from index.index_parser import IndexParser
from config_reader import ConfigReaderFactory, ConfigReader

def compile_dag(index_file_path: str) -> nx.MultiDiGraph:
    """Compile the package DAG."""
    config_dict = read_config_files(index_file_path)
    dag_config = clean_and_validate_configs(config_dict)
    package_dag = create_dag(dag_config)
    return package_dag

def read_config_files(index_file_path: str) -> dict:
    """Read the configuration files."""
    # Initialize the factory and processor
    index_loader_factory = IndexLoaderFactory()
    index_processor = IndexProcessor(index_loader_factory)

    # Process the index file to get the index dictionary
    package_index_dict = index_processor.process_index(index_file_path)

    # Initialize the index parser
    index_parser = IndexParser(index_dict=package_index_dict)

    # Extract the bridges paths and runnable files paths
    bridges_file_paths = index_parser.get_and_remove_bridges()
    runnables_file_paths = index_parser.get_runnables_paths_from_index()

    # Read the package's bridges and runnables files
    config_reader_factory = ConfigReaderFactory()
    config_reader = ConfigReader(config_reader_factory)    
    all_bridges = [config_reader.read_config(bridge) for bridge in bridges_file_paths]
    all_runnables = [config_reader.read_config(runnable) for runnable in runnables_file_paths]

    # Convert the list of dictionaries to a single dictionary for bridges and runnables separately
    bridges_dict = {}
    for bridge in all_bridges:
        bridges_dict.update(bridge)
    runnables_dict = {}
    for runnable in all_runnables:
        runnables_dict.update(runnable)

    return config_dict

def clean_and_validate_configs(config_dict: dict):
    """Clean and validate the configuration files."""
    


    return dag_config

def create_dag():
    """Create the package DAG."""
    pass