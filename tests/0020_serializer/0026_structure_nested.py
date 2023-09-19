import pytest

from py_css_styleguide.exceptions import SerializerError
from py_css_styleguide.serializer import ManifestSerializer


@pytest.mark.parametrize(
    "context,expected",
    [
        # Nested mode with single property and ensure 'structure' is an ignored
        # keyword
        (
            {
                "keys": "black white",
                "value": "#000000 #ffffff",
                "structure": "whatever",
            },
            {"black": {"value": "#000000"}, "white": {"value": "#ffffff"}},
        ),
        # Nested mode with multiple property
        (
            {
                "keys": "black white",
                "selectors": ".bg-black .bg-white",
                "values": "#000000 #ffffff",
            },
            {
                "black": {"selectors": ".bg-black", "values": "#000000"},
                "white": {"selectors": ".bg-white", "values": "#ffffff"},
            },
        ),
        # With JSON list splitter
        (
            {
                "keys": '["black", "white"]',
                "value": '["#000000", "#ffffff"]',
                "structure": "whatever",
                "splitter": "object-list",
            },
            {"black": {"value": "#000000"}, "white": {"value": "#ffffff"}},
        ),
    ],
)
def test_serialize_to_nested_success(context, expected):
    serializer = ManifestSerializer()

    serialized = serializer.serialize_to_nested("foo", context)

    assert serialized == expected


@pytest.mark.parametrize(
    "context",
    [
        # Missing 'keys'
        {"value": "#000000 #ffffff"},
        # Length difference with keys
        {"keys": "black white", "selectors": ".bg-black"},
    ],
)
def test_serialize_to_nested_error(context):
    serializer = ManifestSerializer()

    with pytest.raises(SerializerError):
        serializer.serialize_to_nested("foo", context)
