# TOML Configuration Files

TOML ([Tom's Obvious Minimal Language](https://toml.io/en/v1.0.0)) is a configuration file syntax that defines a format for human and machine-readable structured plain text. I selected it for this project because it's just as full featured as JSON and YAML, and has multiple ways to represent the same dictionaries, unlike JSON and YAML (which I find helpful). Due to negligible indentation, TOML is very robust and easy to work with. Its primary downside is that it has not been around for as long as YAML or JSON, and so not every language has an existing TOML parser (though Python, MATLAB, and R all do). I take care to keep the TOML files in this package as simple as possible, and to avoid using any advanced features, though this may occasionally lead to some repetition.

!!!tip
    This page is focused on how to write and use the TOML files. For a more high-level introduction to the concepts on this page, check out the [Glossary](../terms.md).

## pyproject.toml
Python relies on pyproject.toml files to specify the metadata for publishing packages (see [Python docs](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) for details). For use with the `dagpiler` package, a minimal default file structure is provided below. The contents of this file are created when you run `dagpiler init` in a new project folder.
```toml
# $project_folder/pyproject.toml
[build-system]
requires = ['hatchling']
build-backend = 'hatchling.build'

[project]
name = "your_package_name"
version = '0.1.0'
description = 'Your package description'
authors = [{name = "Author Name", email ="author@email.com"}]
dependencies = [
    "dagpiler"
]
```

## index.toml
This file specifies the paths to all of the other files in the package. For your package to work, this file must be located at `$project_folder/src/$project_name/index.toml`. It can contain arbitrarily nested dictionaries, but every value must be a file path or list of file paths. **Relative file paths are preferred for portability.** The root directory for the relative file paths is the directory containing the index.toml file, `$project_folder/src/$project_name`, as that is the root directory when the package is installed via `pip`.

!!!tip
    The index.toml file is the only file that is required to be in a specific location. The rest of the files can be located anywhere as long as the paths are correctly specified in the index.toml file.
!!!tip
    Try to keep all of the package's files within the `$project_folder/src/$project_name` directory so that `index.toml` can reference them using relative paths. Use absolute paths to files outside of this folderonly when necessary, as this is not portable.

### Examples
The simplest `index.toml` files are just one key-value pair, where the key can be any string and the value is a file path. For example:
```toml
# $project_folder/src/$project_name/index.toml
package_file = "path/to/package_file.toml"
```
In larger packages with more files, more organization becomes useful. For example, categorizing paths by type:
```toml
# $project_folder/src/$project_name/index.toml
processes = [
    "path/to/process1.toml",
    "path/to/process2.toml"
]
plots = [
    "path/to/plots1.toml"
]
```
### Special keys
bridges: The files that connect the current package to other packages. It is a file path or list of file paths.
```toml
# $project_folder/src/$project_name/index.toml
runnables = [
    "path/to/runnables1.toml",
    "path/to/runnables2.toml"
]
bridges = "path/to/bridges.toml"
```

## runnables.toml
The main contents of a package reside in its 1+ runnables' .toml files, of which there are multiple types. Every type of runnable needs to specify a `type` attribute, and most will have `inputs` and/or `outputs`. Any custom attributes that the user provides in addition to the built-in ones are stored in the nodes, but are not used by the compiler.

Below are outlines of the different types of builtin Runnable types. For more information on a specific type, see that Runnable's page.

### Process
Process type runnables are the most frequent runnable type. They process and transform data, and are the only Runnable type that has output variables. Inputs are identified by name, similar to keyword arguments available in most languages. As multiple outputs are typically identified by their ordering, output variables are specified in a list (in the same order that they are output).

```toml
[runnable_name]
type = "process"
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
inputs.input1 = "runnable1.variable1"
```

### Summary
Summary type runnables summarize the data.

```toml
[runnable_name]
type = "summary"
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
In this case, one input variable is receiving data from multiple sources, triggering a polyfurcation of the DAG, with one branch per input variable. Most commonly this would happen with Plot and Summary runnables, to reuse the same runnable to plot or summarize multiple variables, though it is used with Process runnables as well.

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