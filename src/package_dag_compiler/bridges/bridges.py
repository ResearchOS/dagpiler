
import networkx as nx

from variables.variables import VARIABLE_FACTORY

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

                # TODO: Add edge from source to target (if both dynamic)
                # OR if source is hard-coded and target is dynamic, then don't add an edge
                # TODO: Either way, need to convert unspecified to another variable type.
                if source != target:
                    # Be sure to remove slicing from the source variable, and use the full variable name
                    input_variable = VARIABLE_FACTORY.create_variable(target, source)
                    # Handle the case where source and target are both dynamic variables
                    # Handle the case where source is hard-coded and target is dynamic. In that 
                    output_variable = VARIABLE_FACTORY.create_variable(source)
                    assert input_variable in package_dependency_graph.nodes, f"Variable value {input_variable} not found as an input variable in the DAG. Check your spelling and ensure that the variable is an input to a runnable."
                    assert output_variable in package_dependency_graph.nodes, f"Variable value {output_variable} not found as an output variable in the DAG. Check your spelling and ensure that the variable is an output from a runnable."
                    package_dependency_graph.add_edge(output_variable, input_variable)