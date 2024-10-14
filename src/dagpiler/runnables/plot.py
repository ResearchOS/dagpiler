from ..runnables.runnables import Runnable, register_runnable, initialize_inputs, initialize_outputs
from ..runnables.dict_validator import DictValidator

RUNNABLE_TYPE = "plot"

@register_runnable(RUNNABLE_TYPE)
class Plot(Runnable):
    """A process object that can be run in a DAG."""
    
    def __init__(self, 
                 name: str, 
                 exec: str,
                 inputs: dict,
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
            "level": level,
            "batch": batch,
            "subset": subset
        }
        runnable_dict.update(kwargs)
        dict_validator = DictValidator()
        dict_validator.validate(runnable_dict)    
        self.name = name
        self.exec = exec
        self.inputs = inputs
        self.level = level
        self.batch = batch

    @classmethod
    def from_dict(cls, runnable_dict: dict):        
        return cls(**runnable_dict)

    def to_dict(self) -> dict:
        runnable_dict = {
            "name": self.name,
            "type": RUNNABLE_TYPE,
            "exec": self.exec,                        
            "inputs": self.inputs,
            "level": self.level,
            "batch": self.batch
        }
        return runnable_dict
    
    def initialize_variables(self):
        initialize_inputs(self)
        initialize_outputs(self)

    