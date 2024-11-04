from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...nodes.runnables.runnables import Runnable

class RunnableFactory():
    """Factory for creating Runnable objects."""

    def __init__(self):
        self.runnable_types = {}

    def register_runnable(self, runnable_type: str, runnable_class):
        self.runnable_types[runnable_type] = runnable_class

    def create_runnable(self, runnable_dict: dict) -> "Runnable":
        runnable_type = runnable_dict.get("type")
        runnable_class = self.runnable_types.get(runnable_type, None)        
        if runnable_class is None:
            raise ValueError(f"No runnable class found for type {runnable_type}")        
        del runnable_dict["type"]      
        return runnable_class(**runnable_dict)
    
RUNNABLE_FACTORY = RunnableFactory()

def register_runnable(runnable_type: str):
    def decorator(cls):
        RUNNABLE_FACTORY.register_runnable(runnable_type, cls)
        return cls
    return decorator