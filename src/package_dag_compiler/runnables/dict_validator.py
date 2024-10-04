

class DictValidator():
    def __init__(self):
        self.factory = ValidatorFactory()

    def validate(self, dictionary: dict) -> dict:
        cleaned_dict = {}
        for key, value in dictionary.items():
            validator = self.factory.get_validator(key)
            if validator:
                cleaned_dict[key] = validator.validate(value)
            else:
                cleaned_dict[key] = value # Allows for optional keys
        return cleaned_dict
    
class AttributeValidator:
    """Interface for attribute cleaning strategies."""
    def validate(self, value):
        raise NotImplementedError("Each validator must implement a clean method")
    
class ValidatorFactory:
    """Factory class to manage and provide appropriate validators for attributes."""
    
    def __init__(self):
        self.validators = {}

    def register_validator(self, key: str, validator: AttributeValidator):
        """Registers a validator for a specific attribute key."""
        self.validators[key] = validator

    def get_validator(self, key: str):
        """Retrieves the validator for the given key, if it exists."""
        return self.validators.get(key, None)
    
# ValidatorFactory instance, used for registering validators
validator_factory = ValidatorFactory()

# Register validator decorator to automatically register new validators
def register_validator(key: str):
    def decorator(validator_cls):
        validator_factory.register_validator(key, validator_cls())
        return validator_cls
    return decorator

@register_validator("name")
class NameValidator(AttributeValidator):
    """Cleans the 'name' attribute."""
    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError(f"Expected 'name' to be a str, got {type(value)}")
        return value.strip()

@register_validator("exec")
class ExecValidator(AttributeValidator):
    """Cleans the 'exec' attribute."""
    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError(f"Expected 'exec' to be a str, got {type(value)}")
        return value.strip()

@register_validator("inputs")
class InputsValidator(AttributeValidator):
    """Cleans the 'inputs' attribute."""
    def validate(self, value):
        if not isinstance(value, dict):
            raise ValueError(f"Expected 'inputs' to be a dict, got {type(value)}")
        return value

@register_validator("outputs")
class OutputsValidator(AttributeValidator):
    """Cleans the 'outputs' attribute."""
    def validate(self, value):
        if not isinstance(value, list):
            raise ValueError(f"Expected 'outputs' to be a list, got {type(value)}")
        return value

@register_validator("level")
class LevelValidator(AttributeValidator):
    """Cleans the 'level' attribute."""
    def validate(self, value):
        if not isinstance(value, list):
            raise ValueError(f"Expected 'level' to be a list, got {type(value)}")
        return value

@register_validator("batch")
class BatchValidator(AttributeValidator):
    """Cleans the 'batch' attribute."""
    def validate(self, value):
        if not isinstance(value, list):
            raise ValueError(f"Expected 'batch' to be a list, got {type(value)}")
        return value