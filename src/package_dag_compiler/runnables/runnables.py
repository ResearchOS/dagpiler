from abc import abstractmethod

class Runnable():

    types = ["process", "plot", "summary"]    

    def __init__(self):
        pass

    @abstractmethod
    def from_dict(self, runnable_dict: dict):
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @abstractmethod
    def _clean(self):
        pass

    @abstractmethod
    def _validate(self):
        self._validate_type(self.name, self.type)
        self._validate_name(self.name)

    def _validate_type(self, value: str, expected_type: str):
        """Validate the type of a Runnable object."""
        if not isinstance(type, str):
            raise ValueError(f"Expected str, got {type(value)}")     
        value = value.lower()   
        if not isinstance(value, expected_type):
            raise ValueError(f"Expected {expected_type}, got {type(value)}")
        if value not in self.types:
            raise ValueError(f"Expected one of {self.types}, got {value}")
        
    def _validate_name(self, name: str):
        if not isinstance(name, str):
            raise ValueError(f"Expected str, got {type(name)}")