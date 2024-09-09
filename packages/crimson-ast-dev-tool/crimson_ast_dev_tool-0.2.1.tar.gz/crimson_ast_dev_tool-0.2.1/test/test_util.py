import ast
import pytest
from crimson.ast_dev_tool.util import (
    safe_unparse,
    clean_indent,
    _count_indent,
    _clean_indent,
)


def test_safe_unparse():
    node = ast.parse("x = 1")
    result = safe_unparse(node)
    assert result == "x = 1"


def test_safe_unparse_none():
    result = safe_unparse(None)
    assert result is None


def test_clean_indent_string():
    text = """
    def func():
        x = 1
        y = 2
        return x + y
    """
    result = clean_indent(text)
    expected = "\ndef func():\n    x = 1\n    y = 2\n    return x + y\n"
    assert result == expected


def test_clean_indent_list():
    lines = [
        "    def func():",
        "        x = 1",
        "        y = 2",
        "        return x + y",
    ]
    result = clean_indent(lines)
    expected = "def func():\n    x = 1\n    y = 2\n    return x + y"
    assert result == expected


def test_clean_indent_return_lines():
    text = """
    def func():
        x = 1
        y = 2
        return x + y
    """
    result = clean_indent(text, return_type="lines")
    expected = ['', 'def func():', '    x = 1', '    y = 2', '    return x + y', '']
    assert result == expected


def test_clean_indent_no_indentation():
    text = "x = 1\ny = 2\nz = 3"
    result = clean_indent(text)
    assert result == text


def test_count_indent():
    assert _count_indent("    x = 1") == 4
    assert _count_indent("x = 1") == 0
    assert _count_indent("") is None
    assert _count_indent("  ") is None


def test_clean_indent_internal():
    lines = ["    x = 1", "        y = 2", "    z = 3"]
    result = _clean_indent(lines)
    assert result == ["x = 1", "    y = 2", "z = 3"]


def test_clean_indent_mixed_indentation():
    text = """
    def func():
        x = 1
      y = 2
        z = 3
    """
    result = clean_indent(text)
    expected = "\ndef func():\n    x = 1\n  y = 2\n    z = 3\n"
    assert result == expected


def test_clean_indent_empty_lines():
    text = """
    x = 1

    y = 2

    z = 3
    """
    result = clean_indent(text)
    expected = "\nx = 1\n\ny = 2\n\nz = 3\n"
    assert result == expected


if __name__ == "__main__":
    pytest.main()
