from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..variables.variables import Variable

from ...constants import VARIABLE_TYPES_KEYS

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
        
    def create_variable(self, variable_name: str, raw_user_inputted_value: Any = None) -> "Variable":
        variable_type = get_variable_type(variable_name, raw_user_inputted_value)

        variable_class = self.variable_types.get(variable_type, None)
        if variable_class is None:
            raise ValueError(f"No variable class found for type {variable_type}")      

        # Create a temporary variable object to get its value_for_hashing
        temp_variable = variable_class(variable_name, raw_user_inputted_value)

        # Use (name, hash(value_for_hashing)) tuple as the key for the cache
        cache_key = temp_variable.attrs_hash()

        # If the variable is already in the cache, return the cached variable
        if self.use_singleton:
            if cache_key in self.variable_cache:
                return self.variable_cache[cache_key]
        
        # If not, store the variable in the cache and return it
        self.variable_cache[cache_key] = temp_variable
        return temp_variable
    
    def convert_variable(self, previous_input_variable: "Variable", source: Any) -> "Variable":
        """Convert a variable to a different type."""
        # Remove old variable from cache
        cache_key = previous_input_variable.attrs_hash()
        self.variable_cache.pop(cache_key, None)

        # Create a new variable
        new_variable = self.create_variable(previous_input_variable.name, source)
        return new_variable
    
def get_variable_type(variable_name: str, raw_user_inputted_value: Any = None) -> str:
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
    return variable_type

VARIABLE_FACTORY = VariableFactory()

def register_variable(variable_type: str):
    def decorator(cls):
        VARIABLE_FACTORY.register_variable(variable_type, cls)
        return cls
    return decorator