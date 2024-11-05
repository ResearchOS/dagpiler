from collections import defaultdict
from copy import deepcopy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from networkx import MultiDiGraph as DAG

try:
    import networkx as nx
except:
    pass

from base_dag import DAG

from ..nodes.variables.variables import Variable, OutputVariable, DynamicVariable, HardcodedVariable, UnspecifiedVariable, LoadFromFile, DataObjectFilePath, DataObjectName
from ..nodes.runnables.process import Process
from ..nodes.runnables.plot import Plot
from ..dag.organizer import order_nodes, get_dag_of_runnables

colors_dict = {
    HardcodedVariable: 'blue',
    LoadFromFile: 'blue',
    DataObjectFilePath: 'blue',
    DataObjectName: 'blue',
    DynamicVariable: 'green',
    OutputVariable: 'red',
    UnspecifiedVariable: 'yellow',    
    Process: 'purple',
    Plot: 'purple'   
}

def get_layers(graph: DAG):
    layers = defaultdict(list)
    for node in nx.topological_sort(graph):
        layer = 0
        for predecessor in graph.predecessors(node):
            layer = max(layer, layers[predecessor] + 1)  # Determine the layer of the node
        layers[node] = layer
    # Invert the layers dictionary to get nodes per layer
    layers_by_generation = defaultdict(list)
    for node, layer in layers.items():
        layers_by_generation[layer].append(node)
    return layers_by_generation

def plot_dag(dag: DAG, layout: str = 'generation'):  
    import matplotlib.pyplot as plt      
    nodes_with_labels = {node: node.name for node in dag.nodes(data=False)}    
    nodes_with_labels = {k: v.replace('.', '.\n') for k, v in nodes_with_labels.items()}
    layers = get_layers(dag)
    # Assign positions based on layers    
    layer_height = 1.0  # Vertical space between layers
    layer_width = 1.0   # Horizontal space between nodes in the same layer

    if layout == 'generation':
        pos = set_generational_layout(dag, layers, layer_width, layer_height)
    else:
        pos = set_topological_layout(dag, layer_width, layer_height)

    node_colors = [colors_dict.get(node.__class__, 'black') for node in dag.nodes]

    # Strip package and function names on variables to make the graph more readable
    for node in nodes_with_labels:        
        if issubclass(node.__class__, Variable):
            nodes_with_labels[node] = node.name.split('.')[-1]

    nx.draw(dag, pos, with_labels=False, labels=nodes_with_labels, node_color=node_colors, edge_color='grey')
    nx.draw_networkx_labels(dag, pos, nodes_with_labels, font_size=8)
    plt.show()

def set_topological_layout(dag: DAG, layer_width: float, layer_height: float):
    """Left to right layout"""
    runnables_dag = get_dag_of_runnables(dag)   
    sorted_runnable_nodes = order_nodes(runnables_dag)

    pos = {}    
    for i, node in enumerate(sorted_runnable_nodes):
        pos[node] = (3 * i * layer_width, 0) # Times 3 because inputs and outputs need to go between function nodes.

        inputs = list(dag.predecessors(node))
        input_step = layer_height / (len(inputs) - 1) if len(inputs) > 1 else 0
        input_offsets = [-layer_height/2 + k * input_step for k in range(len(inputs))]          
        outputs = list(dag.successors(node))
        output_step = layer_height / (len(outputs) - 1) if len(outputs) > 1 else 0
        output_offsets = [-layer_height/2 + k * output_step for k in range(len(outputs))]
        for j, input_node in enumerate(inputs):            
            pos[input_node] = (pos[node][0] - 1, input_offsets[j])
        for j, output_node in enumerate(outputs):
            pos[output_node] = (pos[node][0] + 1, output_offsets[j])

    # label_pos = deepcopy(pos)
    return pos

def set_generational_layout(dag: DAG, layers: list, layer_width: float, layer_height: float):
    """Top to bottom layout"""
    # Move constants to the layer below the lowest layer of their successors
    pos = {}
    first_layer = deepcopy(layers[0])
    for node in first_layer:
        if not isinstance(dag.nodes[node], (LoadFromFile, HardcodedVariable, DataObjectFilePath, DataObjectName, UnspecifiedVariable)):
            continue
        min_layer = len(layers)
        successors = list(dag.successors(node))            
        for successor in successors:
            for layer_num, layer in enumerate(layers):
                if successor in layers[layer_num]:
                    min_layer = min(min_layer, layer_num)
                    break
        layers[0].remove(node)
        layers[min_layer-1].append(node)        

    for layer, nodes in layers.items():
        for i, node in enumerate(nodes):
            pos[node] = (i * layer_width, -layer * layer_height)

    return pos