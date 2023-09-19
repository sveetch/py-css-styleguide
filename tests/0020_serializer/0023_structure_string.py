import pytest

from py_css_styleguide.exceptions import SerializerError
from py_css_styleguide.serializer import ManifestSerializer


@pytest.mark.parametrize(
    "context,expected",
    [
        # Basic string
        ({"value": "ok"}, "ok"),
        # Empty string is ok
        ({"value": ""}, ""),
        # Looks like a space separated list but it's a string
        ({"value": "black white"}, "black white"),
        # Some unicode
        ({"value": "¿ pœp ?"}, "¿ pœp ?"),
    ],
)
def test_serialize_to_string_success(context, expected):
    serializer = ManifestSerializer()

    serialized = serializer.serialize_to_string("foo", context)

    assert serialized == expected


@pytest.mark.parametrize(
    "context",
    [
        # Missing 'value'
        {"content": "nope"},
        # None value for when variable is not defined
        {"value": None},
    ],
)
def test_serialize_to_string_error(context):
    serializer = ManifestSerializer()

    with pytest.raises(SerializerError):
        serializer.serialize_to_string("foo", context)
