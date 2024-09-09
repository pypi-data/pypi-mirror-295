import ast
import pytest
from crimson.ast_dev_tool.collector import collect_nodes


# Sample function and class for testing
def sample_function():
    x = 1
    y = 2
    return x + y


class SampleClass:
    def sample_method(self):
        pass


# Test cases
def test_collect_nodes_with_string():
    source = """
def func1():
    x = 1
    y = 2
    return x + y

def func2():
    a = 3
    b = 4
    return a * b
    """
    result = collect_nodes(source, ast.FunctionDef)
    assert len(result) == 2
    assert all(isinstance(node, ast.FunctionDef) for node in result)


def test_collect_nodes_with_ast():
    tree = ast.parse(
        """
x = 1
y = 2
z = 3
    """
    )
    result = collect_nodes(tree, ast.Assign)
    assert len(result) == 3
    assert all(isinstance(node, ast.Assign) for node in result)


def test_collect_nodes_with_function():
    result = collect_nodes(sample_function, ast.Assign)
    assert len(result) == 2
    assert all(isinstance(node, ast.Assign) for node in result)


def test_collect_nodes_with_class():
    result = collect_nodes(SampleClass, ast.FunctionDef)
    assert len(result) == 1
    assert isinstance(result[0], ast.FunctionDef)


def test_collect_nodes_return_sources():
    source = "x = 1\ny = 2\nz = 3"
    result = collect_nodes(source, ast.Assign, return_type="sources")
    assert len(result) == 3
    assert all(isinstance(item, str) for item in result)
    assert "x = 1" in result
    assert "y = 2" in result
    assert "z = 3" in result


def test_collect_nodes_empty_result():
    source = "x = 1\ny = 2\nz = 3"
    result = collect_nodes(source, ast.FunctionDef)
    assert len(result) == 0


def test_collect_nodes_invalid_input():
    with pytest.raises(Exception):
        collect_nodes(42, ast.Assign)


if __name__ == "__main__":
    pytest.main()
