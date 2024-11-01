# dagpiler
Tool to compile a DAG of a data processing pipeline from formatted TOML files.

By adhering to a portable, flexible standard, data science packages written by independent authors can be easily merged together. This foundational layer can then support and tie together tools and standards within and between disciplines.

Dagpiler is the first in a planned series of tools that will build on one another to standardize and facilitate common operations in data processing. 

## Useage
```python
from dagpiler import compile_dag

# Compile the DAG.
dag = compile_dag('package_name')

# Write the DAG to JSON file.
dag.print_dag('dag.json')
```

## Documentation
Documentation: https://researchos.github.io/dagpiler/