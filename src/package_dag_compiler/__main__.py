# src/package_name/__main__.py
from core import compile_dag

if __name__ == "__main__":
    # package_name = "import_mocap_forceplates_from_c3d_file"
    package_name = "frame_range_no_nan"
    compile_dag(package_name)
