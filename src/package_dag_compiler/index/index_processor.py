import os
import json
import toml
from abc import ABC, abstractmethod

class FileUtils:
    @staticmethod
    def get_extension(file_path: str) -> str:
        """Extract the file extension from the file path."""
        return os.path.splitext(file_path)[1]

class IndexProcessor:
    def __init__(self, factory):
        """IndexProcessor should be initialized with an IndexLoaderFactory."""
        self.factory = factory
        self.index_path = None

    def process_index(self, index_file_path: str) -> dict:
        """Process the index file."""
        self.index_path = index_file_path
        if not os.path.exists(index_file_path):
            raise FileNotFoundError(f"Index file {index_file_path} not found")
        
        ext = FileUtils.get_extension(index_file_path)
        index_loader = self.factory.get_index_loader(ext)        
        return index_loader.load_index(index_file_path)

class IndexLoader(ABC):
    """Interface for loading the index file."""
    @abstractmethod
    def load_index(self, file_path: str) -> dict:
        pass

class IndexLoaderFactory:
    def __init__(self):
        self.loaders = {}

    def register_index_loader(self, ext: str, loader: IndexLoader):
        self.loaders[ext] = loader

    def get_index_loader(self, ext: str) -> IndexLoader:
        """Retrieve a loader based on file extension."""
        loader = self.loaders.get(ext, None)
        if loader is None:
            raise ValueError(f"No loader found for extension {ext}")
        return loader
    
# Factory instance for registering index loaders
INDEX_LOADER_FACTORY = IndexLoaderFactory()

def register_index_loader(ext: str):
    """Decorator to register a new IndexLoader."""
    def decorator(cls):
        INDEX_LOADER_FACTORY.register_index_loader(ext, cls())
        return cls
    return decorator

@register_index_loader(".toml")
class IndexLoaderTOML(IndexLoader):
    def load_index(self, file_path: str) -> dict:
        with open(file_path, "r") as f:
            return toml.load(f)

@register_index_loader(".json")
class IndexLoaderJSON(IndexLoader):
    def load_index(self, file_path: str) -> dict:
        with open(file_path, "r") as f:
            return json.load(f)
