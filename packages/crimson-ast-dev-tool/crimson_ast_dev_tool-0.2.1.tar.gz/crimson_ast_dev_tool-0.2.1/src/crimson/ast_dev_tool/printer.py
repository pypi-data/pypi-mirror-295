from typing import Union
import ast
from typing import overload
from .getter import get_node, _SourceObjectType, _SourceObjectTypes


@overload
def print_node(node: ast.AST, indent=2) -> None:
    """doc"""
    ...


@overload
def print_node(source: str, indent=2) -> None:
    """doc"""
    ...


@overload
def print_node(object: _SourceObjectType, indent=2) -> None:
    """doc"""
    ...


def print_node(target: Union[ast.AST, str, _SourceObjectType], indent=2) -> None:
    if any([type(target) is str, type(target) in _SourceObjectTypes]):
        node = get_node(target)
    elif isinstance(target, ast.AST):
        node = target
    else:
        raise Exception("Input is not valid")

    _print_node(node, indent)


def _print_node(node: ast.AST, indent=2) -> None:
    print(ast.dump(node, indent=indent))
