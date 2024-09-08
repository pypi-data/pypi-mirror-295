import pytest
from crimson.templator import format_indent


def test_no_safe_flag_indent():
    kwargs = {
        "arg1": """\
I want to write very long lines
1
2
3
even 4!\
"""
    }
    template = r"""
    \{arg1\}
"""
    expected_formatted = """
    I want to write very long lines
    1
    2
    3
    even 4!
"""

    formatted = format_indent(template, open=r"\{", close=r"\}", safe=True, **kwargs)

    assert expected_formatted == formatted


def test_allow_to_add_additional_text_after_pattern():
    kwargs = {"arg1": "line1\nline2"}
    template = r"""
    \{arg1\} Additional text with indent will cause an error.
"""

    formatted = format_indent(template, **kwargs, safe=True)

    expected = """
    line1
    line2 Additional text with indent will cause an error.
"""

    assert formatted == expected
