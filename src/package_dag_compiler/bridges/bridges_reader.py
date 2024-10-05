

class BridgesReader:
    """Read the bridges files."""
    def __init__(self):
        pass

    def read(self):
        bridges = []
        for b in bridges:
            bridges.append(self._read_bridge(b))
        return bridges
    
    def _read_bridge(self, bridge_file: str) -> str:
        with open(bridge_file, 'r') as f:
            return f.read()