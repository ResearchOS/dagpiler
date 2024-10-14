from abc import abstractmethod
import os
import json

class ConfigReader:
    """Interface for reading all configuration files except index files."""
    @abstractmethod
    def read_config(self, config_path: str) -> dict:
        raise NotImplementedError("Each config reader must implement a read_config method")

class ConfigReaderFactory:

    config_readers = {}

    def get_config_reader(self, config_path: str, key: str = "name") -> ConfigReader:
        ext = os.path.splitext(config_path)[1]
        config_reader = self.config_readers.get(ext, None)
        config_reader.key = key
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
        try:
            import toml
        except ImportError:
            raise ImportError("You need to install the 'toml' package to read TOML files.")
        with open(config_path, 'r') as f:
            return toml.load(f)
        
@register_config_reader(".yaml")
class YAMLConfigReader(ConfigReader):
    def read_config(self, config_path: str) -> dict:
        try:
            import yaml
        except ImportError:
            raise ImportError("You need to install the 'pyyaml' package to read YAML files.")
        with open(config_path, 'r') as f:
            return yaml.load(f, Loader=yaml.FullLoader)
        
class RunnableParser:
    """Interface for parsing runnable dicts."""
    @abstractmethod
    def parse_runnable(self, runnable: dict) -> dict:
        raise NotImplementedError("Each runnable parser must implement a parse_runnable method")
    
class RunnableParserFactory:

    runnable_parsers = {}

    def get_runnable_parser(self, key: str) -> RunnableParser:        
        runnable_parser = self.runnable_parsers.get(key, None)
        if runnable_parser is None:
            raise ValueError(f"No runnable parser found for key {key}")
        return runnable_parser
    
    def register_runnable_parser(self, ext: str, runnable_parser: RunnableParser):
        self.runnable_parsers[ext] = runnable_parser

RUNNABLE_PARSER_FACTORY = RunnableParserFactory()

def register_runnable_parser(key: str):
    def decorator(cls):
        RUNNABLE_PARSER_FACTORY.register_runnable_parser(key, cls())
        return cls
    return decorator

@register_runnable_parser("name")
class NameRunnableParser(RunnableParser):
    """Parse a runnable dict with the runnable name as the key."""
    def parse_runnable(self, runnable: dict) -> dict:
        return runnable
    
@register_runnable_parser("type")
class TypeRunnableParser(RunnableParser):
    """Parse a runnable dict with the runnable type as the key."""
    def parse_runnable(self, runnable: dict) -> dict:
        # Put the type as a key in the dictionary
        type = [k for k in runnable.keys()][0]
        runnable["type"] = type
        # Rename the key to name
        name = runnable[type]["name"]
        runnable["name"] = name
        # Remove the type key
        del runnable[type]
        return runnable