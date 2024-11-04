from ...nodes.runnables.runnables import Runnable
from ...nodes.runnables.runnable_factory import register_runnable
from ...nodes.runnables.dict_validator import DictValidator

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
        super().__init__() # Mandatory

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
        # Create a new dictionary with converted inputs to avoid modifying the original
        runnable_dict["inputs"] = {key: value.to_dict() if hasattr(value, 'to_dict') else value 
                                for key, value in self.inputs.items()}

        # Create a new list with converted outputs to avoid modifying the original
        runnable_dict["outputs"] = [output.to_dict() if hasattr(output, 'to_dict') else output 
                                    for output in self.outputs]          
            
        return runnable_dict    

    