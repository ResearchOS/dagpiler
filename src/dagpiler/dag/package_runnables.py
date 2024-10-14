import networkx as nx

from ..runnables.runnables import RUNNABLE_FACTORY
from ..variables.variables import VARIABLE_FACTORY

def add_package_runnables_to_dag(package_name: str, package_runnables_dict: dict, dag: nx.MultiDiGraph) -> None:
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
        runnable_node.initialize_variables()
        runnable_nodes.append(runnable_node) # For connecting the variables later
        
        # Add the runnable to the DAG
        dag.add_node(runnable_node)

        # Add the inputs and outputs as edges to the DAG
        if "inputs" in runnable_node.__dict__:
            for input_var in runnable_node.inputs.values():
                dag.add_node(input_var)
                dag.add_edge(input_var, runnable_node)
                if not nx.is_directed_acyclic_graph(dag):
                    raise ValueError(f"Adding edge {input_var} -> {runnable_node} would create a cycle in the DAG.")

        if "outputs" in runnable_node.__dict__:
            for output_var in runnable_node.outputs.values():
                dag.add_node(output_var)
                dag.add_edge(runnable_node, output_var)      
                if not nx.is_directed_acyclic_graph(dag):
                    raise ValueError(f"Adding edge {runnable_node} -> {output_var} would create a cycle in the DAG.")  

        
    # Connect the variables to one another
    for runnable_node in runnable_nodes:
        if "inputs" not in runnable_node.__dict__:
            continue
        for input_var in runnable_node.inputs.values():
            if runnable_node.__class__.__name__ != "DynamicVariable":
                continue # Skip everything that's not a dynamic variable

            # Ensure that the value_for_hashing has any slicing removed, and the full variable name is used to match the output variable
            output_var = VARIABLE_FACTORY.create_variable(runnable_node.value_for_hashing)
            assert output_var in dag.nodes, f"Variable value {output_var} from {input_var} not found as an output variable in the DAG. Check your spelling and ensure that the variable is an output from a runnable."
            dag.add_edge(output_var, input_var)
            if not nx.is_directed_acyclic_graph(dag):
                raise ValueError(f"Adding edge {output_var} -> {input_var} would create a cycle in the DAG.")
