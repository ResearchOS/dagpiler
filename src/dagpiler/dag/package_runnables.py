from base_dag import DAG

from ..nodes.runnables.runnables import initialize_variables
from ..nodes.runnables.runnable_factory import RUNNABLE_FACTORY
from ..nodes.variables.variable_factory import VARIABLE_FACTORY

def add_package_runnables_to_dag(package_name: str, package_runnables_dict: dict, dag: DAG) -> None:
    """Add package runnables to the DAG."""
    runnable_nodes = []
    for runnable_name, runnable in package_runnables_dict.items():        
        # Convert the runnable to a node in the DAG
        runnable_name = ".".join([package_name, runnable_name]) # Set the name of the runnable
        runnable["name"] = runnable_name
        if "type" not in runnable:
            raise ValueError(f"""Missing "type" attribute in runnable {runnable_name}""")
        runnable_node = RUNNABLE_FACTORY.create_runnable(runnable)
        # Create separate Variable nodes for each input and output
        initialize_variables(runnable_node)
        runnable_nodes.append(runnable_node) # For connecting the variables later
        
        # Add the runnable to the DAG
        dag.add_node(runnable_node)

        # Add the inputs and outputs as edges to the DAG
        if hasattr(runnable_node, "inputs"):
            for input_var in runnable_node.inputs.values():
                dag.add_node(input_var)
                dag.add_edge(input_var, runnable_node)

        if hasattr(runnable_node, "outputs"):
            for output_var in runnable_node.outputs.values():
                dag.add_node(output_var)
                dag.add_edge(runnable_node, output_var) 
        
    # Connect the variables to one another
    for runnable_node in runnable_nodes:
        if not hasattr(runnable_node, "inputs"):
            continue
        for input_var in runnable_node.inputs.values():
            if input_var.__class__.__name__ != "DynamicVariable":
                continue # Skip everything that's not a dynamic variable

            # Ensure that the value_for_hashing has any slicing removed, and the full variable name is used to match the output variable
            output_var = VARIABLE_FACTORY.create_variable(runnable_node.value_for_hashing)
            assert output_var in dag.nodes, f"Variable value {output_var} from {input_var} not found as an output variable in the DAG. Check your spelling and ensure that the variable is an output from a runnable."
            dag.add_edge(output_var, input_var)
