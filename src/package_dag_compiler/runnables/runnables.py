from abc import abstractmethod

class Runnable():
    """Interface for runnable objects that can be run in a DAG."""

    types = ["process", "plot", "summary"]    

    def __init__(self):
        pass

    @abstractmethod
    def from_dict(self, runnable_dict: dict):
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass