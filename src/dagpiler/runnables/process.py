from ..runnables.runnables import Runnable, register_runnable
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
        for input_key, input_value in runnable_dict["inputs"].items():
            if hasattr(input_value, 'to_dict') and callable(input_value.to_dict):
                runnable_dict["inputs"][input_key] = input_value.to_dict()           

        for output_key, output_value in runnable_dict["outputs"].items():
            if hasattr(output_value, 'to_dict') and callable(output_value.to_dict):
                runnable_dict["outputs"][output_key] = output_value.to_dict()            
            
        return runnable_dict

    