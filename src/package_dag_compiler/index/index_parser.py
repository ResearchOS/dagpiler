import os

class IndexParser():

    def __init__(self, index_dict: dict):
        self.index_dict = index_dict

    def get_and_remove_bridges(self) -> list:
        """Return the bridges from the index dictionary and remove that key from the index dictionary so that all that's left is the runnables."""
        bridges = self.index_dict.get("bridges", [])
        if not isinstance(bridges, list):
            raise ValueError(f"Expected list, got {type(bridges)}")
        package_folder = os.environ.get("PACKAGE_FOLDER")
        for b in bridges:
            full_bridge_path = os.path.join(package_folder, b)
            if not os.path.exists(full_bridge_path):
                raise FileNotFoundError(f"Bridge {b} not found")
        self.index_dict.pop("bridges", None)
        return bridges
    
    def _flatten_index(self) -> dict:
        """Flatten the index dictionary."""
        # Recursively flatten the nested dictionary, returning a list of just the values, and omitting the keys
        def flatten(d):
            for key, value in d.items():
                if isinstance(value, dict):
                    yield from flatten(value)
                else:
                    for v in value:
                        yield v
        return list(flatten(self.index_dict))
    
    def get_runnables_paths_from_index(self) -> dict:
        """Return the index dictionary."""
        return self._flatten_index()        