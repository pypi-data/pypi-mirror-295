import pytest
import ast
from crimson.ast_dev_tool.printer import (
    print_node,
)
from io import StringIO
import sys


# Sample function to capture print output
def capture_output(func, *args, **kwargs):
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        func(*args, **kwargs)
        return sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout


# Sample source code
source_code = """
def hello():
    print("Hello, world!")
"""

# Sample AST node
node = ast.parse(source_code)


# Sample class for _SourceObjectType test
class SampleClass:
    def sample_method(self):
        pass


sample_class_instance = SampleClass()


def test_print_node_with_ast():
    output = capture_output(print_node, node, indent=2)
    assert "Module" in output


def test_print_node_with_string():
    output = capture_output(print_node, source_code, indent=2)
    assert "Module" in output


def test_print_node_with_source_object_type():
    # Assuming get_node correctly handles SampleClass.sample_method
    output = capture_output(print_node, sample_class_instance.sample_method, indent=2)
    assert "FunctionDef" in output  # Adjust based on expected AST node type


def test_print_node_invalid_input():
    with pytest.raises(Exception):
        print_node(42, indent=2)


# Test with function type
def test_print_node_with_function():
    def sample_function():
        pass

    output = capture_output(print_node, sample_function, indent=2)
    assert "FunctionDef" in output  # Adjust based on expected AST node type


if __name__ == "__main__":
    pytest.main()
