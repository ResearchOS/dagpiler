import datetime
import os
import toml
import json
import yaml

from base_dag import DAG

from ..dag.organizer import order_nodes, order_edges, get_dag_of_runnables
from ..nodes.node import NodeFactory

def print_dag(dag: DAG, path: str = "dag.json") -> None:
    """Print the DAG in a human-readable format."""    
    if path != "stdout" and not os.path.exists(os.path.dirname(path)):
        raise FileNotFoundError(f"Directory {os.path.dirname(path)} does not exist.")
    
    dag_writer = DAG_WRITER_FACTORY.create(path.split(".")[-1])
    dag_writer.write(dag, path)

class DagWriter:
    def write(self, dag: DAG, path: str) -> None:
        raise NotImplementedError

class DagWriterFactory:
    def __init__(self):
        self._writers = {}
    
    def register(self, format: str, writer: DagWriter):
        self._writers[format] = writer
    
    def create(self, format: str) -> DagWriter:
        writer = self._writers.get(format)
        if not writer:
            raise ValueError(format)
        return writer
    
DAG_WRITER_FACTORY = DagWriterFactory()

def register_writer(format: str):
    def decorator(cls):
        DAG_WRITER_FACTORY.register(format, cls)
        return cls
    return decorator

@register_writer("stdout")
class StdoutDagWriter(DagWriter):
    """Write the DAG to stdout (default)"""    
    def write(self, dag: DAG, path: str) -> None:
        dag_dict = {}
        dag_dict["nodes"] = [str(node) for node in order_nodes(dag)]
        dag_dict["edges"] = [f"{str(edge[0])} -> {str(edge[1])}" for edge in order_edges(dag)]
        print("DAG:")
        print("nodes")
        for count, node in enumerate(dag_dict["nodes"]):
            print(f"{count}: {node}")
        print("edges")
        for count, edge in enumerate(dag_dict["edges"]):
            print(f"{count}: {edge}")

@register_writer("toml")    
class TomlDagWriter(DagWriter):
    """Write the DAG to a TOML file."""
    def write(self, dag: DAG, path: str) -> None:
        dag_dict = {}
        dag_dict["nodes"] = [str(node) for node in order_nodes(dag)]
        dag_dict["edges"] = [f"{str(edge[0])} -> {str(edge[1])}" for edge in order_edges(dag)]
        
        if not os.path.exists(os.path.dirname(path)):
            raise FileNotFoundError(f"Directory {os.path.dirname(path)} does not exist.")
                
        pretty_string = self.pretty_format_toml(dag_dict)
        with open(path, "w") as f:        
            f.write(pretty_string)

    def pretty_format_toml(self, dag_dict: dict) -> str:
        """Pretty format the TOML string."""
        # Replace the list brackets with newlines
        result = []
        result.append("nodes = [\n")
        result.append("\n".join([f"""    "{node}",""" for node in dag_dict["nodes"]]))
        result.append("\n]\n\n")
        result.append("edges = [\n")
        result.append("\n".join([f"""    "{edge}",""" for edge in dag_dict["edges"]]))
        result.append("\n]\n")
        return "".join(result)

@register_writer("json")
class JsonDagWriter(DagWriter):
    """Write the DAG to JSON file."""
    def write(self, dag: DAG, path: str) -> None:
        with open(path, "w") as f:
            json.dump(self.graph_to_json(dag), f)

    def graph_to_json(self, dag: DAG) -> str:
        """Convert the DAG to a JSON string."""
        # Prepare a dictionary to hold the graph data
        graph_dict = {
            "nodes": [],
            "edges": []
        }
        
        # Iterate over the nodes and use the to_dict() method for serialization
        for node in dag.nodes:
            node_data = dag.nodes[node]
            node_dict = node_data.to_dict()  # Use the to_dict method to convert to dict
            node_dict['id'] = node  # Include node identifier if necessary
            graph_dict["nodes"].append(node_dict)

        # Iterate over the edges and store them as pairs (source, target)
        for source, target in dag.edges:
            graph_dict["edges"].append({"source": source, "target": target})

        # Convert the graph dictionary to JSON
        return json.dumps(graph_dict, indent=2)
    
@register_writer("yaml")
class YamlDagWriter(DagWriter):
    def write(self, dag: DAG, path: str) -> None:
        raise NotImplementedError

def json_to_dag(json_dag: dict) -> DAG:
    """Convert the saved JSON back to a DAG."""
    data = json.loads(json_dag)
    dag = DAG()

    # Add the nodes to the graph using the RunnableFactory
    for node_data in data["nodes"]:
        node = NodeFactory.create_node(node_data)
        dag.add_node(node)

    # Add the edges to the graph
    for edge in data["edges"]:
        source = NodeFactory.create_node(edge["source"])
        target = NodeFactory.create_node(edge["target"])
        dag.add_edge(source, target)

    return dag

def save_dag(dag: DAG, file_path: str = None):
    if file_path is None:
        file_path = os.path.join(os.getcwd(), ".dagpiler", f"{datetime.datetime.now()}_dag.json")

    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    dagwriter = DAG_WRITER_FACTORY.create(file_path.split(".")[-1])
    dagwriter.write(dag, file_path)

def load_dag(file_path: str) -> DAG:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist.")
    
    with open(file_path, "r") as f:
        return json_to_dag(f.read())