# Bridging Packages
When packages are developed independently of one another, by definition they have no way of knowing what inputs or outputs the other provides. Bridging is the mechanism by which independently developed packages are connected together. The bridge name is just an identifier (unique within each package). Sources are the origin of the bridge. Any type of input variable can be entered as the source, see [Process](process.md#inputs). Targets are where the variable is being directed to. Typically, there would either be just one source and multiple targets, or one target and multiple sources.

Here is an example of a bridges.toml file:

```toml
[bridge_name]
sources = [
    "package1.runnable1.output1"
]
targets = [
    "package2.runnable1.input1"
]
```
Excerpts from package 1 and 2's runnable.toml file:
```toml
# package1/src/package1/runnable1.toml
[runnable1]
type = "process"
inputs.input1 = 5
outputs = [
    "output1"
]

# package2/src/package2/runnable1.toml
[runnable1]
type = "process"
inputs.input1 = "?"
outputs = [
    "output1"
]
```

Bridges will most typically be used to provide an input variable for a variable that is [Unspecified](process.md/#unspecified) in its own package, meaning it relies on other packages to provide that variable. However, ***any*** variable from any package can be overriden by being bridged. Other common use cases include providing non-default hard-coded values, or specifying a different file path to load a variable from.

Multiple sources leading to one target indicates that the DAG will split at that target, creating a copy of the subgraph of nodes descended from the target. This is useful when you want to run multiple processes on the same data.
```toml
[bridge_name]
sources = [
    "package1.runnable1.output1",
    "package2.runnable1.output1"
]
targets = [
    "package3.runnable1.input1"
]
```