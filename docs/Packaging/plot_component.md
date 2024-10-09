# PlotComponent

PlotComponents are the individual layers of a plot. They are used by Plot-type Runnables to define the appearance of the plot. Each PlotComponent has its own attributes, while the Plot itself has attributes that apply to the entire plot.

Here is a minimal working example of a PlotComponent TOML file:
```toml
# $project_folder/src/$project_name/path/to/component_name.toml
[component_name]
type = "component"
exec = "path/to/file.ext::func_name"
inputs_order = [
    "input1",
    "input2"
]
```

Note that unlike Process Runnables, the inputs are specified in a list, `inputs_order`, rather than a dictionary. This is because the actual variables being used as inputs are defined in the Plot Runnable, and the PlotComponent only needs to know the order in which they are used.

This is a limitation of TOML, as it alphabetizes the input variables in the dictionary, so the order in which they are specified in the TOML file is not preserved. To work around this, the `inputs_order` list is used to specify the order in which the variables are used in the function.

Here are the optional attributes that can be specified in the `[component_name]` table of a PlotComponent TOML file:
```toml
[component_name]
props.prop1 = "value" # Overrides the default value for the component

# Example
props.LineWidth = 2
```

The `props` dictionary is specific to the plotting function that this PlotComponent executes. To know which properties a particular plotting function accepts, refer to the documentation for that function in its package's documentation.