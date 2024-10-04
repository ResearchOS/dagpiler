# Package Folder Structure

```text
root/
├── .dependencies/ (folder created by ros specifically for packages)
├── .venv/ (typical virtual environment folder created by the user with pip, conda, etc.)
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

## Benefits
1. By explicitly specifying the .dependencies folder as the installation path, installation is independent of virtual environment defaults.
2. By default, the wheel is built from the `src` directory, so the dependencies will be properly excluded.

## Downsides
1. Because the package is installed in a custom location, I need to wrap the pip install in an `ros install`. 