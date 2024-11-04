import re
import os

from ...config_reader import CONFIG_READER_FACTORY
from ...nodes.node import Node
from ...nodes.variables.variable_factory import VARIABLE_FACTORY, register_variable

class Variable(Node):
    """Variable object that can be used as input or output to a Runnable."""
    
    def __init__(self, 
                 name: str, 
                 user_inputted_value: str = None,
                 **kwargs):
        var_dict = {
            "name": name,
            "user_inputted_value": user_inputted_value,
            "value_for_hashing": None,
            "slices": None            
        }
        # No validation here because there really isn't any validation to perform. Any value can be a variable.
        var_dict.update(kwargs)
        for key, value in var_dict.items():
            setattr(self, key, value)
        super().__init__()

    # @abstractmethod
    def set_value_for_hashing(self):
        """Set the value of the variable for hashing."""
        # raise NotImplementedError("set_value_for_hashing method not implemented")
        pass
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "user_inputted_value": self.user_inputted_value,
            "value": self.user_inputted_value,
            "value_for_hashing": self.value_for_hashing,
        }
        
    @classmethod
    def from_dict(cls, var_dict: dict) -> "Variable":
        return VARIABLE_FACTORY.create_variable(var_dict["name"], var_dict["user_inputted_value"])


@register_variable("unspecified")
class UnspecifiedVariable(Variable):
    """Variable that is "?" in the TOML file."""
    pass

@register_variable("output")
class OutputVariable(Variable):
    """Variable that is an output of a Runnable."""

    def __init__(self, name: str, user_inputted_value: str = None):
        super().__init__(name, user_inputted_value)
        self.set_value_for_hashing()

    def set_value_for_hashing(self):
        self.value_for_hashing = self.name

@register_variable("hardcoded")
class HardcodedVariable(Variable):
    """Variable that is hard-coded in the TOML file."""
    
    def set_value_for_hashing(self):
        self.value_for_hashing = self.user_inputted_value
    
@register_variable("load_from_file")
class LoadFromFile(Variable):
    """Variable that loads its value from a file."""

    def __init__(self, name: str, user_inputted_value: str):
        super().__init__(name, user_inputted_value)
        self.set_value_for_hashing()
    
    def set_value_for_hashing(self):
        package_path = os.environ.get("PACKAGE_FOLDER", None)
        key = list(self.user_inputted_value.keys())[0]
        full_path = os.path.join(package_path, self.user_inputted_value[key])
        config_reader = CONFIG_READER_FACTORY.get_config_reader(full_path)
        self.value_for_hashing = config_reader.read_config(full_path)

@register_variable("data_object_file_path")
class DataObjectFilePath(Variable):
    """Variable that represents the path to a data object file."""
    
    def set_value_for_hashing(self):
        self.value_for_hashing = self.user_inputted_value

@register_variable("data_object_name")
class DataObjectName(Variable):
    """Variable that represents the name of a data object."""
    
    def set_value_for_hashing(self):
        self.value_for_hashing = self.user_inputted_value

@register_variable("dynamic")
class DynamicVariable(Variable):
    """Variable that is a dynamic reference to an output variable."""

    def __init__(self, name: str, user_inputted_value: str):
        super().__init__(name, user_inputted_value)
        self.set_value_for_hashing()
    
    def set_value_for_hashing(self):
        # Must include the slices in the value for hashing, otherwie the hash won't change when the slices do!
        self.value_for_hashing = self.user_inputted_value
        self.set_slices()

    def set_slices(self):
        # Regular expression to find all occurrences of "[...]" at the end of the string
        pattern = r'\[([^\[\]]+)\]'

        # Find all occurrences of the pattern in the string
        self.slices = re.findall(pattern, self.user_inputted_value)