
import networkx as nx


def order_nodes(dag: nx.MultiDiGraph):
    """Order the nodes in the DAG. Within each topological generation, order by the node name."""
    sorted_nodes = []
    
    # Step 1: Get nodes by topological generations
    for generation in nx.topological_generations(dag):
        # Step 2: Sort nodes alphabetically by 'name' attribute within each generation
        generation_sorted = sorted(generation, key=lambda n: dag.nodes[n].get('name', ''))
        sorted_nodes.extend(generation_sorted)
    
    return sorted_nodes

def order_edges(dag: nx.MultiDiGraph):
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