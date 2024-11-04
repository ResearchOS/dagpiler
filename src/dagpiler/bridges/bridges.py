
from base_dag import DAG

from ..nodes.variables.variable_factory import VARIABLE_FACTORY, get_variable_type

def add_bridges_to_dag(package_name: str, package_bridges_dict: dict, dag: DAG, processed_packages: dict) -> None:
    """Add package dependencies to the package dependency graph."""
    from ..read_and_compile_dag import process_package, get_package_name_from_runnable

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
                if source == target:
                    raise ValueError(f"Source and target are the same: {source}")
                
                target_package = get_package_name_from_runnable(target)
                                     
                # Recursively process target and source packages if not already done
                if target_package not in processed_packages:
                    process_package(target_package, processed_packages, dag)
                if source_package not in processed_packages:
                    process_package(source_package, processed_packages, dag)

                # Add edge from source to target (if both dynamic)
                # OR if source is hard-coded and target is dynamic, then don't add an edge
                # Either way, need to convert unspecified to another variable type.

                # Get the variable type for the source variable
                source_variable_type = get_variable_type(source)
                if source_variable_type == "output":
                     # Create output variable
                    output_variable = VARIABLE_FACTORY.create_variable(source)
                else:
                    output_variable = None

                previous_input_variable = [v for v in dag.nodes if v.name == target]
                if not previous_input_variable:
                    raise ValueError(f"No input variable found for target {target}")
                previous_input_variable = previous_input_variable[0]                

                converted_input_variable = VARIABLE_FACTORY.convert_variable(previous_input_variable, source)                
                # Replace references to the previous variable in each successor runnable's inputs
                successor_runnables = list(dag.successors(previous_input_variable))
                for runnable in successor_runnables:
                    if hasattr(runnable, 'inputs') and previous_input_variable in runnable.inputs.values():
                        # Replace old variable with new variable in inputs
                        for key, value in runnable.inputs.items():
                            if value == previous_input_variable:
                                runnable.inputs[key] = converted_input_variable
                mapping = {previous_input_variable: converted_input_variable}
                dag = dag.relabel_nodes(mapping)

                # Add edge from source to target
                if output_variable is not None:
                    dag.add_edge(output_variable, converted_input_variable)