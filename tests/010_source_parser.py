# -*- coding: utf-8 -*-
import pytest

from py_css_styleguide.parser import TinycssSourceParser


@pytest.mark.parametrize('source,expected', [
    # Basic single line
    (
        '.styleguide-foo{content: "yep"}',
        {
            "styleguide-foo": {
                "content": "yep",
            }
        },
    ),
    # Basic CSS variable
    (
        '.styleguide-foo{--myvar: "ping"}',
        {
            "styleguide-foo": {
                "myvar": "ping",
            }
        },
    ),
    # Multiple rules
    (
        (
            '.styleguide-foo{ content: "yep"; quote: "pika" } '
            '.styleguide-bar{content: "hola"}'
        ),
        {
            "styleguide-bar": {
                "content": "hola"
            },
            "styleguide-foo": {
                "content": "yep",
                "quote": "pika"
            }
        },
    ),
    # Multiple rules on multiple lines
    (
        (
            '.styleguide-foo{\n'
            '    content: "yep";\n'
            '    quote: "pika"\n'
            '}\n'
            '\n'
            '.styleguide-bar{\n'
            '    content: "hola"\n'
            '}'
        ),
        {
            "styleguide-bar": {
                "content": "hola"
            },
            "styleguide-foo": {
                "content": "yep",
                "quote": "pika"
            }
        },
    ),
])
def test_source_parse(source, expected):
    """
    Ensure TinyCSS parsing is still as expected.
    """
    parser = TinycssSourceParser()
    rules = parser.parse(source)

    assert rules == expected
