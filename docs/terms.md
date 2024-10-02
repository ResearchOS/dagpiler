# Dictionary

Throughout the dictionary and the docs, you'll see notation for file and folder paths that may include dollar signs `$`. Whatever comes after this symbol is intended to be a dynamic variable, e.g. `$project_folder` will be replaced with the actual folder path for your project.

### DAG
A Directional Acyclic Graph (DAG) consisting of nodes and edges. Nodes can be Runnables or Variables, and edges represent the connections between nodes.

### index.toml
Recommended to be located at `$project_folder/src/$project_name/index.toml`. This file contains all of the file paths to all of the files that comprise this package. For maximum flexibility, the only requirement as to the structure of this file is that it consist only of dictionaries with any degree of nesting, where each key is whatever string the user wants, and the values are either a subdictionary, or an absolute file path. No relative file paths or other strings, no numbers, or lists are allowed outside of dictionaries.

### pyproject.toml
Recommended to be located at the root of your project folder, `pyproject.toml` is a type of text file that is Python's default way of providing the metadata needed to share Python packages. This is the only Python-standard .toml file, the rest are defined by me for the purposes of compiling a DAG from a TOML-based modular package format.

### Runnable

### Variable

### Runnable: Process

### Runnable: Plot

### Runnable: Stats