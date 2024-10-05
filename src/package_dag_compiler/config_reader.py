import json
import toml

class ConfigReader:
    """Interface for reading all configuration files except index files."""
    def __init__(self, factory):
        self.factory = factory

    def read_config(self, config_path: str) -> dict:
        config_reader = self.factory.get_config_reader(config_path)
        return config_reader.read_config(config_path)

class ConfigReaderFactory:

    config_readers = {}

    def get_config_reader(self, config_path: str) -> ConfigReader:
        ext = config_path.split('.')[-1]
        config_reader = self.config_readers.get(ext, None)
        if config_reader is None:
            raise ValueError(f"No config reader found for extension {ext}")
        return config_reader
    
    def register_config_reader(self, ext: str, config_reader: ConfigReader):
        self.config_readers[ext] = config_reader

config_reader_factory = ConfigReaderFactory()

def register_config_reader(ext: str):
    def decorator(cls):
        config_reader_factory.register_config_reader(ext, cls())
        return cls
    return decorator

@register_config_reader(".json")
class JSONConfigReader(ConfigReader):
    def read_config(self, config_path: str) -> dict:
        with open(config_path, 'r') as f:
            return json.load(f)
        
@register_config_reader(".toml")
class TOMLConfigReader(ConfigReader):
    def read_config(self, config_path: str) -> dict:
        with open(config_path, 'r') as f:
            return toml.load(f)