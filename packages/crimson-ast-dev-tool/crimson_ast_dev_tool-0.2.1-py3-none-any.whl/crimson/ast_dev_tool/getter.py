from types import ModuleType, FunctionType, MethodType
from typing import Union, Type
import ast
from ast import parse
from typing import overload
from inspect import getsource
from .util import clean_indent
# object, source, node

_SourceObjectType = Union[ModuleType, Type, FunctionType, MethodType]
# type is for the type of classes
_SourceObjectTypes = (ModuleType, Type, FunctionType, MethodType, type)


@overload
def get_node(object: _SourceObjectType) -> ast.AST:
    ...


@overload
def get_node(source: str) -> ast.AST:
    ...


def get_node(target: Union[object, str]) -> ast.AST:
    if type(target) is str:
        source = target
    elif type(target) in _SourceObjectTypes:
        source = getsource(object=target)
    else:
        raise Exception('Input is not valid')

    source = clean_indent(source, return_type='str')

    node = _get_node(source)

    return node


def _get_node(source: str) -> ast.AST:
    tree = parse(source)
    return tree
