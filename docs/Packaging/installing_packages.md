# Installing packages

You've found a package you want to use, and now you want to install it.

## Installing from PyPI

Packages are installed using:
```bash
ros install <package_name>
```

Under the hood, this runs `pip install <package_name> --target <project_root>/.dependencies`. This installs the package into the `.dependencies` directory of your project folder.

## Installing from GitHub

You can install a package from GitHub using:
```bash
ros install <github_repo_url>
```

This runs `pip install git+<github_repo_url> --target <project_root>/.dependencies`.

## Installing from a local directory

You can install a package from a local directory using:
```bash
ros install <path_to_package>
```

This runs `pip install <path_to_package> --target <project_root>/.dependencies`.