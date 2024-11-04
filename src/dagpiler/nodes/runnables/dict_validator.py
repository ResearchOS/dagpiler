from ...nodes.runnables.dict_attr_validator import ATTRIBUTE_VALIDATOR_FACTORY

class DictValidatorFactory:
    """Factory class to manage and provide appropriate validators for attributes."""
    
    def __init__(self):
        self.validators = {}

    def register_validator(self, key: str, validator):
        """Registers a validator for a specific attribute key."""
        self.validators[key] = validator

    def get_validator(self, key: str):
        """Retrieves the validator for the given key, if it exists."""
        return self.validators.get(key, None)

# ValidatorFactory instance, used for registering validators
dict_validator_factory = DictValidatorFactory()

class DictValidator():
    """Validate the dictionary of a runnable."""
    def __init__(self):
        self.runnable_validator_factory = RUNNABLE_VALIDATOR_FACTORY

    def validate(self, dictionary: dict) -> dict:
        # Retrieve the 'type' attribute
        runnable_type = dictionary.get('type')
        if not runnable_type:
            raise ValueError(f"""Missing "type" attribute in "{dictionary["name"]}" dictionary""")
        
        # Retrieve the appropriate validator for the 'type' attribute
        validator = self.runnable_validator_factory.get_validator(runnable_type)

        # Use the validator to validate the dictionary
        validator.validate(dictionary)

# Register validator decorator to automatically register new validators
def register_validator(key: str):
    def decorator(validator_cls):
        dict_validator_factory.register_validator(key, validator_cls())
        return validator_cls
    return decorator

class RunnableValidator:
    """Interface for runnable validators."""            
    def validate(self, dictionary: dict) -> dict:
        # Check for missing required attributes
        missing_attrs = [attr for attr in self.required_attributes if attr not in dictionary]
        if missing_attrs:
            raise ValueError(f"Missing required attributes for 'process': {missing_attrs}")

        cleaned_dict = {}
        # Validate each attribute present in the dictionary
        for key in dictionary:
            validator = self.attribute_validator_factory.get_validator(key)
            if validator:
                cleaned_dict[key] = validator.validate(dictionary[key])
            else:
                cleaned_dict[key] = dictionary[key]  # Handle unexpected attributes if necessary
        return cleaned_dict

class RunnableValidatorFactory:
    """Factory to manage and provide appropriate runnable validators based on type."""
    def __init__(self):
        self.validators = {}

    def register_validator(self, type_key: str, validator: RunnableValidator):
        """Registers a runnable validator for a specific type."""
        self.validators[type_key] = validator

    def get_validator(self, type_key: str):
        """Retrieves the runnable validator for the given type."""
        validator = self.validators.get(type_key)
        if validator is None:
            raise ValueError(f"No RunnableValidator registered for type '{type_key}'")
        return validator

# Global factory instance for registering runnable validators
RUNNABLE_VALIDATOR_FACTORY = RunnableValidatorFactory()

def register_runnable_validator(type_key: str):
    """Decorator to register a new RunnableValidator."""
    def decorator(validator_cls):
        RUNNABLE_VALIDATOR_FACTORY.register_validator(type_key, validator_cls())
        return validator_cls
    return decorator

@register_runnable_validator("process")
class ProcessValidator(RunnableValidator):
    """Validator for 'process' type runnables."""
    def __init__(self):
        self.required_attributes = ["name", "inputs", "outputs", "type"]
        self.attribute_validator_factory = ATTRIBUTE_VALIDATOR_FACTORY  # Use existing attribute validators

@register_runnable_validator("plot")
class PlotValidator(RunnableValidator):
    """Validator for 'plot' type runnables."""
    def __init__(self):
        self.required_attributes = ["name", "type", "inputs", "axes"]
        self.attribute_validator_factory = ATTRIBUTE_VALIDATOR_FACTORY  # Use existing attribute validators   

@register_runnable_validator("plot_component")
class PlotComponentValidator(RunnableValidator):
    """Validator for 'plot' type runnables."""
    def __init__(self):
        self.required_attributes = ["name", "type", "inputs"]
        self.attribute_validator_factory = ATTRIBUTE_VALIDATOR_FACTORY  # Use existing attribute validators   

@register_runnable_validator("summary")
class SummaryValidator(RunnableValidator):
    """Validator for 'process' type runnables."""
    def __init__(self):
        self.required_attributes = ["name", "inputs", "type"]
        self.attribute_validator_factory = ATTRIBUTE_VALIDATOR_FACTORY  # Use existing attribute validators