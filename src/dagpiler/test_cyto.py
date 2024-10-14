import json
from fasthtml.common import *
from starlette.staticfiles import StaticFiles

app = FastHTML()

# Route to render the graph
@app.get("/")
async def display_graph():
    return Div(
            # Load necessary scripts for Cytoscape and Dagre        
            Script(src="https://unpkg.com/cytoscape@3.23.0/dist/cytoscape.min.js"),
            Script(src="https://unpkg.com/dagre@0.8.5/dist/dagre.min.js"),
            Script(src="https://unpkg.com/cytoscape-dagre@2.5.0/cytoscape-dagre.js"),
            Script(src="src/dagpiler/graph.js"),    
    )

# Run the Application
if __name__ == "__main__":
    from uvicorn import run
    app.mount('/src/dagpiler', StaticFiles(directory='src/dagpiler'), name='dagpiler')
    run(app, host="127.0.0.1", port=8000)