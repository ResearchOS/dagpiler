
import networkx as nx

def add_bridges_to_dag(package_name: str, package_bridges_dict: dict, package_dependency_graph: nx.MultiDiGraph, processed_packages: dict) -> None:
    """Add package dependencies to the package dependency graph."""
    from compile_dag import process_package, get_package_name_from_runnable

    # Check if bridges exist for the package
    if not package_bridges_dict:
            print(f"INFO: No bridges found for package {package_name}")
    # From bridges, extract package dependencies
    for bridge_name, bridge in package_bridges_dict.items():
        sources = bridge.get("sources", [])
        targets = bridge.get("targets", [])

        # For each (source_pkg, target_pkg), add edge from target_pkg to source_pkg
        for source in sources:
            source_package = get_package_name_from_runnable(source)
            for target in targets:
                target_package = get_package_name_from_runnable(target)
                                     
                # Recursively process target and source packages if not already done
                if target_package not in processed_packages:
                    process_package(target_package, processed_packages, package_dependency_graph)
                if source_package not in processed_packages:
                    process_package(source_package, processed_packages, package_dependency_graph)