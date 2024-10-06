from abc import abstractmethod
from typing import Any
import re
import os

from config_reader import CONFIG_READER_FACTORY

VARIABLE_TYPES_KEYS = {
    "__load__": "load_from_file",
    "__data_object_path__": "data_object_file_path",
    "__data_object_name__": "data_object_name"
}

class Variable:
    """Variable object that can be used as input or output to a Runnable."""
    
    def __init__(self, name: str, user_inputted_value: str = None):
        self.name = name
        self.user_inputted_value = user_inputted_value # The exact value from the config file input by the user, including slices
        self.value_for_hashing = None # The value used for hashing, obtained from self.set_value_for_hashing() by Variable subclasses
        self.slices = None # The slices of the variable, if any

    def __str__(self):
        return f"Variable({self.name})"
    
    def __repr__(self) -> str:
        raise NotImplementedError("repr method not implemented")

    @abstractmethod
    def set_value_for_hashing(self):
        """Set the value of the variable for hashing."""
        raise NotImplementedError("set_value_for_hashing method not implemented")

    def __eq__(self, other: "Variable"):
        return self.name == other.name and self.value_for_hashing == other.value_for_hashing

    def __hash__(self):
        return hash(self.name)
    
class VariableFactory:
    """Factory for creating Variable objects."""
    
    def __init__(self):
        self.variable_types = {}
        self.variable_cache = {} # Cache to store unique Variable instances
        self.use_singleton = True # Use the singleton pattern for Variable objects by default

    def toggle_singleton_off(self):
        """Turn off the singleton pattern for Variable objects."""
        self.use_singleton = False
    
    def register_variable(self, variable_type: str, variable_class):
        self.variable_types[variable_type] = variable_class
        
    def create_variable(self, variable_name: str, raw_user_inputted_value: Any = None) -> Variable:
        variable_type = "hardcoded" # Default to constant if an integer or float is found
        if raw_user_inputted_value is None:
            variable_type = "output"
        if isinstance(raw_user_inputted_value, str):
            # Get the number of "." in the string
            num_periods = raw_user_inputted_value.count(".")
            if num_periods > 0:
                variable_type = "dynamic"
            elif raw_user_inputted_value != "?":
                variable_type = "hardcoded" # Any string besides "?" that doesn't contain a "."
            else:
                variable_type = "unspecified" # "?" string
        elif isinstance(raw_user_inputted_value, dict):
            key = list(raw_user_inputted_value.keys())[0]     
            variable_type = VARIABLE_TYPES_KEYS.get(key, None)
            if variable_type is None:
                variable_type = "hardcoded" # Default to constant if no special key is found
            else:
                raw_user_inputted_value = raw_user_inputted_value[key]
        elif isinstance(raw_user_inputted_value, list):
            # TODO: Implement parameter sweep
            pass

        variable_class = self.variable_types.get(variable_type, None)
        if variable_class is None:
            raise ValueError(f"No variable class found for type {variable_type}")      

        # Create a temporary variable object to get its value_for_hashing
        temp_variable = variable_class(variable_name, raw_user_inputted_value)

        # Use (name, hash(value_for_hashing)) tuple as the key for the cache
        cache_key = (temp_variable.name, temp_variable.__hash__())

        # If the variable is already in the cache, return the cached variable
        if self.use_singleton:
            if cache_key in self.variable_cache:
                return self.variable_cache[cache_key]
        
        # If not, store the variable in the cache and return it
        self.variable_cache[cache_key] = variable_class(variable_name, raw_user_inputted_value)
        return temp_variable
    
VARIABLE_FACTORY = VariableFactory()

def register_variable(variable_type: str):
    def decorator(cls):
        VARIABLE_FACTORY.register_variable(variable_type, cls)
        return cls
    return decorator

@register_variable("unspecified")
class UnspecifiedVariable(Variable):
    """Variable that is "?" in the TOML file."""

    def __repr__(self) -> str:
        return f"UnspecifiedInputVariable({self.name})"

@register_variable("output")
class OutputVariable(Variable):
    """Variable that is an output of a Runnable."""

    def __init__(self, name: str, user_inputted_value: str = None):
        super().__init__(name, user_inputted_value)
        self.set_value_for_hashing()

    def set_value_for_hashing(self):
        self.value_for_hashing = self.name
    
    def __repr__(self) -> str:
        return f"OutputVariable({self.name})"

@register_variable("hardcoded")
class HardcodedVariable(Variable):
    """Variable that is hard-coded in the TOML file."""

    def __repr__(self) -> str:
        return f"HardCodedVariable({self.name})"
    
    def set_value_for_hashing(self):
        self.value_for_hashing = self.user_inputted_value
    
@register_variable("load_from_file")
class LoadFromFile(Variable):
    """Variable that loads its value from a file."""

    def __repr__(self) -> str:
        return f"LoadFromFileVariable({self.name})"

    def __init__(self, name: str, user_inputted_value: str):
        super().__init__(name, user_inputted_value)
        self.set_value_for_hashing()
    
    def set_value_for_hashing(self):
        package_path = os.environ.get("PACKAGE_FOLDER", None)
        full_path = os.path.join(package_path, self.user_inputted_value)
        config_reader = CONFIG_READER_FACTORY.get_config_reader(full_path)
        self.value_for_hashing = config_reader.read_config(full_path)

@register_variable("data_object_file_path")
class DataObjectFilePath(Variable):
    """Variable that represents the path to a data object file."""

    def __repr__(self) -> str:
        return f"DataObjectFilePathVariable({self.name})"
    
    def set_value_for_hashing(self):
        self.value_for_hashing = self.user_inputted_value

@register_variable("data_object_name")
class DataObjectName(Variable):
    """Variable that represents the name of a data object."""

    def __repr__(self) -> str:
        return f"DataObjectNameVariable({self.name})"
    
    def set_value_for_hashing(self):
        self.value_for_hashing = self.user_inputted_value

@register_variable("dynamic")
class DynamicVariable(Variable):
    """Variable that is a dynamic reference to an output variable."""

    def __repr__(self) -> str:
        return f"DynamicInputVariable({self.name})"

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