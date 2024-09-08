from typing import Dict, Any, List, Union, Tuple, Generic, TypeVar
from ._utils import (
    add_prefix,
    convert_dict_of_lists_to_list_of_dicts,
)
from crimson.intelli_type import IntelliType
from .__RemoveLines import _RemoveLines

T = TypeVar("T")

# region Types


class Template_(IntelliType, str, Generic[T]):
    r"""
    Template used with special brackets, such as:
        - insert: `\[keyword\]`
        - indent: `\{keyword\}`
        - indent_loop: `\\[keyword\\]`

    The brackets can be customized.

    It must be used with r.
        - example:

        ```python
        template = r'''
        \[name\] : \[age\]
        '''
        ```
    """


class bool_:
    pass


class Safe_(IntelliType, bool_, Generic[T]):
    """
    If it is true,

    values of kwargs are passed enclosed by str.
        - value = str(value)
    """

    annotation = bool


class Open_(IntelliType, str, Generic[T]):
    """
    It should be symmetric with Close_.
    It was planned to be flexible, but only default settings are tested.
    """


class Close_(IntelliType, str, Generic[T]):
    """
    It should be symmetric with Open_.
    It was planned to be flexible, but only default settings are tested.
    """


class Union_(Tuple):
    """
    Dummy of Union.
    Tuple is used to mimic the structures used with Union.
    """


class Kwargs_(IntelliType, Dict[str, Union_[str, Any]], Generic[T]):
    """
    It is designed to use the format functions similar to `str.format`.

    It Safe_ is True, Dict[str, str],
    else if Safe_ is False, Dict[str, Any],

    Example:\n
        ```python
        kwargs: Kwargs_
        format_insert(template, **kwargs)
        ```
    """

    annotation = Dict[str, Union[str, Any]]


class Kwargs_List_(
    IntelliType,
    Union_[List[Kwargs_], Dict[str, List[Union_[str, Any]]]],
    Generic[T],
):
    """
    Note that it is used as a positional arg unlike Kwargs_.

    Example:\n
        ```python
        kwargs: Kwargs_List_ = {
            "name": ["John", "Maria"],
            "age": [20, 30]
        }

        # or

        kwargs: Kwargs_List_ = [
            {"name": "John, "age": 20},
            {"name": "Maria, "age": 30},
        ]

        format_insert_loop(template, kwargs)
        ```
    """

    annotation = Union[List[Kwargs_], Dict[str, List[Union[str, Any]]]]


class CutEnds_(IntelliType, Tuple[int, int], Generic[T]):
    """
    The formatted template is returned as:
        `cut_ends = (1, 1)`

        `return formatted[cut_ends[0]: -cut_ends[1]]`

    Even if `cut_ends[1]` is 0, `None` is used instead of `-cut_ends[1]`.
    """


# endregion

# region Public Functions


def format_insert(
    template: Template_[str],
    open: Open_[str] = r"\[",
    close: Close_[str] = r"\]",
    safe: Safe_[bool] = True,
    **kwargs: Kwargs_[Dict[str, Union[str, Any]]],
):
    r"""
    Example:
        Script:
        ```python
        template = r'''
        \[arg1\]
        '''
        format_insert(
            template,
            {"arg1": "Hello world!"}
        )
        ```
        Output:
        ```
        Hello world!
        ```
    """
    for key, value in kwargs.items():
        if safe:
            value = _convert_to_str(value)

        pattern = open + key + close
        template = template.replace(pattern, value)

    return template


def format_indent(
    template: Template_[str],
    open: Open_[str] = r"\{",
    close: Close_[str] = r"\}",
    safe: Safe_[bool] = True,
    **kwargs: Kwargs_[Dict[str, Union[str, Any]]],
):
    r"""
    Example:
        Script:
        ```python
        template = r'''
        No intent line
            \{indented\}
        '''
        format_indent(
            template,
            {"indented": "Indented Line1\nIndented Line2\n"}
        )
        ```
        Output:
        ```
        No intent line
            Indented Line1
            Indented Line2
        ```
    """
    for key, value in kwargs.items():
        if safe:
            value = _convert_to_str(value)
        template = _format_indent_single(template, key, value, open, close)

    return template


def format_insert_loop(
    template: Template_[str],
    kwargs_list: Kwargs_List_[Union[List[Kwargs_], Dict[str, List[Union[str, Any]]]]],
    open: Open_[str] = r"\\[",
    close: Close_[str] = r"\\]",
    safe: Safe_[bool] = True,
    cut_ends: Tuple[int, int] = (0, 0),
):
    r"""
    Example:
        Script:
        ```python
        template = r'''
        \\[name\\]: \\[age\\]:
        '''
        format_indent(
            template,
            kwargs_list = {"name": ["John", "Maria"], {"age": [20, 30]}
        )
        ```
        Output:
        ```
        No intent line
            Indented Line1
            Indented Line2
        ```
    """
    parsers = [_format_insert_loop_many, _format_insert_loop_list]
    errors = []

    for parser in parsers:
        try:
            return parser(template, kwargs_list, open, close, safe, cut_ends)
        except Exception as e:
            errors.append(f"{parser.__name__} error: {e}")
            continue

    raise ValueError(
        "Both format_insert_loop_many and format_insert_loop_legacy failed with errors: "
        + "; ".join(errors)
    )


def remove_lines(template: str, open: str = r"\(", close: str = r"\)") -> str:
    """
    Not documented. Can be deprecated.
    """
    return _RemoveLines.remove_lines(template, open, close)


# endregion

# region Private Functions


def _format_insert_loop_many(
    template: str,
    kwargs_many: Dict[str, List[str]],
    open: str = r"\\[",
    close: str = r"\\]",
    safe: bool = True,
    cut_ends: Tuple[int, int] = (0, 0),
):
    kwargs_list = convert_dict_of_lists_to_list_of_dicts(kwargs_many)

    return _format_insert_loop_list(template, kwargs_list, open, close, safe, cut_ends)


def _format_insert_loop_list(
    template: str,
    kwargs_list: List[Dict[str, str]],
    open: str = r"\\[",
    close: str = r"\\]",
    safe: bool = True,
    cut_ends: Tuple[int, int] = (0, 0),
):
    formatteds = []

    for kwargs in kwargs_list:
        formatted = format_insert(template, open, close, safe, **kwargs)
        formatteds.append(formatted)

    formatted_lines = "\n".join(formatteds).splitlines()

    cut_end = -cut_ends[1] if cut_ends[1] != 0 else None
    formatted_lines = formatted_lines[cut_ends[0] : cut_end]

    formatted = "\n".join(formatted_lines)

    return formatted


def _convert_to_str(value: Any):
    return str(value)


def _format_indent_single(
    text: str,
    key: str,
    value: str,
    open: str = r"\{",
    close: str = r"\}",
):
    pattern = open + key + close
    new_lines = []
    for line in text.split("\n"):
        if line.find(pattern) != -1:
            remaining_text = get_remaining_text(line, pattern)
            # _check_indent_line(line, pattern)
            indent = line[: line.find(pattern)]
            formatted_text = add_prefix(value, indent) + remaining_text
            new_lines.append(formatted_text)
        else:
            new_lines.append(line)

    return "\n".join(new_lines)


def get_remaining_text(line: str, pattern: str):
    line = line.lstrip()
    remaining_text = line.replace(pattern, "")
    return remaining_text


def _check_indent_line(text: str, pattern: str):
    remaining_text = text.replace(pattern, "").strip()

    if remaining_text:
        raise ValueError(f"The line contains characters other than '{pattern}'")

    return True


# endregion
