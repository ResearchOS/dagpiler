from ..runnables.runnables import Runnable, register_runnable, initialize_inputs, initialize_outputs
from ..runnables.dict_validator import DictValidator

RUNNABLE_TYPE = "process"

@register_runnable(RUNNABLE_TYPE)
class Process(Runnable):
    """A process object that can be run in a DAG."""
    
    def __init__(self, 
                 name: str,                  
                 inputs: dict, 
                 outputs: list, 
                 exec: str = "",
                 level: list = "", 
                 batch: list = [],
                 subset: str = "",
                 **kwargs
                 ):    
        runnable_dict = {
            "name": name,
            "type": RUNNABLE_TYPE,
            "exec": exec,                        
            "inputs": inputs,
            "outputs": outputs,
            "level": level,
            "batch": batch,
            "subset": subset
        }
        runnable_dict.update(kwargs)
        dict_validator = DictValidator()
        dict_validator.validate(runnable_dict)
        for key, value in runnable_dict.items():
            setattr(self, key, value)

    @classmethod
    def from_dict(cls, runnable_dict: dict):        
        return cls(**runnable_dict)

    def to_dict(self) -> dict:
        runnable_dict = {
            "name": self.name,
            "type": RUNNABLE_TYPE,
            "exec": self.exec,                        
            "inputs": self.inputs,
            "outputs": self.outputs,
            "level": self.level,
            "batch": self.batch
        }
        print(f"Inputs:, {self.inputs}")
        print(f"Outputs:, {self.outputs}")
        for input_key, input_value in runnable_dict["inputs"].items():
            if hasattr(input_value, 'name'):
                runnable_dict["inputs"][input_key] = input_value.name
            # If it's a string or another type without `name`, leave as is

        for output_key, output_value in runnable_dict["outputs"].items():
            if hasattr(output_value, 'name'):
                runnable_dict["outputs"][output_key] = output_value.name
            # If it's a string or another type without `name`, leave as is
            
        return runnable_dict
    
    def initialize_variables(self):
        initialize_inputs(self)
        initialize_outputs(self)

    