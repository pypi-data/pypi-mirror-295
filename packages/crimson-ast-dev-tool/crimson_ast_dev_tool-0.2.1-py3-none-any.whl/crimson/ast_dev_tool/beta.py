from typing import List, Union, Literal, overload
from pydantic import BaseModel


class _TypeChecker(BaseModel):
    str_list: List[str]


def _check_str_list(input):
    passed = None
    try:
        _TypeChecker(str_list=input)
        passed = True
    except Exception:
        passed = False
    return passed


@overload
def add_indent(
    lines: List[str], indent: int = 4, return_type: Literal["str", "lines"] = "str"
) -> Union[str, List[str]]:
    """doc"""
    ...


@overload
def add_indent(
    text: str, indent: int = 4, return_type: Literal["str", "lines"] = "str"
) -> Union[str, List[str]]:
    """doc"""
    ...


def add_indent(
    input: Union[str, List[str]],
    indent: int = 4,
    return_type: Literal["str", "lines"] = "str",
) -> Union[str, List[str]]:
    if type(input) is str:
        lines = input.splitlines()
    elif _check_str_list(input):
        lines = input

    lines = _add_indent(lines, indent)

    if return_type == "str":
        output = "\n".join(lines)
    elif return_type == "lines":
        pass

    return output


def _add_indent(lines: List[str], indent: int = 4) -> List[str]:
    new_lines = []
    for line in lines:
        new_lines.append(" " * indent + line)
    return new_lines


def insert_text(index: int, indent: int, text: str, new_text: str):
    lines = text.splitlines()
    new_lines = new_text.splitlines()

    new_lines = add_indent(new_lines, indent=indent)

    lines = lines[:index] + new_lines + lines[index:]
    text = "\n".join(lines)
    return text


def replace_text(start: int, end: int, indent: int, text: str, new_text: str):
    lines = text.splitlines()
    new_lines = new_text.splitlines()

    new_lines = add_indent(new_lines, indent=indent)

    lines = lines[:start] + new_lines + lines[end:]
    text = "\n".join(lines)
    return text
