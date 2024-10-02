# Package Design

This is where I'll detail the high-level (and probably some lower level) implementation details. Before diving in, I want to cover some relevant terminology.

## Highest Level Summary
At the highest level, this package does the following:
### 1. Reads TOML files for a given project. 
Finds all listed dependencies recursively.
### 2. Constructs a Directional Acyclic Graph (DAG) from those TOML files
Using the data from the TOML files, a DAG is constructed that defines a data processing pipeline, where data flows from source to target nodes.