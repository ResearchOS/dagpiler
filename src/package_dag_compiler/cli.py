"""Contains all the command line interface code for the Package-DAG-Compiler package."""
import os

import typer

from package_dag_compiler.toml_files.discover_toml import discover_pyproject_files
from package_dag_compiler.toml_files.read_toml import read_toml_files
from package_dag_compiler.dag.create_dag import create_dag_from_dict

# Create a Typer CLI endpoint
app = typer.Typer()

@app.command(name = "compile")
def compile(pyproject_toml_path: str):
    """Compile the package DAG."""    
    # Discover the TOML files
    pyproject_toml_files = discover_pyproject_files(pyproject_toml_path)
    # Read the TOML files
    toml_data = read_toml_files(pyproject_toml_files)

    # Create the DAG from the loaded TOML files
    package_dag = create_dag_from_dict(toml_data)
    return package_dag

@app.command(name = "discover")
def discover_toml_files():
    """List all the pyproject.toml files that are discoverable."""
    # Discover the TOML files
    toml_files = discover_pyproject_files()
    print("ResearchOS Packages")
    print("====================")
    for file in toml_files:
        print(file)    

if __name__=="__main__":
    app()