"""Contains all the command line interface code for the dagpiler package."""
import os

import typer

from .toml_files.discover_toml import discover_pyproject_files
# from package_dag_compiler.dag.create_dag import create_dag_from_edge_list_of_toml_files

# Create a Typer CLI endpoint
app = typer.Typer()

@app.command(name = "compile")
def main(pyproject_toml_path: str):
    """Compile the package DAG."""        

    # Discover the TOML files, return the edge list of paths
    pyproject_toml_edge_list            = discover_pyproject_files(pyproject_toml_path)

    # Sort the dependencies edge list. Must be kept as an edge list to handle dependencies properly.
    sorted_pyproject_toml_edge_list     = sort_dependencies_edge_list(pyproject_toml_edge_list)       

    # Create the DAG from the loaded TOML files
    package_dag                         = create_dag_from_edge_list_of_toml_files(sorted_pyproject_toml_edge_list)
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
    # app()
    pyproject_path = "/Users/mitchelltillman/Desktop/Not_Work/Code/Python_Projects/Package-DAG-Compiler/tests/fixtures/packages/package1/pyproject.toml"
    main(pyproject_path)