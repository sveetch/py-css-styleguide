import pytest

from py_css_styleguide.exceptions import SerializerError
from py_css_styleguide.serializer import ManifestSerializer


@pytest.mark.parametrize(
    "context,expected",
    [
        # Null value
        ({"object": "null"}, None),
        # Boolean list
        ({"object": "true"}, True),
        # Empty list
        ({"object": "[]"}, []),
        # Empty dict
        ({"object": "{}"}, {}),
        # Simple list and encoding
        ({"object": '["foo", "téléphone"]'}, ["foo", "téléphone"]),
        # Simple dict
        ({"object": '{"foo": "ping", "bar": "pong"}'}, {"foo": "ping", "bar": "pong"}),
        # Nested dict
        (
            {"object": '{"foo": "bar", "plop": {"ping": "pang", "pong": "pung"}}'},
            {"foo": "bar", "plop": {"ping": "pang", "pong": "pung"}},
        ),
        # Various type in a dict
        (
            {
                "object": (
                    """{"foo": "bar", "life": 42, "moo": true,"""
                    """"plop": ["ping", "pong"]}"""
                )
            },
            {"foo": "bar", "life": 42, "moo": True, "plop": ["ping", "pong"]},
        ),
    ],
)
def test_serialize_to_complex_success_libsass(context, expected):
    """
    Valid content with JSON parser for libsass support should be properly deserialized
    as expected.
    """
    serializer = ManifestSerializer(compiler_support="libsass")

    serialized = serializer.serialize_to_complex("foo", context)

    assert serialized == expected


@pytest.mark.parametrize(
    "context,expected",
    [
        # Null value
        ({"object": "None"}, None),
        # Boolean list
        ({"object": "True"}, True),
        # Empty list
        ({"object": "[]"}, []),
        # Empty dict
        ({"object": "{}"}, {}),
        # Simple list and encoding
        ({"object": '["foo", "téléphone"]'}, ["foo", "téléphone"]),
        ({"object": "['foo', 'téléphone']"}, ["foo", "téléphone"]),
        # Simple dict
        ({"object": '{"foo": "ping", "bar": "pong"}'}, {"foo": "ping", "bar": "pong"}),
        # Nested dict
        (
            {"object": '{"foo": "bar", "plop": {"ping": "pang", "pong": "pung"}}'},
            {"foo": "bar", "plop": {"ping": "pang", "pong": "pung"}},
        ),
        # Various type in a dict
        (
            {
                "object": (
                    """{"foo": "bar", "life": 42, "moo": True,"""
                    """"plop": ["ping", "pong"]}"""
                )
            },
            {"foo": "bar", "life": 42, "moo": True, "plop": ["ping", "pong"]},
        ),
    ],
)
def test_serialize_to_complex_success_dartsass(context, expected):
    """
    Valid content with Python AST parser for dart-sass support should be properly
    deserialized as expected.
    """
    serializer = ManifestSerializer(compiler_support="dartsass")

    serialized = serializer.serialize_to_complex("foo", context)

    assert serialized == expected


@pytest.mark.parametrize(
    "context",
    [
        # Missing 'object'
        {"value": "#000000 #ffffff"},
        # Empty object
        {"object": ""},
        # Single quote encoding issue
        {"object": "['foo']"},
        # Syntax error
        {"object": '["foo"'},
    ],
)
def test_serialize_to_complex_libsass_error(context):
    serializer = ManifestSerializer(compiler_support="libsass")
    with pytest.raises(SerializerError):
        serializer.serialize_to_complex("refname", context)


@pytest.mark.parametrize(
    "context",
    [
        # Missing 'object'
        {"value": "#000000 #ffffff"},
        # Empty object
        {"object": ""},
        # Syntax error
        {"object": '["foo"'},
    ],
)
def test_serialize_to_complex_dartsass_error(context):
    serializer = ManifestSerializer(compiler_support="dartsass")
    with pytest.raises(SerializerError):
        serializer.serialize_to_complex("refname", context)
