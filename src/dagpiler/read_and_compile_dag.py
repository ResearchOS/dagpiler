import os
import json

from base_dag import DAG

from .index.index_processor import INDEX_LOADER_FACTORY, IndexProcessor
from .index.index_parser import IndexParser
from .config_reader import CONFIG_READER_FACTORY, RUNNABLE_PARSER_FACTORY
from .dag.package_runnables import add_package_runnables_to_dag
from .bridges.bridges import add_bridges_to_dag

from .nodes.variables.variables import UnspecifiedVariable

def check_no_unspecified_variables(dag: DAG) -> None:
    """Check that there are no unspecified variables in the DAG."""
    unspecified_input_variables = [n for n in dag.nodes if n.__class__==UnspecifiedVariable and dag.in_degree(n)>0]
    if len(unspecified_input_variables) > 0:
        for unspecified_input_variable in unspecified_input_variables:
            print(f"Unspecified input variable found in the DAG: {unspecified_input_variable}")
        raise ValueError("Unspecified input variables found in the DAG. Please specify all inputs.")

def process_package(package_name: str, processed_packages: dict, package_dependency_graph: DAG) -> None:
    """Recursively process packages based on bridges."""
    # Check if the package has already been processed
    if package_name in processed_packages:
        return    

    # Get the index file path for the package
    index_file_path = get_index_file_path(package_name)

    os.environ["PACKAGE_FOLDER"] = os.path.dirname(index_file_path)
    
    # Read the package's bridges and runnables
    package_runnables_and_bridges = get_package_runnables_and_bridges(index_file_path)
    package_bridges_dict = package_runnables_and_bridges["bridges"]
    package_runnables_dict = package_runnables_and_bridges["runnables"]

    # Store the package's data
    processed_packages[package_name] = {
        "runnables": package_runnables_dict,
        "bridges": package_bridges_dict
    }

    if not package_runnables_dict:
        print(f"WARNING: No runnables found for package {package_name}")

    add_package_runnables_to_dag(package_name, package_runnables_dict, package_dependency_graph)    
    add_bridges_to_dag(package_name, package_bridges_dict, package_dependency_graph, processed_packages)

def get_package_name_from_runnable(runnable_full_name: str) -> str:
    """Extract the package name from a runnable's full name."""
    # Assumes format "package_name.runnable_name"
    if isinstance(runnable_full_name, str) and '.' in runnable_full_name:   
        return runnable_full_name.split('.')[0]
    return None

def get_index_file_path(package_name: str) -> str:
    """Map a package name to its index file path."""
    # Get the python folder
    python_version_folders = os.listdir(os.path.join(os.getcwd(), '.venv', 'lib'))
    # Remove folders that don't contain "python"
    python_version_folders = [folder for folder in python_version_folders if "python" in folder]
    if not python_version_folders:
        raise ValueError("No python version folders found in the virtual environment.")
    python_version_folder = python_version_folders[0]    
    installed_package_folders = os.listdir(os.path.join(os.getcwd(), '.venv', 'lib', python_version_folder, 'site-packages'))
    # Get the package folders that contain the project name
    lower_package_name = package_name.lower()
    package_folders = [folder for folder in installed_package_folders if lower_package_name in folder]
    if not package_folders:
        raise ValueError(f"Package {package_name} not found in .venv/lib/{python_version_folder}/site-packages. Is it installed?")
    # Remove folders that don't start with the package name
    package_folders = [folder for folder in package_folders if folder.startswith(lower_package_name)]    
    # If a folder has "dist-info" in its name, use that one.
    dist_info_folders = [folder for folder in package_folders if "dist-info" in folder]    

    if len(dist_info_folders) > 1:
        raise ValueError(f"Multiple dist-info folders found for {package_name}. Please specify the correct one.")
    # If a dist-info folder is found, use that one
    dist_info_folder = dist_info_folders[0]

    dist_info_folder_path = os.path.join(os.getcwd(), '.venv', 'lib', python_version_folder, 'site-packages', dist_info_folder)
    if "direct_url.json" not in os.listdir(dist_info_folder_path):
        ## Non-editable package
        package_folder_path = os.path.join(dist_info_folder_path, package_name)
        return os.path.join(package_folder_path, "index.toml")
    
    # Read the direct_url.json file
    with open(os.path.join(dist_info_folder_path, "direct_url.json"), 'r') as f:
        direct_url_json = json.load(f)            
    if direct_url_json.get("dir_info") and direct_url_json["dir_info"].get("editable") and direct_url_json["dir_info"]["editable"] is True:
        ## Editable installation
        package_folder_path = direct_url_json["url"].split("://")[-1]
        return os.path.join(package_folder_path, "src", package_name, 'index.toml')
    else:
        # Non-editable package that have a direct_url.json file
        package_folder_path = os.path.join(os.getcwd(), '.venv', 'lib', python_version_folder, 'site-packages', package_name)
        return os.path.join(package_folder_path, "index.toml")
   

def get_package_runnables_and_bridges(index_file_path: str) -> dict:
    """Read the configuration files."""
    package_root_folder = os.path.dirname(index_file_path)
    # Initialize the factory and processor
    index_processor = IndexProcessor(INDEX_LOADER_FACTORY)

    # Process the index file to get the index dictionary
    package_index_dict = index_processor.process_index(index_file_path)

    # Initialize the index parser
    index_parser = IndexParser(index_dict=package_index_dict)

    # Extract the bridges paths and runnable files paths
    bridges_file_paths = index_parser.get_and_remove_bridges()
    runnables_file_paths = index_parser.get_runnables_paths_from_index()

    for bridge_file_path in bridges_file_paths:
        if not os.path.exists(os.path.join(package_root_folder, bridge_file_path)):
            raise FileNotFoundError(f"Path {bridge_file_path} not found")
    for runnables_file_path in runnables_file_paths:
        if not os.path.exists(os.path.join(package_root_folder, runnables_file_path)):
            raise FileNotFoundError(f"Path {runnables_file_path} not found")

    # Read the package's bridges and runnables files
    config_reader = CONFIG_READER_FACTORY.get_config_reader(index_file_path)
    bridges_full_file_paths = [os.path.join(package_root_folder, bridge) for bridge in bridges_file_paths]
    package_bridges = [config_reader.read_config(bridge) for bridge in bridges_full_file_paths]

    config_parser = RUNNABLE_PARSER_FACTORY.get_runnable_parser(key="name")
    runnable_full_file_paths = [os.path.join(package_root_folder, runnable) for runnable in runnables_file_paths]    
    package_runnables = [config_parser.parse_runnable(config_reader.read_config(runnable)) for runnable in runnable_full_file_paths]

    # Convert the list of dicts to a single dict for bridges and runnables
    package_bridges_dict = {}
    for bridge in package_bridges:
        package_bridges_dict.update(bridge)
    package_runnables_dict = {}
    # Each key is the name of the runnable.
    for runnable in package_runnables:
        package_runnables_dict.update(runnable)

    return {
        "bridges": package_bridges_dict,
        "runnables": package_runnables_dict
    }