import pytest

from py_css_styleguide.exceptions import SerializerError
from py_css_styleguide.serializer import ManifestSerializer


@pytest.mark.parametrize(
    "context,expected",
    [
        # Single item list
        ({"items": "black"}, ["black"]),
        # Empty list is ok
        ({"items": ""}, []),
        # Multiple list items
        ({"items": "black white"}, ["black", "white"]),
        # Many items
        (
            {"items": "1 2 3 4 5 6 7 8 9 0"},
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
        ),
        # With JSON list splitter
        (
            {"splitter": "object-list", "items": '["black", "white"]'},
            ["black", "white"],
        ),
    ],
)
def test_serialize_to_list_success(context, expected):
    serializer = ManifestSerializer()

    serialized = serializer.serialize_to_list("foo", context)

    assert serialized == expected


@pytest.mark.parametrize(
    "context",
    [
        # Missing 'items'
        {"values": "#000000 #ffffff"},
        # None value although it can occurs from parsed data because it happen
        # only if 'items' is not defined
        {"items": None},
    ],
)
def test_serialize_to_list_error(context):
    serializer = ManifestSerializer()

    with pytest.raises(SerializerError):
        serializer.serialize_to_list("foo", context)
