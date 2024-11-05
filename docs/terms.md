# Glossary

#### A note on notation
Throughout the glossary and the docs, you may see notation for file and folder paths that include dollar signs `$`. Whatever comes after this symbol is intended to be a dynamic variable, e.g. `$project_folder` will be replaced with the actual folder path for your project.

## DAG
The output of this package is a Directional Acyclic Graph (DAG) consisting of nodes and edges. Nodes can be Runnables or Variables, and edges are the connections between nodes. 

## index.toml
Recommended to be located at `$project_folder/src/$project_name/index.toml`. This file contains all of the file paths to all of the files that comprise this package. For maximum flexibility, the only requirement as to the structure of this file is that it consist only of dictionaries (with any degree of nesting for organizational purposes), where each key is a user-defined string, and the values are either a subdictionary, or a file path. No other strings, no numbers, or lists are allowed outside of dictionaries. Relative file paths are preferred for portability. They are relative to the `$project_folder/src/$project_name` directory, as that is the root directory when the package is installed. Absolute file paths should be used only when needed to access files outside of the project folder.

## pyproject.toml
Recommended to be located at the root of your project folder, `pyproject.toml` is a type of text file that is [Python's default way of providing the metadata needed to share Python packages](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/). This is the only Python-standard .toml file, the rest are custom-defined in this package for the purposes of compiling a DAG from a TOML-based modular package format.

## Variable
Variables are defined within the Runnables where they are used, they do not have their own sections of a TOML file. Variables can be specified as inputs or outputs, and are the primary way that data flows between Runnables.

A Variable node in the DAG is an input Variable if its successor is a Runnable, and an output Variable if its predecessor is a Runnable. Input Variables can be any of several types: hard-coded, loading a file, specifying a data object's name or file path, or even unspecified. Output variables do not have these delineations - they are all simply "outputs".

## Runnable
"Runnable" is an umbrella term for any node type that is not a Variable, and executes code. The default Runnable types are Process, Plot, PlotComponent, and Summary (in development). There are different types of Runnables because they each require different attributes to function, though some attributes are mandatory and shared between all Runnable types.

### Runnable: Process
The most common type of Runnable. Takes in data, processes it by executing the associated code, and outputs data.

### Runnable: Plot
Runnable that visualizes data. Takes in data and metadata about the Plot, Axes, and PlotComponent to construct and save the plot. 

!!!info
    Plots themselves do not have code associated with them, and so do not have an `exec`property. However, PlotComponents do.

### Runnable: PlotComponent
!!!todo
Used by Plot-type Runnables to define a single layer of the plot. Executes the plotting functions, while Plot Runnables themselves do not.

### Runnable: Summary
!!!todo
Responsible for summarizing the data so it can be entered into statistical analysis.

## Bridges
The mechanism to connect Runnables in different packages. Using similar syntax as in the package's TOML files, the separation of the bridge file allows for the separation of concerns between the package's internal structure and its external connections. This means that a package can be written to reference variables from other packages without knowing anything about those other packages. For more information, see the [Bridging](Packaging/bridging_packages.md) page.