import os

class IndexParser():

    def __init__(self, index_dict: dict):
        self.index_dict = index_dict

    def get_and_remove_bridges(self) -> list:
        """Return the bridges from the index dictionary and remove that key from the index dictionary."""
        bridges = self.index_dict.get("bridges", [])
        if not isinstance(bridges, list):
            raise ValueError(f"Expected list, got {type(bridges)}")
        for b in bridges:
            if not os.path.exists(b):
                raise FileNotFoundError(f"Bridge {b} not found")
        self.index_dict.pop("bridges", None)
        return bridges
    
    def _flatten_index(self) -> dict:
        """Flatten the index dictionary."""
        # Recursively flatten the nested dictionary, returning a list of just the values, and omitting the keys
        def flatten(d):
            for k, v in d.items():
                if isinstance(v, dict):
                    yield from flatten(v)
                else:
                    yield v
        return list(flatten(self.index_dict))
    
    def get_runnables_paths_from_index(self) -> dict:
        """Return the index dictionary."""
        paths = self._flatten_index()
        for path in paths:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Path {path} not found")
        return paths