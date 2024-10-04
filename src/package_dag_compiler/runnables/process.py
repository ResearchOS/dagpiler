from runnables.runnables import Runnable
from runnables.dict_cleaner import DictCleaner
from runnables.dict_validator import DictValidator

class Process(Runnable):
    """A process object that can be run in a DAG."""

    type = "process"
    
    def __init__(self, 
                 name: str, 
                 exec: str,
                 inputs: dict, 
                 outputs: list, 
                 level: list, 
                 batch: list
                 ):        
        self.name = name
        self.exec = exec
        self.inputs = inputs
        self.outputs = outputs
        self.level = level
        self.batch = batch

    @classmethod
    def from_dict(cls, runnable_dict: dict):
        cleaner = DictCleaner()
        validator = DictValidator()
        cleaned_dict = cleaner.clean(runnable_dict)
        is_valid = validator.validate(cleaned_dict)
        if not is_valid:
            raise ValueError("Invalid process dictionary")
        return cls(**cleaned_dict)

    def to_dict(self) -> dict:
        runnable_dict = {
            "name": self.name,
            "type": self.type,
            "exec": self.exec,                        
            "inputs": self.inputs,
            "outputs": self.outputs,
            "level": self.level,
            "batch": self.batch
        }
        return runnable_dict

    