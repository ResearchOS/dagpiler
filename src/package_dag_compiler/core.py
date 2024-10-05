import os

import networkx as nx

from index.index_processor import IndexLoaderFactory, IndexProcessor
from index.index_parser import IndexParser
from config_reader import ConfigReaderFactory, ConfigReader


def compile_dag(package_name: str) -> nx.MultiDiGraph:
    """Get the dependency graph of packages and their runnables.
    NOTE: This is NOT the final compiled graph, as it still needs to be fully validated and cleaned."""
    processed_packages = {}
    package_dependency_graph = nx.MultiDiGraph()
    process_package(package_name, processed_packages, package_dependency_graph)

    # Perform a topological sort to get packages in the correct order
    package_order = list(nx.topological_sort(package_dependency_graph))
    
    # Collect runnables and bridges in topological order
    all_runnables_dict = {}
    all_bridges_dict = {}
    for pkg_name in package_order:
        package_data = processed_packages[pkg_name]
        runnables = package_data["runnables"]
        bridges = package_data["bridges"]
        for runnable_name, runnable_dict in runnables.items():
            full_runnable_name = f"{pkg_name}.{runnable_name}"
            all_runnables_dict[full_runnable_name] = runnable_dict
        all_bridges_dict.update(bridges)
    
    # Proceed to clean, validate, and create the DAG
    # dag_config = clean_and_validate_configs(all_runnables_dict, all_bridges_dict)
    # package_dag = create_dag(dag_config)
    return package_dag  # Replace with the actual DAG creation

def process_package(package_name: str, processed_packages: dict, package_dependency_graph: nx.DiGraph) -> None:
    """Recursively process packages based on bridges."""
    # Check if the package has already been processed
    if package_name in processed_packages:
        return

    # Get the index file path for the package
    index_file_path = get_index_file_path(package_name)
    
    # Read the package's bridges and runnables
    package_runnables_and_bridges = get_package_runnables_and_bridges(index_file_path)
    package_bridges_dict = package_runnables_and_bridges["bridges"]
    package_runnables_dict = package_runnables_and_bridges["runnables"]

    # Store the package's data
    processed_packages[package_name] = {
        "runnables": package_runnables_dict,
        "bridges": package_bridges_dict
    }

    # From bridges, extract package dependencies
    for bridge_name, bridge in package_bridges_dict.items():
        sources = bridge.get("sources", [])
        targets = bridge.get("targets", [])
        
        # Extract package names from sources and targets
        source_packages = set(get_package_name_from_runnable(r) for r in sources if get_package_name_from_runnable(r))
        target_packages = set(get_package_name_from_runnable(r) for r in targets if get_package_name_from_runnable(r))

        # For each (source_pkg, target_pkg), add edge from target_pkg to source_pkg
        for source_pkg in source_packages:
            for target_pkg in target_packages:
                if source_pkg != target_pkg:
                    # Add edge from target package to source package
                    package_dependency_graph.add_edge(target_pkg, source_pkg)
                # Recursively process target and source packages if not already done
                if target_pkg not in processed_packages:
                    process_package(target_pkg, processed_packages, package_dependency_graph)
                if source_pkg not in processed_packages:
                    process_package(source_pkg, processed_packages, package_dependency_graph)

def get_package_name_from_runnable(runnable_full_name: str) -> str:
    """Extract the package name from a runnable's full name."""
    # Assumes format "package_name.runnable_name"
    if isinstance(runnable_full_name, str) and '.' in runnable_full_name:   
        return runnable_full_name.split('.')[0]
    return None

def get_index_file_path(package_name: str) -> str:
    """Map a package name to its index file path."""
    # Implement the logic based on your project structure
    # For example, if packages are stored in 'packages/{package_name}/index.toml':
    return os.path.join('packages', package_name, 'index.toml')

def get_package_runnables_and_bridges(index_file_path: str) -> dict:
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
    package_bridges = [config_reader.read_config(bridge) for bridge in bridges_file_paths]
    package_runnables = [config_reader.read_config(runnable) for runnable in runnables_file_paths]

    # Convert the list of dicts to a single dict for bridges and runnables
    package_bridges_dict = {}
    for bridge in package_bridges:
        package_bridges_dict.update(bridge)
    package_runnables_dict = {}
    for runnable in package_runnables:
        package_runnables_dict.update(runnable)

    return {
        "bridges": package_bridges_dict,
        "runnables": package_runnables_dict
    }




# def compile_dag(package_name: str, index_file_path: str) -> nx.MultiDiGraph:
#     """Compile the package DAG."""
#     config_dict = read_config_files(package_name, index_file_path)
#     # dag_config = clean_and_validate_configs(config_dict)
#     # package_dag = create_dag(dag_config)
#     return package_dag

# def clean_and_validate_configs(config_dict: dict):
#     """Clean and validate the configuration files."""
    


#     return dag_config

# def create_dag():
#     """Create the package DAG."""
#     pass