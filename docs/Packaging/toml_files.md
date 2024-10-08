# TOML Configuration Files

TOML (Tom's Obvious Minimal Language) is a configuration file syntax that defines a format for human and machine-readable structured plain text. I like it a lot because it's just as full featured as JSON and YAML, has multiple ways to represent the same dictionaries, unlike JSON and YAML (which I find helpful), and due to negligible indentation, TOML is a very robust and easy to work with language. Its primary downside is that it has not been around for as long as YAML or JSON, and so not every language has an existing TOML parser, and not all TOML parsers are created equal (some may not handle the more advanced features in TOML like arrays of tables).

## pyproject.toml
Python relies on pyproject.toml files to specify the metadata for publishing packages. The minimal default file structure is:
```toml
[build-system]
requires = ['hatchling']
build-backend = 'hatchling.build'

[project]
name = "package_name"
version = '0.1.0'
description = 'Package description'
authors = [{name = "Author Name", email ="author@email.com"}]
dependencies = [
    "package-dag-compiler"
]
```

## index.toml
This file points to all of the other files in the package. It can be any format, but every value must be a file path. At its simplest, it could contain just one file path:
```toml
package_file = "path/to/package_file.toml"
```
In larger packages with more files, more organization becomes useful. For example, categorizing paths by type:
```toml
processes = [
    "path/to/process1.toml",
    "path/to/process2.toml"
]
plots = [
    "path/to/plots1.toml"
]
```
### Special keys
- bridges: The files that help connect the current package to others.
```toml
runnables = [
    "path/to/runnables1.toml",
    "path/to/runnables2.toml"
]
bridges = "path/to/bridges.toml"
```

## runnables.toml
The main contents of a package reside in its 1+ runnables' .toml files, of which there are multiple types. Every type of runnable needs at minimum the following attributes: `type`, `exec`, and `inputs`.

Example runnable format:
```toml
[runnable_name]
type = "runnable_type"
exec = "path/to/file.ext:func_name"
inputs.input1 = "runnable1.variable1"
```

### Process
Process type runnables are the most frequent runnable type. They process and transform data, and are the only type that has output variables. Inputs are identified by name, similar to keyword arguments available in most languages. As there are no named outputs, output variables are specified in a list in the same order that they are output.

```toml
[runnable_name]
type = "process"
exec = "path/to/file.ext:func_name"
inputs.input1 = "runnable1.variable1"
outputs = [
    "output1",
    "output2"
]
```

### Plot
Plot type runnables are exactly what they sound like - they plot and visualize data.

```toml
[runnable_name]
type = "plot"
exec = "path/to/file.ext:func_name"
inputs.input1 = "runnable1.variable1"
```

### Summary
Summary type runnables summarize the data.

```toml
[runnable_name]
type = "summary"
exec = "path/to/file.ext:func_name"
inputs.input1 = "runnable1.variable1"
```

## bridges.toml
Bridges are the mechanism by which independently developed packages are connected together. The bridge name is just an identifier (unique within each package). Sources are the origin of the variable being bridged, and targets are where the variable is being directed to. Typically, there would either be just one source and multiple targets, or one target and multiple sources.

Most projects just need one of these bridges files, althouh multiple bridges files are supported. If you find yourself with many bridges, consider splitting the package up into smaller packages.

Here is a basic example bridges.toml file:
```toml
[bridge_name]
sources = [
    "package1.runnable1.output1"
]
targets = [
    "package2.runnable1.input1"
]
```

Note that each entry contains the package name, which is not included in the package's runnables.toml files because the referenced runnables are assumed to be located within the same package. When bridging, the package name must be specified explicitly to resolve potential naming conflicts between packages.

### One source, multiple targets
In this case, one output variable is being used as an input to multiple runnables. This is a common practice, as there are often computed variables that need to be used by multiple functions further along the pipeline.

### One target, multiple sources
In this case, one input variable is receiving data from multiple sources, triggering a polyfurcation of the DAG, with one branch per input variable. Most commonly this would happen with Plot and Summary runnables, to reuse the same runnable to plot or summarize multiple variables. 

In the below example, two variables are both being connected to the input variable for a Summary runnable.
```toml
[summaries]
sources = [
    "package1.runnable1.variable1",
    "package1.runnable2.variable1"
]
targets = [
    "package2.summary1.data"
]
```

### Multiple targets, multiple sources
!!!todo
Currently unsupported and will raise an error, though in the future I aim to support this. It will be treated as though it were a series of N bridges with one target and multiple sources, where N is the number of targets. Therefore, each source will be applied to each target