import hashlib

from abc import abstractmethod
from ..variables.variables import VARIABLE_FACTORY

class Runnable:
    """Interface for runnable objects that can be run in a DAG.""" 

    @classmethod
    def from_dict(cls, runnable_dict: dict):        
        return cls(**runnable_dict)

    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError("to_dict method not implemented")

    @abstractmethod
    def initialize_variables(self):
        raise NotImplementedError("initialize_variables method not implemented")
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __hash__(self) -> int:
        """Compute a unique SHA256 hash for the instance."""
        # Convert the dictionary representation to a sorted, stable string for hashing
        hashable_repr = str(sorted(self.to_dict().items()))
        sha256_hash = hashlib.sha256(hashable_repr.encode('utf-8')).hexdigest()
        
        # Truncate the sha256 hash to fit within the integer space for __hash__.
        return int(sha256_hash, 16) % (10 ** 8)  # Modulo to fit within typical hash size
        
    def __eq__(self, other) -> bool:
        if not isinstance(other, Runnable):
            return False
        return self.to_dict() == other.to_dict()

class RunnableFactory():
    """Factory for creating Runnable objects."""

    def __init__(self):
        self.runnable_types = {}

    def register_runnable(self, runnable_type: str, runnable_class):
        self.runnable_types[runnable_type] = runnable_class

    def create_runnable(self, runnable_dict: dict) -> Runnable:
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

class NodeFactory:
    """Decides whether to create a Runnable or Variable based on the dictionary passed in."""

    def create_node(self, node_dict: dict):
        if "inputs" in node_dict or "outputs" in node_dict:
            return RUNNABLE_FACTORY.create_runnable(node_dict)
        return VARIABLE_FACTORY.create_variable(node_dict)