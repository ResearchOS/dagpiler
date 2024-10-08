from abc import ABC, abstractmethod

from dagpiler.toml_files.read_toml import read_runnable_plot, read_runnable_process, read_runnable_stats

REQUIRED_INDEX_FIELDS = ["process", "plot", "stats"]

class IndexKeyProcessor(ABC):
    """Abstract class for index key processors."""
    @abstractmethod
    def process(self, index_dict: dict) -> dict:
        """Process the index dictionary."""
        pass

class ProcessIndexKeyProcessor(IndexKeyProcessor):
    """Process the process index key."""
    def process(self, index_dict: dict) -> dict:
        """Process the index dictionary."""
        return read_runnable_process(index_dict)
    
class PlotIndexKeyProcessor(IndexKeyProcessor):
    """Process the plot index key."""
    def process(self, index_dict: dict) -> dict:
        """Process the index dictionary."""
        return read_runnable_plot(index_dict)
    
class StatsIndexKeyProcessor(IndexKeyProcessor):
    """Process the stats index key."""
    def process(self, index_dict: dict) -> dict:
        """Process the index dictionary."""
        return read_runnable_stats(index_dict)
    
class IndexKeyProcessorFactory:
    """Factory for creating index key processors."""
    @staticmethod
    def create_index_key_processor(index_key: str) -> IndexKeyProcessor:
        """Create an index key processor."""
        if index_key == "process":
            return ProcessIndexKeyProcessor()
        if index_key == "plot":
            return PlotIndexKeyProcessor()
        if index_key == "stats":
            return StatsIndexKeyProcessor()
        raise ValueError(f"Index key: {index_key} is not valid.")

def clean_index_dict(index_dict: dict) -> dict:
    """Clean the index dictionary."""
    for field in REQUIRED_INDEX_FIELDS:
        # Ensure all required fields are present
        if field not in index_dict:
            index_dict[field] = []
        # Ensure all required fields are lists
        if not isinstance(index_dict[field], list):
            index_dict[field] = [index_dict[field]]
    non_require_fields = [field for field in index_dict.keys() if field not in REQUIRED_INDEX_FIELDS]
    for field in non_require_fields:
        # Ensure all non-required fields are lists
        if not isinstance(index_dict[field], list):
            index_dict[field] = [index_dict[field]]
    return index_dict

def clean_and_validate_runnable(runnable: dict) -> dict:
    """Clean and validate the runnable dictionary."""
    # Ensure that the required fields are present
    required_fields = ["type", "name"]
    for field in required_fields:
        if field not in runnable:
            raise ValueError(f"Runnable dictionary is missing required field: {field}.")
    # Ensure that the type is valid
    if runnable["type"] not in REQUIRED_INDEX_FIELDS():
        raise ValueError(f"Runnable type: {runnable['type']} is not valid.")
    return runnable