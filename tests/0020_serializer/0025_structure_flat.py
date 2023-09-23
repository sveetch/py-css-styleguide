from collections import OrderedDict

import pytest

from py_css_styleguide.exceptions import SerializerError
from py_css_styleguide.serializer import ManifestSerializer


@pytest.mark.parametrize(
    "context,expected,order",
    [
        (
            OrderedDict((("keys", "black white"), ("values", "#000000 #ffffff"))),
            OrderedDict((("black", "#000000"), ("white", "#ffffff"))),
            ["black", "white"],
        ),
        (
            OrderedDict(
                (("keys", "black white red"), ("values", "#000000 #ffffff #ff0000"))
            ),
            OrderedDict(
                (("black", "#000000"), ("white", "#ffffff"), ("red", "#ff0000"))
            ),
            ["black", "white", "red"],
        ),
        (
            OrderedDict(
                (
                    ("keys", "cyan black white red"),
                    ("values", "#48999b #000000 #ffffff #ff0000"),
                )
            ),
            OrderedDict(
                (
                    ("cyan", "#48999b"),
                    ("black", "#000000"),
                    ("white", "#ffffff"),
                    ("red", "#ff0000"),
                )
            ),
            ["cyan", "black", "white", "red"],
        ),
        # keys/values only in flat mode, everything else is ignored
        (
            OrderedDict(
                (
                    ("keys", "black white"),
                    ("values", "#000000 #ffffff"),
                    ("dummy", "whatever"),
                )
            ),
            OrderedDict((("black", "#000000"), ("white", "#ffffff"))),
            ["black", "white"],
        ),
        # With JSON list splitter and mixed types
        (
            OrderedDict(
                (
                    ("splitter", "object-list"),
                    ("keys", '["black", "integer", "false", "null"]'),
                    ("values", '["#000000", 42, false, null]'),
                )
            ),
            OrderedDict((
                ("black", "#000000"),
                ("integer", 42),
                ("false", False),
                ("null", None),
            )),
            ["black", "integer", "false", "null"],
        ),
    ],
)
def test_serialize_to_flat_success(context, expected, order):
    serializer = ManifestSerializer()

    serialized = serializer.serialize_to_flat("foo", context)

    assert serialized == expected
    assert order == list(serialized.keys())


@pytest.mark.parametrize(
    "context",
    [
        # Missing 'keys'
        {"values": "#000000 #ffffff"},
        # Missing 'values'
        {"keys": "black white"},
        # Length differences between keys and values
        {"keys": "black white red", "values": "#000000"},
    ],
)
def test_serialize_to_flat_error(context):
    serializer = ManifestSerializer()

    with pytest.raises(SerializerError):
        serializer.serialize_to_flat("foo", context)
