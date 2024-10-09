# Creating New Packages

For any data science project, or when building a data processing pipeline component, first you need to initialize your project.

1. Create a new directory for your project.
```bash
mkdir $project_folder
```

2. [Create a new virtual environment in the project directory](https://docs.python.org/3/library/venv.html#creating-virtual-environments) and [activate it](https://docs.python.org/3/library/venv.html#how-venvs-work).

!!!warning
    For now, the virtual environment MUST be named `.venv` to work with the dagpiler package.

```bash
cd $project_folder
python -m venv .venv

source .venv/bin/activate # Linux and MacOS
.venv\Scripts\activate # Windows
```

3. Install the dagpiler package using pip
```bash
pip install dagpiler
```

4. Initialize the project with the `dagpiler init` command. This creates the [folder structure and files needed for the project](publishing_packages.md#package-folder-structure).
!!!todo
```bash
dagpiler init
```

5. Write the TOML files that define your data processing pipeline components. For more information on the types of TOML files, see the [Types of TOML Files](toml_files.md) page.

6. Compile the TOML files into a NetworkX Directed Acyclic Graph (DAG) using the `dagpiler compile` command. This command will check the TOML files for errors and compile them into