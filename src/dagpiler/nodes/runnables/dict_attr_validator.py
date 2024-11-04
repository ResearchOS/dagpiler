from ...constants import DELIMITER
     
class AttributeValidator:
    """Interface for attribute cleaning strategies."""
    def validate(self, value):
        raise NotImplementedError("Each validator must implement a validation method")
    
class AttrValidatorFactory:
    """Factory class to manage and provide appropriate validators for attributes."""
    
    def __init__(self):
        self.validators = {}

    def register_validator(self, key: str, validator: AttributeValidator):
        """Registers a validator for a specific attribute key."""
        self.validators[key] = validator

    def get_validator(self, key: str):
        """Retrieves the validator for the given key, if it exists."""
        return self.validators.get(key, None)
    
ATTRIBUTE_VALIDATOR_FACTORY = AttrValidatorFactory()

def register_attr_validator(key: str):
    def decorator(validator_cls):
        ATTRIBUTE_VALIDATOR_FACTORY.register_validator(key, validator_cls())
        return validator_cls
    return decorator

@register_attr_validator("name")
class NameValidator(AttributeValidator):
    """Cleans the 'name' attribute."""
    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError(f"Expected 'name' to be a str, got {type(value)}")
        return value.strip()

@register_attr_validator("exec")
class ExecValidator(AttributeValidator):
    """Cleans the 'exec' attribute."""
    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError(f"Expected 'exec' to be a str, got {type(value)}")
        if DELIMITER not in value:
            raise ValueError(f"Expected 'exec' to contain a separator '{DELIMITER}'")
        split_exec = value.split(sep=DELIMITER)
        return value.strip()

@register_attr_validator("inputs")
class InputsValidator(AttributeValidator):
    """Cleans the 'inputs' attribute."""
    def validate(self, value):
        if not isinstance(value, dict):
            raise ValueError(f"Expected 'inputs' to be a dict, got {type(value)}")
        return value

@register_attr_validator("outputs")
class OutputsValidator(AttributeValidator):
    """Cleans the 'outputs' attribute."""
    def validate(self, value):
        if not isinstance(value, list):
            raise ValueError(f"Expected 'outputs' to be a list, got {type(value)}")
        return value

@register_attr_validator("level")
class LevelValidator(AttributeValidator):
    """Cleans the 'level' attribute."""
    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError(f"Expected 'level' to be a list, got {type(value)}")
        return value

@register_attr_validator("batch")
class BatchValidator(AttributeValidator):
    """Cleans the 'batch' attribute."""
    def validate(self, value):
        if not isinstance(value, list):
            raise ValueError(f"Expected 'batch' to be a list, got {type(value)}")
        return tuple(value)
    
@register_attr_validator("subset")
class SubsetValidator(AttributeValidator):
    """Cleans the 'subset' attribute."""
    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError(f"Expected 'subset' to be a str, got {type(value)}")
        return value
    
@register_attr_validator("type")
class TypeValidator(AttributeValidator):
    """Cleans the 'type' attribute."""
    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError(f"Expected 'type' to be a str, got {type(value)}")
        return value