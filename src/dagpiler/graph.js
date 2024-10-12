// graph.js
document.addEventListener("DOMContentLoaded", function() {
    if (typeof cytoscape === 'undefined' || typeof cytoscapeDagre === 'undefined') {
        console.error('cytoscape or cytoscape-dagre failed to load');
        return;
    }
    
    cytoscape.use(cytoscapeDagre);

    let selectedNodes = [];
    const elements = JSON.parse(elementsJson);  // `elementsJson` will be injected from the backend
    elements.forEach(element => {
        if (element.data.label) {
            element.data.label = element.data.label.split('.').join('.\n');
        }
    });

    const cy = cytoscape({
        container: document.getElementById("cy"),
        elements: elements,
        layout: {
            name: 'dagre'
        },
        style: [
            {
                selector: 'node',
                style: {
                    'background-color': '#0074D9',
                    'label': 'data(label)',
                    'color': '#000',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'font-size': '10px',
                    'text-wrap': 'wrap',
                    'text-max-width': '80px'
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': 2,
                    'line-color': '#0074D9',
                    'target-arrow-color': '#0074D9',
                    'target-arrow-shape': 'triangle'
                }
            },
            {
                selector: '.highlighted',
                style: {
                    'background-color': 'red',
                    'line-color': 'red',
                    'target-arrow-color': 'red',
                    'transition-duration': '0.0s'
                }
            }
        ]
    });

    cy.on('tap', 'node', function(evt) {
        const node = evt.target;
        selectedNodes = [node];  // Select only one node for editing
        console.log("Node selected:", node.data());
    });

    window.openFolderPicker = function() {
        const input = document.createElement('input');
        input.type = 'file';
        input.webkitdirectory = true;
        input.onchange = (event) => {
            const folderName = event.target.files[0].webkitRelativePath.split('/')[0];
            document.getElementById("project-name").textContent = folderName;
        };
        input.click();
    }

    window.addNode = function() {
        const nodeName = prompt("Enter node name:");
        if (nodeName) {
            cy.add({ group: 'nodes', data: { id: nodeName, label: nodeName }});
        }
    }

    window.removeNode = function() {
        const selectedNode = selectedNodes[0];
        if (selectedNode) {
            cy.remove(selectedNode);
            selectedNodes = [];
        }
    }

    window.addEdge = function() {
        if (selectedNodes.length === 2) {
            const source = selectedNodes[0].id();
            const target = selectedNodes[1].id();
            cy.add({ group: 'edges', data: { source, target }});
            selectedNodes = [];
        }
    }

    window.removeEdge = function() {
        const selectedEdge = cy.$('.highlighted').filter('edge');
        if (selectedEdge.length > 0) {
            cy.remove(selectedEdge);
        }
    }

    window.editNode = function() {
        if (selectedNodes.length === 0) {
            alert("Please select a node to edit.");
            return;
        }
        const node = selectedNodes[0];
        const attributes = node.data();
        let formHtml = '<form onsubmit="return saveNodeAttributes(this, \'' + node.id() + '\')">';
        for (const [key, value] of Object.entries(attributes)) {
            if (key !== 'id' && key !== 'label') {
                formHtml += `<label>${key}: <input type='text' name='${key}' value='${value}'></label><br>`;
            }
        }
        formHtml += '<button type="submit">Save</button><button type="button" onclick="closeEditForm()">Cancel</button></form>';
        document.getElementById("edit-node-form").innerHTML = formHtml;
        document.getElementById("edit-node-form").style.display = 'block';
    }

    window.saveNodeAttributes = function(form, nodeId) {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        const node = cy.getElementById(nodeId);
        for (const [key, value] of Object.entries(data)) {
            node.data(key, value);
        }
        closeEditForm();
        return false;
    }

    window.closeEditForm = function() {
        document.getElementById("edit-node-form").style.display = 'none';
    }
});
