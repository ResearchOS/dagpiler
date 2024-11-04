from base_dag import DAG

from ..nodes.variables.variables import Variable
from ..nodes.variables.variable_factory import VARIABLE_FACTORY
from ..nodes.runnables.runnables import Runnable

def polyfurcate_dag(dag: DAG) -> DAG:
    """Polyfurcate the DAG as needed if multiple variables input into a single variable."""
    nodes_to_furcate = get_nodes_to_furcate(dag)
    if not nodes_to_furcate:
        return dag
    return perform_polyfurcation(dag, nodes_to_furcate)

def get_nodes_to_furcate(dag: DAG) -> list:
    """Get the nodes in the DAG that need to be furcated.
    If an input variable has more than one source, then the node needs to be furcated."""
    nodes_to_furcate = []
    # Get all the edges where the source node is a variable and the target node is a runnable
    input_variable_nodes = [edge[0] for edge in dag.edges if isinstance(edge[0], Variable) and isinstance(edge[1], Runnable)] # Includes Constants, etc.

    for target_node in input_variable_nodes:
        source_nodes = list(dag.predecessors(target_node))
        if len(source_nodes) > 1:
            nodes_to_furcate.append(target_node)
    return nodes_to_furcate

def perform_polyfurcation(dag: DAG, nodes_to_furcate: list):
    """Furcate (split) the DAG downstream from each node.
    Do this in topological order so that the furcations propagate exponentially."""
    # Turn off the singleton pattern for the Variable Factory, as multiple variables will now potentially be created with the same name.
    VARIABLE_FACTORY.toggle_singleton_off()
    for node in nodes_to_furcate:
        node_name = node.name # Until this point, node.name is guaranteed to be unique. After polyfurcation, it will not be unique.
        # Each predecessor should be linked to one copied DAG.
        predecessors = list(dag.predecessors(node)) # The multiple output variables for each of which a new DAG will be created
        assert len(predecessors) > 1, f"Node {node} has only one source. It should not be furcated."

        # Get all of the descendant nodes
        descendant_nodes = list(nx.descendants(dag, node)).append(node)        
        descendant_graph = dag.subgraph(descendant_nodes)

        # Create a new DAG for each source
        for predecessor in predecessors:
            new_dag, node_mapping = copy_dag_new_uuid(descendant_graph)

            # Add the new DAG to the overall DAG
            dag.add_nodes_from(new_dag.nodes(data=True))
            dag.add_edges_from(new_dag.edges)

            # Connect the non-furcating predecessor nodes to the new DAG
            # Get the predecessor nodes that feed into the subgraph in the original DAG.
            # Exclude nodes within the subgraph.
            non_furcate_predecessors = {}
            non_furcate_predecessors = {n:
                pred for n in descendant_graph.nodes
                for pred in dag.predecessors(n)
                if pred not in descendant_graph.nodes
            }            
            
            for pred, orig_node in non_furcate_predecessors.items():
                new_node = node_mapping[orig_node]
                dag.add_edge(pred, new_node)

            # Connect the furcating predecessor to the new DAG
            new_node = [n for n in new_dag.nodes if new_dag.nodes[n].name == node_name][0]
            dag.add_edge(predecessor, new_node)
    return dag

        
# def copy_dag_new_uuid(original_dag: DAG) -> DAG:
#     """Copy the DAG with new node UUID's, preserving (deep copying) the node data."""
#     original_edges = original_dag.edges
    
#     new_dag = DAG()

#     # Mapping from the original node UUID to the new node UUID
#     node_mapping = {node: str(uuid.uuid4()) for node in original_dag.nodes}

#     # Add nodes with new UUID's and deep copy of data
#     for old_node, new_node in node_mapping.items():
#         original_data = original_dag.nodes[old_node]['node']
#         copied_data = copy.deepcopy(original_data)
#         copied_data["id"] = new_node # Change the UUID
#         new_dag.add_node(new_node, node=copied_data)

#     # Add edges with new UUID's
#     new_dag.add_edges_from((node_mapping[u], node_mapping[v]) for u, v in original_edges)

#     return new_dag, node_mapping