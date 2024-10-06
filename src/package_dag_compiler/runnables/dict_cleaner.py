

class DictCleaner():
    """Clean the dictionary for a runnable."""
    def __init__(self):
        self.factory = CleanerFactory()

    def clean(self, dictionary: dict) -> dict:
        cleaned_dict = {}
        for key, value in dictionary.items():
            cleaner = self.factory.get_cleaner(key)            
            cleaned_dict[key] = cleaner.clean(value)
        return cleaned_dict
    
class AttributeCleaner:
    """Interface for attribute cleaning strategies."""
    def clean(self, value):
        raise NotImplementedError("Each cleaner must implement a clean method")
    
class FallbackCleaner(AttributeCleaner):
    """Fallback cleaner for values of any type."""
    def clean(self, value):
        if isinstance(value, str):
            return self._clean_string(value)
        elif isinstance(value, list):
            return self._clean_list(value)
        elif isinstance(value, dict):
            return self._clean_dict(value)
        else:
            return self._clean_generic(value)

    def _clean_string(self, value: str):
        """Trims whitespace for strings."""
        return value.strip()

    def _clean_list(self, value: list):
        """Cleans each element of a list."""
        return [self.clean(item) for item in value]

    def _clean_dict(self, value: dict):
        """Cleans each key-value pair in a dict."""
        return {k: self.clean(v) for k, v in value.items()}

    def _clean_generic(self, value):
        """Returns the value as-is for types that don't need special cleaning."""
        return value
    
class CleanerFactory:
    """Factory class to manage and provide appropriate cleaners for attributes."""
    
    def __init__(self):
        self.cleaners = {
            "default": FallbackCleaner()
        }

    def register_cleaner(self, key: str, cleaner: AttributeCleaner):
        """Registers a cleaner for a specific attribute key."""
        self.cleaners[key] = cleaner

    def get_cleaner(self, key: str):
        """Retrieves the cleaner for the given key, if it exists."""
        cleaner = self.cleaners.get(key, None)
        if cleaner is None:
            cleaner = self.cleaners["default"]
        return cleaner
    
# CleanerFactory instance, used for registering cleaners
cleaner_factory = CleanerFactory()

# Register cleaner decorator to automatically register new cleaners
def register_cleaner(key: str):
    def decorator(cleaner_cls):
        cleaner_factory.register_cleaner(key, cleaner_cls())
        return cleaner_cls
    return decorator


@register_cleaner("name")
class NameCleaner(AttributeCleaner):
    """Cleans the 'name' attribute."""
    def clean(self, value):
        if not isinstance(value, str):
            raise ValueError(f"Expected 'name' to be a str, got {type(value)}")
        value.lower()
        return value.strip()

@register_cleaner("exec")
class ExecCleaner(AttributeCleaner):
    """Cleans the 'exec' attribute."""
    def clean(self, value):
        if not isinstance(value, str):
            raise ValueError(f"Expected 'exec' to be a str, got {type(value)}")
        value.lower()
        return value.strip()

@register_cleaner("inputs")
class InputsCleaner(AttributeCleaner):
    """Cleans the 'inputs' attribute."""
    def clean(self, value):
        if not isinstance(value, dict):
            raise ValueError(f"Expected 'inputs' to be a dict, got {type(value)}")
        cleaned_value = {}
        for key, value in value.items():
            cleaned_key = key.lower()
            cleaned_value[cleaned_key] = value
        return cleaned_value

@register_cleaner("outputs")
class OutputsCleaner(AttributeCleaner):
    """Cleans the 'outputs' attribute."""
    def clean(self, value):
        if not isinstance(value, list):
            raise ValueError(f"Expected 'outputs' to be a list, got {type(value)}")
        return value

@register_cleaner("level")
class LevelCleaner(AttributeCleaner):
    """Cleans the 'level' attribute."""
    def clean(self, value):
        if not isinstance(value, list):
            raise ValueError(f"Expected 'level' to be a list, got {type(value)}")
        return value

@register_cleaner("batch")
class BatchCleaner(AttributeCleaner):
    """Cleans the 'batch' attribute."""
    def clean(self, value):
        if not isinstance(value, list):
            raise ValueError(f"Expected 'batch' to be a list, got {type(value)}")
        return value