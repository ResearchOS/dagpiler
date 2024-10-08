# Package-DAG-Compiler

The Directional Acyclic Graph (DAG) is a data structure (a type of Graph) that at its most fundamental level consists of nodes and directed (Directional) edges, and does not contain any loops (Acyclic). Typically, nodes are objects, and directed edges are the directional relationships between them, such as `gas -> car` indicating that the car depends on gas. It is the same in this package. Typically, edges are notated using some variant of `source -> target` (equivalently, `(source, target)`), which can be read in one of two ways:

1. The target depends on the source.
2. The source feeds in to the target.

The second, more source-centric interpretation guides the design philosophy of this package. In the context of a workflow orchestration tool, where data flows from a dataset to a final output, I think this makes more sense. In the DAG, nodes are Runnable functions and the edges are the Variables' data flowing between them, the edges look more like `Runnable -> Variable` which can be read as "data from this Runnable node flows into this output Variable". Similarly, `Variable -> Runnable` indicates that data flows from a Variable and is an input to a Runnable.

In this package, edges carry no meaning or metadata, they simply define directional connectivity. All of the metadata is contained in the node properties.

At a high level, there are two types of nodes: Runnables, and Variables. Runnables represent things that you run, generally a function that you can call or a script you can run. Categories of Runnables include Process, Stats, and Plot. More on those later. The other node type is Variables, which as you would expect help direct the flow of data. Runnable nodes can only directly connect to Variables, they cannot connect to each other directly. However, Variable nodes can connect to either a Runnable or another Variable. The edges between nodes, whether they be Runnable -> Variable, Variable -> Runnable, or Variable - Variable, represent the flow of data between steps in a data processing pipeline. There can only be one connection between an output variable node and an input variable node without triggering a split in the DAG. A split is exactly what it sounds like. An exact copy of the subgraph of nodes descended from the current  Runnable node is created, and attached to that same Runnable node.

Further Reading:
1. Recommended package directory structure
    - Can use a template to generate the TOML files and directory structure
3. How to use this package
    - Example project
    - Templates
    - Documentation per function
    - Output is NetworkX graph