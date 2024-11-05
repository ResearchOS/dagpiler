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
```bash
dagpiler init
```
It will ask you for the following metadata to set up the pyproject.toml and mkdocs.yml files:
    - `name`: The name of the package (REQUIRED)
    - `author name`: The name of the author (OPTIONAL)
    - `author email`: The email of the author (OPTIONAL)
!!!tip
    If you don't want to provide any metadata here (including the package name), you can provide it later in the pyproject.toml and mkdocs.yml files manually. This step is inteded only to save you time later.

5. Write the TOML files that define your data processing pipeline components. For more information on the types of TOML files, see the [Types of TOML Files](toml_files.md) page.

6. Compile the TOML files into a Directed Acyclic Graph (DAG) object using the `dagpiler compile` command line command. This command will check the TOML files for errors and compile them into the DAG.

!!!warning
    No matter how you run the `compile` command, the package name must match a package that has been pip installed in the current folder's virtual environment (.venv).

To run the command from Python:
```python
from dagpiler import compile_dag

package_name = "my_package"
dag = compile_dag(package_name)
```