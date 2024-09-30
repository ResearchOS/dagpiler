from package_dag_compiler.toml_files.read_toml import read_runnable_plot, read_runnable_process, read_runnable_stats

def _get_index_readers():
    """Get the index readers."""
    INDEX_READERS = {}
    INDEX_READERS["process"] = read_runnable_process
    INDEX_READERS["plot"] = read_runnable_plot
    INDEX_READERS["stats"] = read_runnable_stats
    return INDEX_READERS

def get_index_reader(index_key: str):
    """Get the reader function for the index key."""
    return _get_index_readers()[index_key]

def get_required_index_fields() -> list:
    """Get the required fields for the index dictionary."""
    return [k for k in _get_index_readers().keys()]

def clean_index_dict(index_dict: dict) -> dict:
    """Clean the index dictionary."""
    required_fields = get_required_index_fields()   
    for field in required_fields:
        # Ensure all required fields are present
        if field not in index_dict:
            index_dict[field] = []
        # Ensure all required fields are lists
        if not isinstance(index_dict[field], list):
            index_dict[field] = [index_dict[field]]
    non_require_fields = [field for field in index_dict.keys() if field not in required_fields]
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
    if runnable["type"] not in get_required_index_fields():
        raise ValueError(f"Runnable type: {runnable['type']} is not valid.")
    return runnable