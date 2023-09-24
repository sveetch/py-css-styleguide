import pytest

from py_css_styleguide.parser import TinycssSourceParser
from py_css_styleguide.exceptions import ParserErrors


@pytest.mark.parametrize(
    "source,expected",
    [
        # Basic single line
        ('.styleguide-foo{content: "yep"}', {"styleguide-foo": {"content": "yep"}}),
        # Basic CSS variable
        ('.styleguide-foo{--myvar: "ping"}', {"styleguide-foo": {"myvar": "ping"}}),
        # Multiple rules
        (
            (
                '.styleguide-foo{ content: "yep"; quote: "pika" } '
                '.styleguide-bar{content: "hola"}'
            ),
            {
                "styleguide-bar": {"content": "hola"},
                "styleguide-foo": {"content": "yep", "quote": "pika"},
            },
        ),
        # Multiple rules on multiple lines
        (
            (
                ".styleguide-foo{\n"
                '    content: "yep";\n'
                '    quote: "pika"\n'
                "}\n"
                "\n"
                ".styleguide-bar{\n"
                '    content: "hola"\n'
                "}"
            ),
            {
                "styleguide-bar": {"content": "hola"},
                "styleguide-foo": {"content": "yep", "quote": "pika"},
            },
        ),
    ],
)
def test_css_parser(source, expected):
    """
    Ensure TinyCSS parsing is still working as expected.
    """
    parser = TinycssSourceParser()
    rules = parser.parse(source)

    assert rules == expected


def test_css_parser_no_references():
    """
    Valid CSS without any reference should succeed and just returns an empty
    OrderedDict.
    """
    parser = TinycssSourceParser()
    rules = parser.parse((
        ".foo { content: \"bar\"; }\n"
        ".zip {\n"
        "    font-size: 1rem;\n"
        "    color: #ffffff;\n"
        "}\n"
    ))

    assert rules == {}


def test_css_parser_naivety():
    """
    Demonstrate that parse is pretty naive and would accept many invalid syntax.
    """
    parser = TinycssSourceParser()
    rules = parser.parse((
        "n##{ope\n"
        ".ping { pong }\n"
        ".zip {\n"
        "    font-size: 1rem;\n"
        ".foo { content: \"bar\"; }\n"
        "    color: #ffffff;\n"
        "}\n"
    ))

    assert rules == {}


def test_css_parser_error():
    """
    Parser should raise explicit ParserErrors with error details in its
    'error_payload' attribute.
    """
    parser = TinycssSourceParser()
    error = payload = None

    try:
        parser.parse("nope")
    except ParserErrors as e:
        error = e
        payload = e.error_payload

    assert str(error) == "Unable to parse CSS due to 1 parsing error(s)"
    assert payload == [
        (
            "Line 1 - Column 1 : [invalid] EOF reached before {} block for a "
            "qualified rule."
        )
    ]
