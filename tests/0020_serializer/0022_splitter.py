import pytest

from py_css_styleguide.exceptions import (
    SerializerError,
    StyleguideUserWarning,
)
from py_css_styleguide.serializer import ManifestSerializer


@pytest.mark.parametrize(
    "value, mode, expected",
    [
        # White space separator
        ("", "white-space", []),
        ("foo", "white-space", ["foo"]),
        ("foo bar", "white-space", ["foo", "bar"]),
        (
            "foo bar téléphone maison",
            "white-space",
            ["foo", "bar", "téléphone", "maison"],
        ),
        ("foo bar téléphone-maison", "white-space", ["foo", "bar", "téléphone-maison"]),
        # TODO: simple whitespace splitting should be normalized so we dont accept
        # whitespace as value
        (
            "foo   bar  téléphone   maison",
            "white-space",
            ["foo", "", "", "bar", "", "téléphone", "", "", "maison"],
        ),
        # JSON list parsing
        ("[]", "object-list", []),
        ('["foo"]', "object-list", ["foo"]),
        ('["foo\'", "bar"]', "object-list", ["foo'", "bar"]),
        (
            '["foo", "ping pong", "bar", "téléphone"]',
            "object-list",
            ["foo", "ping pong", "bar", "téléphone"],
        ),
    ],
)
def test_value_splitter_success(value, mode, expected):
    serializer = ManifestSerializer()

    data = serializer.value_splitter("ref", "prop", value, mode)

    assert data == expected


def test_value_splitter_deprecated_jsonlist():
    """
    Usage of 'json-list' splitter should works but emit a deprecation warning.
    """
    value = '["foo"]'
    mode = "json-list"
    expected = ["foo"]
    serializer = ManifestSerializer()

    with pytest.warns(StyleguideUserWarning):
        data = serializer.value_splitter("ref", "prop", value, mode)

    assert data == expected


@pytest.mark.parametrize(
    "value,mode",
    [
        # Invalid syntax
        ("[", "object-list")
    ],
)
def test_value_splitter_error(value, mode):
    serializer = ManifestSerializer()

    with pytest.raises(SerializerError):
        serializer.value_splitter("ref", "prop", value, mode)


def test_serialize_to_json_deprecated():
    """
    Usage of 'serialize_to_json' splitter should works but emit a deprecation warning.
    """
    context = {"object": '{"foo": "bar", "plop": {"ping": "pang", "pong": "pung"}}'}
    expected = {"foo": "bar", "plop": {"ping": "pang", "pong": "pung"}}
    serializer = ManifestSerializer()

    with pytest.warns(StyleguideUserWarning):
        serialized = serializer.serialize_to_json("foo", context)

    assert serialized == expected
