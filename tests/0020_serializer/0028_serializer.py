from collections import OrderedDict

import pytest

from py_css_styleguide.exceptions import (
    SerializerError,
    StyleguideValidationError,
)
from py_css_styleguide.serializer import ManifestSerializer


@pytest.mark.parametrize(
    "name,context,expected",
    [
        # JSON object with a list
        (
            "palette",
            {
                "styleguide-reference-palette": {
                    "structure": "object-complex",
                    "object": '["foo", "bar"]',
                }
            },
            ["foo", "bar"],
        ),
        # Nested structure with single property
        (
            "palette",
            {
                "styleguide-reference-palette": {
                    "structure": "nested",
                    "keys": "black white",
                    "value": "#000000 #ffffff",
                }
            },
            {"black": {"value": "#000000"}, "white": {"value": "#ffffff"}},
        ),
        # Nested structure with multiple properties
        (
            "palette",
            {
                "styleguide-reference-palette": {
                    "structure": "nested",
                    "keys": "black white",
                    "value": "#000000 #ffffff",
                    "foo": "one two",
                }
            },
            {
                "black": {"value": "#000000", "foo": "one"},
                "white": {"value": "#ffffff", "foo": "two"},
            },
        ),
        # Flat structure
        (
            "palette",
            {
                "styleguide-reference-palette": {
                    "structure": "flat",
                    "keys": "black white",
                    "values": "#000000 #ffffff",
                },
                "styleguide-reference-dummy": {
                    "structure": "nested",
                    "keys": "foo",
                    "values": "bar"
                },
            },
            {"black": "#000000", "white": "#ffffff"},
        ),
        # List structure
        (
            "palette",
            {
                "styleguide-reference-palette": {
                    "structure": "list",
                    "items": "black white",
                },
                "styleguide-reference-dummy": {
                    "structure": "nested",
                    "keys": "foo",
                    "values": "bar"
                },
            },
            ["black", "white"],
        ),
        # String structure
        (
            "palette",
            {
                "styleguide-reference-palette": {"structure": "string", "value": "ok"},
                "styleguide-reference-dummy": {"keys": "foo", "values": "bar"},
            },
            "ok",
        ),
    ],
)
def test_get_reference_success(name, context, expected):
    serializer = ManifestSerializer()

    reference = serializer.get_reference(context, name)

    assert reference == expected


@pytest.mark.parametrize(
    "name,context,expected",
    [
        # Missing reference with single rule
        (
            "palette",
            {
                "styleguide-reference-foo": {
                    "structure": "nested",
                    "keys": "black white",
                    "value": "#000000 #ffffff",
                }
            },
            SerializerError,
        ),
        # Invalid property name
        (
            "palette",
            {
                "styleguide-reference-palette": {
                    "structure": "nested",
                    "keys": "black white",
                    "font-color": "red blue",
                    "value": "#000000 #ffffff",
                }
            },
            StyleguideValidationError,
        ),
        # Missing structure mode name
        (
            "palette",
            {
                "styleguide-reference-palette": {
                    "keys": "black white",
                    "values": "#000000 #ffffff",
                }
            },
            SerializerError,
        ),
        # Invalid structure mode name
        (
            "palette",
            {
                "styleguide-reference-palette": {
                    "structure": "whatever",
                    "keys": "black white",
                    "values": "#000000 #ffffff",
                }
            },
            SerializerError,
        ),
        # Missing required reference from enabled references
        (
            "foo",
            {
                "styleguide-reference-palette": {
                    "structure": "nested",
                    "keys": "black white",
                    "value": "#000000 #ffffff",
                },
                "styleguide-reference-bar": {
                    "structure": "nested",
                    "keys": "black white",
                    "value": "#000000 #ffffff",
                },
            },
            SerializerError,
        ),
    ],
)
def test_get_reference_error(name, context, expected):
    serializer = ManifestSerializer()

    with pytest.raises(expected):
        serializer.get_reference(context, name)


@pytest.mark.parametrize(
    "context,expected,order",
    [
        # Default nested structure for a reference
        (
            {
                "styleguide-metas-references": {"names": "palette"},
                "dummy": {"content": "foo"},
                "styleguide-reference-palette": {
                    "structure": "nested",
                    "keys": "black white",
                    "value": "#000000 #ffffff",
                    "selector": ".bg-black .bg-white",
                },
            },
            {
                "palette": {
                    "black": {"value": "#000000", "selector": ".bg-black"},
                    "white": {"value": "#ffffff", "selector": ".bg-white"},
                }
            },
            ["palette"],
        ),
        # Reference order comes from explicitely enabled reference names order
        (
            OrderedDict(
                (
                    ("styleguide-metas-references", {"names": "foo pika ping"}),
                    (
                        "styleguide-reference-ping",
                        {"structure": "string", "value": "pong"},
                    ),
                    (
                        "styleguide-reference-pika",
                        {"structure": "string", "value": "chu"},
                    ),
                    (
                        "styleguide-reference-foo",
                        {"structure": "string", "value": "bar"},
                    ),
                )
            ),
            {"foo": "bar", "pika": "chu", "ping": "pong"},
            ["foo", "pika", "ping"],
        ),
        # Every structure modes and splitter with automatic enabling
        (
            OrderedDict(
                (
                    ("styleguide-metas-references", {"auto": "true"}),
                    (
                        "styleguide-reference-palette",
                        {
                            "structure": "flat",
                            "keys": "black white",
                            "values": "#000000 #ffffff",
                        },
                    ),
                    (
                        "styleguide-reference-schemes",
                        {
                            "structure": "nested",
                            "keys": "black white gray25",
                            "background": "#000000 #ffffff #404040",
                            "font_color": "#ffffff #000000 #ffffff",
                            "selector": ".black .white .gray25",
                        },
                    ),
                    (
                        "styleguide-reference-spaces",
                        {"structure": "list", "items": "short normal large"},
                    ),
                    (
                        "styleguide-reference-version",
                        {"structure": "string", "value": "V42.0"},
                    ),
                    (
                        "styleguide-reference-jsonstruct",
                        {
                            "structure": "object-complex",
                            "object": '{"foo": "bar", "ping": "pong"}',
                        },
                    ),
                    (
                        "styleguide-reference-flatjson",
                        {
                            "structure": "flat",
                            "splitter": "object-list",
                            "keys": '["black", "white"]',
                            "values": '["#000000", "#ffffff"]',
                        },
                    ),
                )
            ),
            {
                "palette": {"black": "#000000", "white": "#ffffff"},
                "schemes": {
                    "black": {
                        "background": "#000000",
                        "selector": ".black",
                        "font_color": "#ffffff",
                    },
                    "gray25": {
                        "background": "#404040",
                        "selector": ".gray25",
                        "font_color": "#ffffff",
                    },
                    "white": {
                        "background": "#ffffff",
                        "selector": ".white",
                        "font_color": "#000000",
                    },
                },
                "spaces": ["short", "normal", "large"],
                "version": "V42.0",
                "jsonstruct": {"foo": "bar", "ping": "pong"},
                "flatjson": {"black": "#000000", "white": "#ffffff"},
            },
            ["palette", "schemes", "spaces", "version", "jsonstruct", "flatjson"],
        ),
    ],
)
def test_get_enabled_references(context, expected, order):
    serializer = ManifestSerializer()

    enabled_references = serializer.get_meta_reference_names(context)
    references = serializer.get_enabled_references(context, enabled_references)

    assert expected == references
    assert order == list(references.keys())


@pytest.mark.parametrize(
    "context,expected",
    [
        # Basic test to check serialize() glue method is ok
        (
            {
                "styleguide-metas-references": {"names": "palette"},
                "dummy": {"content": "foo"},
                "styleguide-reference-palette": {
                    "structure": "flat",
                    "keys": "black white",
                    "values": "#000000 #ffffff",
                },
            },
            {"palette": {"black": "#000000", "white": "#ffffff"}},
        )
    ],
)
def test_serialize(context, expected):
    serializer = ManifestSerializer()

    references = serializer.serialize(context)

    assert references == expected
