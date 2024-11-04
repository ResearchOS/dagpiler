
from base_dag import DAG

from ..nodes.runnables.runnables import Runnable


def order_nodes(dag: DAG):
    """Order the nodes in the DAG. Within each topological generation, order by the node name."""
    sorted_nodes = []
    
    # Step 1: Get nodes by topological generations
    for generation in nx.topological_generations(dag):
        # Step 2: Sort nodes alphabetically by 'name' attribute within each generation
        generation_sorted = sorted(generation, key=lambda n: dag.nodes[n].get('name', ''))
        sorted_nodes.extend(generation_sorted)
    
    return sorted_nodes

def order_edges(dag: DAG):
    """Order the edges in the DAG. Within each topological generation, order by the edge name."""
    sorted_nodes = order_nodes(dag)

    sorted_edges = []
    for node in sorted_nodes:
        # Get the edges that have this node as the source
        edges = dag.edges(node, data=True)
        # Sort the edges alphabetically by the 'name' attribute of the target node
        edges_sorted = sorted(edges, key=lambda e: dag.nodes[e[1]].get('name', ''))
        sorted_edges.extend(edges_sorted)
    
    return sorted_edges

def get_dag_of_runnables(dag: DAG) -> DAG:
    """Given a DAG with variables & Runnables, return a DAG with only Runnable nodes.
    This DAG has the advantage of being able to topologically sort the Runnable nodes."""
    # Get the transitive closure
    trans_clos_dag = nx.transitive_closure_dag(dag)
    runnable_nodes = [node for node in dag.nodes if issubclass(node.__class__, Runnable)]
    runnable_dag = trans_clos_dag.subgraph(runnable_nodes).copy()
    
    # Get the edges to remove between Runnable nodes that are not neighbors
    edges_to_remove = []
    for edge in runnable_dag.edges(data=False):
        source_node, target_node = edge[0], edge[1]
        prev_path_length = nx.shortest_path_length(dag, source_node, target_node)
        if prev_path_length > 3:
            edges_to_remove.append((source_node, target_node))
    runnable_dag.remove_edges_from(edges_to_remove)
    
    return runnable_dag