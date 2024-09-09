from typing import List, Union, Literal, Optional, overload
from pydantic import BaseModel
import ast


class _TypeChecker(BaseModel):
    str_list: List[str]


def safe_unparse(node: Optional[ast.AST]) -> Optional[str]:
    if node is not None:
        output = ast.unparse(node)
    else:
        output = None
    return output


def _check_str_list(input):
    passed = None
    try:
        _TypeChecker(str_list=input)
        passed = True
    except Exception:
        passed = False
    return passed


@overload
def clean_indent(
    lines: List[str], return_type: Literal["str", "lines"] = "str"
) -> Union[str, List[str]]:
    """doc"""
    ...


@overload
def clean_indent(
    text: str, return_type: Literal["str", "lines"] = "str"
) -> Union[str, List[str]]:
    """doc"""
    ...


def clean_indent(
    input: Union[str, List[str]],
    return_type: Literal["str", "lines"] = "str",
) -> Union[str, List[str]]:
    if type(input) is str:
        lines = input.splitlines()
    elif _check_str_list(input):
        lines = input

    lines = _clean_indent(lines)

    if return_type == "str":
        output = "\n".join(lines)
    elif return_type == "lines":
        output = lines

    return output


def _count_indent(line: str) -> Optional[int]:
    ori = len(line)
    cleaned = len(line.strip())

    if cleaned == 0:
        count = None
    else:
        count = ori - cleaned

    return count


def _clean_indent(lines: List[str]) -> List[str]:
    min_indent = min(
        [_count_indent(line) for line in lines if _count_indent(line) is not None]
    )
    new_lines = []

    if min_indent == 0:
        new_lines = lines
    else:
        for line in lines:
            new_lines.append(line[min_indent:])

    return new_lines
