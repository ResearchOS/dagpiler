# Plot

Unlike Processes, where all of the attributes were used in every Process, Plot Runnables have many attributes, some of which are not required for every Plot, depending on the type of plot you are creating.

Plots also consist of one or more axes, and each axes consists of one or more PlotComponents, which are the individual layers of the plot. Each PlotComponent has its own attributes, while the Plot itself has attributes that apply to the entire plot.

## Plot Attributes

### Required
Every plot must specify at least its type and one axes, and one component in that axes.
```toml
[plot_name]
type = "plot"

[plot_names.axes.axes_name]
component_order = [
    "component_name"
]

[plot_names.axes.axes_name.components.component_name]
path = "path/to/component_name.toml"
inputs.input1 = "runnable1.variable1"
props.prop1 = "value" # Overrides the default value for the component
```

### Optional
Below is all of the optional attributes that can be specified in the `[plot_name]` table of a Plot Runnable.

```toml
[plot_name]
size = [width, height] # The size of the plot in inches
plot_backend = "matlab" # The plotting backend to use (default is "matlab")

# If a movie is being plotted
movie.frames.start = 0 # The first index in the variable to plot
movie.frames.end = 10 # The last index in the variable to plot
movie.frames.step = 1 # The step size between frames
movie.frames.speed = 1 # The speed at which to play the movie. 1 is normal speed, 0.5 is half speed, etc.
movie.frames.save = false # Whether to save the frames as images (default is false)
```

Here are all of the optional attributes that can be specified in the `[plot_names.axes.axes_name]` table of a Plot Runnable. Note that the `x/y/zlim` and `view` attributes can be specified hard-coded or dynamically using variable names.
```toml
[plot_name.axes.axes_name]
position = [rows, columns, index] # The position of the axes in the plot following the matplotlib convention
# OR
position = [left, bottom, width, height] # The position of the axes in the plot following the matplotlib convention
font_size = 12 # The font size of the text on the axes
view = [azimuth, elevation] # The view of the plot in 3D space (default is [0, 90] for 2D plots)
title = "Axes Title" # The title of the axes
xlabel = "X-axis Label" # The label for the x-axis
ylabel = "Y-axis Label" # The label for the y-axis
zlabel = "Z-axis Label" # The label for the z-axis
xlim = [min, max] # The limits of the x-axis
ylim = [min, max] # The limits of the y-axis
zlim = [min, max] # The limits of the z-axis
```

Finally, here are all of the optional attributes that can be specified in the `[plot_names.axes.axes_name.components.component_name]` table of a Plot Runnable.
```toml
[plot_name.axes.axes_name.components.component_name]
props.prop1 = "value" # Overrides the default value of "prop1" for the component

# Example
props.LineWidth = 2 # Overrides the default value of "LineWidth" for the component
```