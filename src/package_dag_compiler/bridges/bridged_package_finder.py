

class BridgedPackageFinder:
    """Interface for locating the packages that are bridged by a package."""

    def get_package_dependencies(self, bridges_list: dict) -> list:
        """Get the dependencies of a package."""
        pass