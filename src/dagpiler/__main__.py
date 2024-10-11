# src/package_name/__main__.py
from core import compile_dag
from dag.printer import print_dag
from visualize_dag import visualize_dag

if __name__ == "__main__":
    # package_name = "import_mocap_forceplates_from_c3d_file"
    package_name = "frame_range_no_nan"
    dag = compile_dag(package_name)
    path = "/Users/mitchelltillman/Desktop/Not_Work/Code/Python_Projects/Package-DAG-Compiler/dag.toml"
    visualize_dag(dag)
    # print_dag(dag, path)