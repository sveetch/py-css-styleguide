import pytest

from py_css_styleguide.exceptions import SerializerError
from py_css_styleguide.serializer import ManifestSerializer


@pytest.mark.parametrize(
    "context, expected, typed",
    [
        ({"value": "0"}, 0, int),
        ({"value": "4.2"}, 4.2, float),
        ({"value": "-4.2"}, -4.2, float),
        ({"value": "4.233336"}, 4.233336, float),
        ({"value": "42"}, 42, int),
        ({"value": "-42"}, -42, int),
    ],
)
def test_serialize_to_number_success(context, expected, typed):
    serializer = ManifestSerializer()

    serialized = serializer.serialize_to_number("foo", context)

    assert serialized == expected
    assert isinstance(serialized, typed) is True


@pytest.mark.parametrize(
    "context",
    [
        # Missing 'value'
        {"content": "nope"},
        # Invalid value
        {"value": "foo"},
        # Empty values
        {"value": ""},
        {"value": None},
    ],
)
def test_serialize_to_number_error(context):
    serializer = ManifestSerializer()

    with pytest.raises(SerializerError):
        serializer.serialize_to_number("foo", context)
