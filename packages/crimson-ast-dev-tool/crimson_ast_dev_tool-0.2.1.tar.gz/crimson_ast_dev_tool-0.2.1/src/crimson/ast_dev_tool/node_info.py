from typing import List, TypedDict
import ast


class Position(TypedDict, total=False):
    lineno: int
    end_lineno: int
    col_offset: int
    end_col_offset: int


class NodeWithInfo(TypedDict):
    node: ast.AST
    position: Position


def extend_positions(nodes: List[ast.AST]) -> List[NodeWithInfo]:
    nodes_data = []

    keys = Position.__annotations__.keys()

    for node in nodes:
        try:
            position = {}
            for key in keys:
                position[key] = getattr(node, key)
            nodes_data.append({"node": node, "position": position})
        except Exception as _:
            print(f"Node, {node}, doesn't have position data.")
            nodes_data.append({"node": node})
            _
    return nodes_data
