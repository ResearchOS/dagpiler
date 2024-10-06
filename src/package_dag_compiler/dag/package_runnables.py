import networkx as nx

from runnables.runnables import RUNNABLE_FACTORY

def add_package_runnables_to_dag(package_name: str, package_runnables_dict: dict, dag: nx.MultiDiGraph) -> None:
    """Add package runnables to the DAG."""
    for runnable_name, runnable in package_runnables_dict.items():        
        # Convert the runnable to a node in the DAG
        runnable_name = ".".join([package_name, runnable_name]) # Set the name of the runnable
        runnable["name"] = runnable_name
        if "type" not in runnable:
            raise ValueError(f"""Missing "type" attribute in runnable {runnable_name}""")
        runnable_node = RUNNABLE_FACTORY.create_runnable(runnable)
        # Create separate Variable nodes for each input and output
        runnable_node.initialize_variables()
        
        # Add the runnable to the DAG
        dag.add_node(runnable_node)

        # Add the inputs and outputs as edges to the DAG
        for input_var in runnable_node.inputs.values():
            dag.add_node(input_var)
            dag.add_edge(input_var, runnable_node)

        for output_var in runnable_node.outputs.values():
            dag.add_node(output_var)
            dag.add_edge(runnable_node, output_var)