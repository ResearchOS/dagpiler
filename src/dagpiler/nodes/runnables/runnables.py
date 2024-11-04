from ...nodes.node import Node
from ...nodes.variables.variable_factory import VARIABLE_FACTORY

class Runnable(Node):
    """Interface for runnable objects that can be run in a DAG."""   
    pass              

def initialize_variables(runnable: Runnable):
    """Initialize input and output variables for the runnable."""
    if hasattr(runnable, "inputs"):
        initialize_inputs(runnable)
    if hasattr(runnable, "outputs"):
        initialize_outputs(runnable)

def initialize_inputs(runnable: Runnable):
    """Initialize input variables for the runnable."""
    inputs_dict = {}
    for input_key, input_var_string in runnable.inputs.items():
        full_var_name = f"{runnable.name}.{input_key}"
        inputs_dict[input_key] = VARIABLE_FACTORY.create_variable(full_var_name, input_var_string)
    runnable.inputs = inputs_dict

def initialize_outputs(runnable: Runnable):
    """Initialize output variables for the runnable."""
    outputs_dict = {}
    for output_var_string in runnable.outputs:
        full_var_name = f"{runnable.name}.{output_var_string}"
        outputs_dict[output_var_string] = VARIABLE_FACTORY.create_variable(full_var_name)
    runnable.outputs = outputs_dict