import pytest

from dagpiler import compile_dag

def test_compile_dag():
    package_name = "frame_range_no_nan"
    dag = compile_dag(package_name)
    assert len(dag.nodes) == 29

if __name__=="__main__":
    pytest.main([__file__])