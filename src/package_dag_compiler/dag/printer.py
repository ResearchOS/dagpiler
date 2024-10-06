import os
import toml

import networkx as nx

from dag.organizer import order_nodes, order_edges

def print_dag(dag: nx.MultiDiGraph, path: str = None) -> None:
    """Print the DAG in a human-readable format."""
    dag_dict = {}
    dag_dict["nodes"] = [str(node) for node in order_nodes(dag)]
    dag_dict["edges"] = [f"{str(edge[0])} -> {str(edge[1])}" for edge in order_edges(dag)]

    if not path:
        print("DAG:")
        print("nodes")
        for count, node in enumerate(dag_dict["nodes"]):
            print(f"{count}: {node}")
        print("edges")
        for count, edge in enumerate(dag_dict["edges"]):
            print(f"{count}: {edge}")
        # print(toml.dumps(dag_dict))
        return
    
    if not os.path.exists(os.path.dirname(path)):
        raise FileNotFoundError(f"Directory {os.path.dirname(path)} does not exist.")
    
    raw_string = toml.dumps(dag_dict)
    pretty_string = pretty_format_toml(dag_dict)
    with open(path, "w") as f:        
        f.write(pretty_string)

def pretty_format_toml(dag_dict: dict) -> str:
    """Pretty format the TOML string."""
    # Replace the list brackets with newlines
    result = []
    result.append("nodes = [\n")
    result.append("\n".join([f"    '{node}'," for node in dag_dict["nodes"]]))
    result.append("\n]\n")
    result.append("edges = [\n")
    result.append("\n".join([f"    '{edge}'," for edge in dag_dict["edges"]]))
    result.append("\n]\n")
    return "".join(result)
