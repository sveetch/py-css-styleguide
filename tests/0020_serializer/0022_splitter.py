import pytest

from py_css_styleguide.exceptions import (
    SerializerError,
    StyleguideUserWarning,
)
from py_css_styleguide.serializer import ManifestSerializer


@pytest.mark.parametrize("value, mode, cleaner, expected", [
    # White space separator
    ("", "white-space", None, []),
    ("", "white-space", "whitespaces", []),
    ("foo", "white-space", None, ["foo"]),
    ("foo bar", "white-space", None, ["foo", "bar"]),
    ("foo bar", "white-space", "whitespaces", ["foo", "bar"]),
    (
        "foo bar téléphone maison",
        "white-space",
        None,
        ["foo", "bar", "téléphone", "maison"],
    ),
    (
        "foo   bar  téléphone   maison",
        "white-space",
        None,
        ["foo", "", "", "bar", "", "téléphone", "", "", "maison"],
    ),
    (
        "foo   bar  téléphone   maison",
        "white-space",
        "whitespaces",
        ["foo", "bar", "téléphone", "maison"],
    ),
    # JSON list parsing
    ("[]", "object-list", None, []),
    ('["foo"]', "object-list", None, ["foo"]),
    ('["foo\'", "bar"]', "object-list", None, ["foo'", "bar"]),
    (
        '["foo", "ping pong", "bar", "téléphone"]',
        "object-list",
        None,
        ["foo", "ping pong", "bar", "téléphone"],
    ),
])
def test_value_splitter_success(value, mode, cleaner, expected):
    serializer = ManifestSerializer()

    data = serializer.value_splitter(
        "ref",
        "prop",
        value,
        mode,
        cleaner=cleaner,
    )
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


@pytest.mark.parametrize("value, mode", [
    # Invalid syntax
    ("[", "object-list")
])
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
