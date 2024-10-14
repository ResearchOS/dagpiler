import json
from fasthtml.common import *
from starlette.staticfiles import StaticFiles

from core import compile_dag
from dag.organizer import get_dag_of_runnables

app = FastHTML()

# Initialize your directed graph
G = compile_dag("frame_range_no_nan")
G = get_dag_of_runnables(G)

# Convert the nodes and edges from the graph into Cytoscape.js format
def graph_to_cytoscape_elements(graph):
    elements = []

    for node in graph.nodes(data=False):
        node_dict = node.to_dict()
        node_data = {"id": node_dict.pop("name")}
        node_data.update(node_dict)  # Add remaining attributes to the node data
        elements.append({"data": node_data})

    for source, target in graph.edges():
        elements.append({"data": {"id": source.name + "_" + target.name, "source": source.name, "target": target.name}})
    
    return elements

@app.post("/save_graph")
async def save_graph():
    print("Graph saved successfully.")
    return "Graph saved successfully."

# Route to render the graph
@app.get("/")
async def display_graph():
    elements_json = json.dumps(graph_to_cytoscape_elements(G))

    return Div(
        # Load necessary scripts for Cytoscape and Dagre        
        Script(src="https://unpkg.com/cytoscape@3.23.0/dist/cytoscape.min.js"),
        Script(src="https://unpkg.com/dagre@0.8.5/dist/dagre.min.js"),
        Script(src="https://unpkg.com/cytoscape-dagre@2.5.0/cytoscape-dagre.js"),      
        Script(f"const elementsJson = {elements_json};", type="text/javascript"),              
        H1("Graph Visualization",
            Span("Choose Project", id="project-name", style="margin-left: 20px;"),
            Button("Browse", _onclick="openFolderPicker()", style="margin-left: 10px;")
        ), 
        Div(
            Button("Add Node", _onclick="addNode()"),
            Button("Remove Node", _onclick="removeNode()"),
            Button("Add Edge", _onclick="addEdge()"),
            Button("Remove Edge", _onclick="removeEdge()"),
            Button("Edit Node", _onclick="editNode()"),  # New "Edit Node" button
            Button("Save", _onclick="saveGraph()")
        ),
        Div(id="cy", style="width: 100vw; height: 70vh; border: 1px solid #ccc; background-color: #f0f0f0;"),
        Div(id="edit-node-form", style="display: none;"),  # Hidden div for the edit form popup 
        Script(src="src/dagpiler/graph.js"),         
    )

# Run the Application
if __name__ == "__main__":
    from uvicorn import run
    app.mount('/src/dagpiler', StaticFiles(directory='src/dagpiler'), name='dagpiler')
    run(app, host="127.0.0.1", port=8000)
