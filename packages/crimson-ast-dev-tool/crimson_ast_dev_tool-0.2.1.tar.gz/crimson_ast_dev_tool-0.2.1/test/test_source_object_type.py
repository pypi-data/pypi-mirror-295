from crimson.ast_dev_tool.getter import _SourceObjectTypes


class A:
    def __init__(self):
        pass

    def func1(self, arg1: int, arg2: str) -> str:
        return str(arg1) + arg2

    def func2(self, arg1: int, arg2: int) -> int:
        return arg1 + arg2


def example_function():
    pass


def test_is_function():
    assert type(example_function) in _SourceObjectTypes


def test_is_class():
    assert type(A) in _SourceObjectTypes


def test_is_method():
    a = A()
    assert type(a.func1) in _SourceObjectTypes


def test_is_not_source_object():
    assert type("some string") not in _SourceObjectTypes
    assert type(42) not in _SourceObjectTypes
    assert type(None) not in _SourceObjectTypes
    assert str not in _SourceObjectTypes
    assert int not in _SourceObjectTypes
    assert bool not in _SourceObjectTypes


if __name__ == "__main__":
    import pytest

    pytest.main()
