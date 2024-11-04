from ..runnables.runnables import Runnable
from ..runnables.runnable_factory import register_runnable
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

    