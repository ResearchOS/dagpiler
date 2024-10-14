#! constants.py

# Constants for the DAGpiler package

DELIMITER = '::'

# Keys to determine the type of input variable in the TOML file.
# The key is the key in the TOML file, and the value is the variable type.
VARIABLE_TYPES_KEYS = {
    "__load__": "load_from_file",
    "__data_object_path__": "data_object_file_path",
    "__data_object_name__": "data_object_name"
}

# Used in the init() function to personalize the project
INIT_TEMPLATE_DIR = "init_template_directory"
DEFAULT_PROJECT_NAME = "My Project"
DEFAULT_AUTHOR_NAME = "Author Name"
DEFAULT_AUTHOR_EMAIL = "author@email.com"

# GitHub repository details
OWNER = "researchos"
REPO = "dagpiler"
BRANCH = "main"  # or the branch you want to replicate