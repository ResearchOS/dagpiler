# Publishing Packages

You've created a set of TOML files, you've compiled them to a DAG, maybe you've even leveraged pre-existing packages by bridging your package with theirs, and you're ready to share your package with the world. 

## Formatting
The packaging format described here is inteded to be flexible enough to work with projects of all sizes using the provided tools.
!!!todo
    Command line tools will be provided to generate the folder structure below, including auto-populating the minimum required contents of pyproject.toml files.

### Package Folder Structure
Verify that your package follows the expected folder structure.

```text
root/
├── .venv/ # created by the user with python -m venv .venv
├── src/
│   ├── $project_name/
│   │   ├── index.toml # Package metadata
├── tests/
│   ├── test_main.py
├── docs/
│   ├── index.md
├── pyproject.toml
├── README.md
├── LICENSE
├── CONTRIBUTING.md
```

Use the provided tools to check that your package matches the required format.
!!!todo
    A command line tool will ensure that the above folder structure is adhered to, including a `docs` and `tests` folder.

Once your package is in the proper format and fully functioning, there are multiple ways to share your package with the world.

# 1. PyPI
The Python Packaging Authority maintains the Python Packaging Index (PyPI), which is where the majority of Python packages reside. Packages in PyPI can be easily installed using `pip install`.

# 2. GitHub (or Other Online Version Control)
If your package is publicly visible and hosted in an online version control platform such as GitHub or another service, you can simply leave it there! Others can pip install directly from your GitHub repository. It's always a good idea to test from another computer that your package can be successfully installed and run.

!!!todo
    