from typing import List, Type, Literal, Union, overload
import ast
from ast import unparse
from .getter import get_node, _SourceObjectTypes, _SourceObjectType


class NodeCollector(ast.NodeVisitor):
    def __init__(self, node_type: Type[ast.AST]):
        self.node_type = node_type
        self.nodes = []

    def visit(self, node: ast.AST):
        if isinstance(node, self.node_type):
            self.nodes.append(node)
        self.generic_visit(node)


@overload
def collect_nodes(
    node: ast.AST,
    node_type: Type[ast.AST],
    return_type: Literal["nodes", "sources"] = "nodes",
) -> Union[List[ast.AST], List[str]]:
    """The shape of the sources are not preserved"""
    ...


@overload
def collect_nodes(
    source: str,
    node_type: Type[ast.AST],
    return_type: Literal["nodes", "sources"] = "nodes",
) -> Union[List[ast.AST], List[str]]:
    """The shape of the sources are not preserved"""
    ...


@overload
def collect_nodes(
    object: _SourceObjectType,
    node_type: Type[ast.AST],
    return_type: Literal["nodes", "sources"] = "nodes",
) -> Union[List[ast.AST], List[str]]:
    """The shape of the sources are not preserved"""
    ...


def collect_nodes(
    input: Union[str, ast.AST, _SourceObjectType],
    node_type: Type[ast.AST],
    return_type: Literal["nodes", "sources"] = "nodes",
) -> Union[List[ast.AST], List[str]]:

    if any([type(input) is str, type(input) in _SourceObjectTypes]):
        node = get_node(input)
    elif isinstance(input, ast.AST):
        node = input
    else:
        raise Exception("Input is not valid")

    collector = NodeCollector(node_type)
    collector.visit(node)
    nodes = collector.nodes

    if return_type == "nodes":
        pass
    elif return_type == "sources":
        nodes = [unparse(node) for node in nodes]

    return nodes
