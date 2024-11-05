# Commands

### compile
```bash
dagpiler compile <package_name> <output_path>
```
Compile the DAG for the specified package (which must be installed in the current folder's `/.venv` virtual environment), returning a DAG object. 

Called with only the `package_name` argument at the command line, it will just print the number of nodes and edges in the compiled DAG. Providing the `output_path` saves the compiled DAG to the TOML or JSON file specified.
```python
import dagpiler
dag = dagpiler.compile_dag(package_name, "path/to/save/dag.json")
```
!!!warning
    Representing DAG nodes as dicts requires multiple layers of nesting, which TOML is not well suited for as it becomes quite redundant and verbose. Therefore, the JSON format is currently the only format that `dagpiler` can load and save all DAG attributes to, bidirectionally. The TOML format prints only the node names and edge connections, and is intended to provide a high-level overview of the DAG structure.
### plot_dag
```bash
dagpiler plot_dag <layout>
```
Compile and visualize the DAG as a matplotlib plot. Default layout is "generation", which puts all nodes of the same generation on the same level (top to bottom). The other option is "topological", which arranges the nodes in topologically sorted order from left to right. For simple graphs, these two layouts may appear similar.
```python
import dagpiler
dag = dagpiler.compile_dag(package_name)
dagpiler.plot_dag(dag, layout)
```

### print_dag
```bash
dagpiler print_dag <output_path>
```
Compile and save the DAG to a formatted TOML file. The goal is for this file to be human-readable and easily editable, and to be useable as input to the `dagpiler compile_dag` command to reconstruct the graph.
```python
import dagpiler
dag = dagpiler.compile_dag(package_name)
dagpiler.print_dag(dag, output_path)
```