import os
import json
import toml

class ConfigReader:
    """Interface for reading all configuration files except index files."""
    def read_config(self, config_path: str) -> dict:
        raise NotImplementedError("Each config reader must implement a read_config method")

class ConfigReaderFactory:

    config_readers = {}

    def get_config_reader(self, config_path: str) -> ConfigReader:
        ext = os.path.splitext(config_path)[1]
        config_reader = self.config_readers.get(ext, None)
        if config_reader is None:
            raise ValueError(f"No config reader found for extension {ext}")
        return config_reader
    
    def register_config_reader(self, ext: str, config_reader: ConfigReader):
        self.config_readers[ext] = config_reader

CONFIG_READER_FACTORY = ConfigReaderFactory()

def register_config_reader(ext: str):
    def decorator(cls):
        CONFIG_READER_FACTORY.register_config_reader(ext, cls())
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