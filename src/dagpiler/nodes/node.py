from abc import abstractmethod
import uuid
import hashlib

class Node:

    def __init__(self):
        self._uuid = str(uuid.uuid4())    

    @classmethod
    def from_dict(cls, runnable_dict: dict):        
        return cls(**runnable_dict)

    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError("to_dict method not implemented")
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def attrs_hash(self):
        """Hash the attributes of the Process object."""
        attrs_dict = self.to_dict()
        # if "inputs" in attrs_dict:
        #     inputs_list = []
        #     for input_name, input in attrs_dict["inputs"].items():
        #         inputs_list.append(input_name + ": " + str(frozenset(input.items())))
        #     attrs_dict["inputs"] = ", ".join(inputs_list)
        # if "outputs" in attrs_dict:
        #     attrs_dict["outputs"] = tuple(attrs_dict["outputs"])
        # if "batch" in attrs_dict:
        #     attrs_dict["batch"] = tuple(attrs_dict["batch"])

        hashable_repr = str(attrs_dict.items())
        return self._hash(hashable_repr)
    
    def __hash__(self) -> int:
        """Compute a  unique SHA256 hash for the instance from the UUID, which is immutable.
        Note that this hash will change during each run, as it's tied to a random UUID.
        Therefore, its only purpose is to identify the object as a node in the DAG."""
        hashable_repr = str(self._uuid)
        return self._hash(hashable_repr)
    
    def _hash(self, string_to_hash: str):
        """Perform the actual hashing on a string."""
        if not isinstance(string_to_hash, str):
            raise ValueError("String to hash must be a string.")
        sha256_hash = hashlib.sha256(string_to_hash.encode('utf-8')).hexdigest()
        return int(sha256_hash, 16) % (10 ** 8)  # Modulo to fit within typical hash size
    
    def __copy__(self) -> "Node":
        """Copy attributes to a new instance."""
        return self.__class__.from_dict(self.to_dict())
        
    def __eq__(self, other) -> bool:
        if not isinstance(other, Node):
            return False
        return self.attrs_hash() == other.attrs_hash()
    
class NodeFactory:
    """Decides whether to create a Runnable or Variable based on the dictionary passed in."""

    def create_node(self, node_dict: dict):
        from runnables.runnable_factory import RUNNABLE_FACTORY
        from variables.variable_factory import VARIABLE_FACTORY
        if "inputs" in node_dict or "outputs" in node_dict:
            return RUNNABLE_FACTORY.create_runnable(node_dict)
        return VARIABLE_FACTORY.create_variable(node_dict)