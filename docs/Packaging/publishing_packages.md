# Publishing Packages

You've created a set of TOML files, you've compiled them to a DAG, maybe you've even leveraged pre-existing packages by bridging your package with theirs, and you're ready to share your package with the world. 

## Formatting
The packaging format described here is inteded to be flexible enough to work with projects of all sizes using the provided tools. Recall that when [creating a package](creating_packages.md), the `dagpiler init` command will create the proper folder structure and files for you.

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
The Python Packaging Authority maintains the Python Packaging Index (PyPI), which is where the majority of Python packages reside. Publishing your package to PyPI is the most common way to share your package with the world. Below are the steps to publish your package to PyPI:

1. [Create an account on PyPI](https://pypi.org/account/register/)

2. [Create a distribution package](https://packaging.python.org/tutorials/packaging-projects/#generating-distribution-archives)
    - Ensure that you have filled out the `pyproject.toml` file with the necessary metadata.

3. [Upload your package to PyPI](https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives)

4. Publish your documentation
    - Run `mkdocs gh-deploy` to publish your documentation to GitHub Pages

Others can then [Install your package from PyPI](installing_packages.md#installing-from-pypi)

# 2. GitHub (or Other Online Version Control)
If your package is publicly visible and hosted in an online version control platform such as GitHub or another service, you can simply leave it there! Others can `pip install` directly from your GitHub repository (see [how to install packages from GitHub](installing_packages.md#installing-from-github)). It's always a good idea to test from another computer that your package can be successfully installed and run.
    
# 3. Other Online Repositories
There are other locations online that can host your package besides version control platforms, such as the [Open Science Foundation](https://osf.io), [Zenodo](https://zenodo.org), etc. To share your package there, you must include either a wheel or source archive of your package, ideally both.