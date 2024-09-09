import ast
import pytest
from crimson.ast_dev_tool.getter import get_node


# Sample function and class for testing
def sample_function():
    return "Hello, World!"


class SampleClass:
    def sample_method(self):
        pass


# Test cases
def test_get_node_with_string():
    source = "def test(): pass"
    result = get_node(source)
    assert isinstance(result, ast.AST)
    assert isinstance(result.body[0], ast.FunctionDef)


def test_get_node_with_function():
    result = get_node(sample_function)
    assert isinstance(result, ast.AST)
    assert isinstance(result.body[0], ast.FunctionDef)


def test_get_node_with_method():
    result = get_node(SampleClass.sample_method)
    assert isinstance(result, ast.AST)
    assert isinstance(result.body[0], ast.FunctionDef)


def test_get_node_with_module():
    import example_module

    result = get_node(example_module)
    assert isinstance(result, ast.AST)
    assert isinstance(result, ast.Module)


def test_get_node_with_class():
    result = get_node(SampleClass)
    assert isinstance(result, ast.AST)
    assert isinstance(result.body[0], ast.ClassDef)


def test_get_node_invalid_input():
    with pytest.raises(Exception):
        get_node(42)


if __name__ == "__main__":
    pytest.main()
