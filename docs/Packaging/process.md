# Process Runnables

Minimal working example:
```toml
[process_name]
type = "process"
exec = "path/to/file.ext:func_name"
inputs.input1 = "runnable1.variable1"
outputs = [
    "output1",
    "output2"
]
```

Primarily, the focus when creating Process Runnables is on the `inputs` fields, as there are many different kinds of inputs that can be specified. Below are definitions and examples of several different kinds of supported inputs.

## Inputs
### Dynamic
These are the names of variables that were output from a previous Runnable ***within the same package***. If they come from a different package, they should be specified in the `bridges.toml` file.

The dynamic variable names are formatted as `runnable_name.variable_name`. The `runnable_name` is the name of the Runnable that produced the variable, and the `variable_name` is the name of the variable that was produced. It must match the name of the variable in the `outputs` list from the producing Runnable. For example:
```toml
[runnable1_name]
type = "process"
inputs.input1 = "runnable2_name.variable1"
```
This specifies that the input variable `variable1` from `runnable2_name` should be used as `input1` in `runnable1_name`.
!!!warning
    If you specify a variable from a Runnable in a different package in the `inputs` field, the compiler will not be able to find it and will raise an error.
!!!tip
    You can specify to use only part of a dynamic variable by including the same slicing syntax used in Python dicts and numpy arrays. For example, `runnable1.variable1["key"]` will only use the value associated with the key `"key"` from the variable `variable1` produced by `runnable1`.

### Unspecified
Indicates that this input does not come from a Runnable within this package. These inputs must be specified in the `bridges.toml` file to run the package.
```toml
inputs.input1 = "?"
```

### Load File
For a variety of reasons, variables are often loaded from files. Providing the `__load__` keyword and the **relative** file path indicates that this variable should be loaded from the provided file. The file path should be relative to the `$project_folder/src/$project_name` directory of the package.
```toml
inputs.input1.__load__ = "path/to/file.ext"
```

### Hard-Coded
Variables can be specified directly within the TOML file. This is useful for relatively simple variables that can be typed by hand. The hard-coded values can be any valid TOML data type, including integers, floats, strings, lists, and dictionaries.
```toml
inputs.input1 = 42 # An integer
inputs.input2 = "string" # A string
inputs.input3 = [1, 2, 3] # A list
```
!!!bug
    Currently, if the hard-coded value is a string that contains a period (".") the compiler will think that it is a dynamic variable. In the future, support for escaping periods using "\\." will be addded.

    Also note that if your hard-coded value is a dictionary with a key matching one of the reserved keys defined here (e.g. `__load__`), the compiler will raise an error.
   
### Data Object Name
```toml
# The general form of the data object name syntax
inputs.input1.__data_object_name__ = "DataObject" 

# In the case where a Subject data object's names is an input.
inputs.input1.__data_object_name__ = "Subject" 
```

### Data Object File Path
```toml
# The general form of the data object file path syntax
inputs.input1.__data_object_file_path__ = "DataObject"

# In the case where a Subject data object's file path is an input.
# Typically used at the beginning of the pipeline to load the data.
inputs.input1.__data_object_file_path__ = "Subject"
```

## Outputs
Outputs are specified as a list of strings. The order of the strings in the list is important, as it determines the order of the outputs. The order of the outputs is important because it is used to identify the data with the variable names.

```toml
outputs = [
    "output1",
    "output2"
]
```