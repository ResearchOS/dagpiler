# Installing Packages

You've found a package you want to use, and now you want to install it! First, you need to put that package in your pyproject.toml file. Depending on where the package is being installed from, there are a few ways to do this using Python's default syntax. For more information than is provided here, check out the linked documentation in the sections below.

After updating your `pyproject.toml` file, you can install all of your package's dependencies by installing your own package using `pip install .` or `pip install -e .` from the root directory of your package.

## Installing from PyPI
Packages installed from PyPI can be specified with their package name, and optionally version restrictions. See [Python docs](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#dependencies-and-requirements) for details. 
```toml
[project]
dependencies = [
    "numpy",
    "pandas"
]
```

## Installing from GitHub
From the [Hatch documentation](https://hatch.pypa.io/1.8/config/dependency/#supported-vcs), packages can also be installed directly from GitHub repositories.
```toml
[project]
dependencies = [
    "dagpiler @ git+https://github.com/ResearchOS/dagpiler"
]
```

## Installing from a local directory
Similarly, dependency packages can be [installed from a local directory](https://hatch.pypa.io/1.8/config/dependency/#local) as well by specifying paths to either the package folder, a wheel (.whl), or source archive (.tar.gz).
```toml
[project]
dependencies = [
    "dagpiler @ file:///path/to/dependent/package/dagpiler" # Package folder path
]
```

## Installing from the Internet (other than version control)
Finally, packages can also be downloaded from any location on the Internet by specifying the package name and the link to the wheel or source archive. For example:
```toml
[project]
dependencies = [
    "pytorch @ https://download.pytorch.org/whl/cu102/torch-1.10.0%2Bcu102-cp39-cp39-linux_x86_64.whl"
]
```