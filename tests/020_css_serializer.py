# -*- coding: utf-8 -*-
import pytest

from py_css_styleguide.parser import TinycssSourceParser
from py_css_styleguide.serializer import SerializerError, ManifestSerializer


@pytest.mark.parametrize('name', [
    "palette",
    "foo_bar",
    "f123",
])
def test_validate_rule_name_success(name):
    serializer = ManifestSerializer()

    serializer.validate_rule_name(name)


@pytest.mark.parametrize('name', [
    "",
    "foo-bar",
    "foo-bar",
    "foo bar",
    "1foo",
    "fooé",
])
def test_validate_rule_name_error(name):
    serializer = ManifestSerializer()

    with pytest.raises(SerializerError):
        serializer.validate_rule_name(name)


@pytest.mark.parametrize('name', [
    "palette",
    "foo_bar",
    "f123",
])
def test_validate_property_name_success(name):
    serializer = ManifestSerializer()

    serializer.validate_property_name(name)


@pytest.mark.parametrize('name', [
    "",
    "foo-bar",
    "foo-bar",
    "foo bar",
    "1foo",
    "fooé",
])
def test_validate_property_name_error(name):
    serializer = ManifestSerializer()

    with pytest.raises(SerializerError):
        serializer.validate_property_name(name)


def test_format_value_dontexists():
    """
    Check error about unexisting required value to format
    """
    serializer = ManifestSerializer()

    data = {}

    with pytest.raises(SerializerError):
        serializer.format_value(data, 'nope')


def test_format_value_unsupported():
    """
    Check error about unsupported format name
    """
    serializer = ManifestSerializer()

    data = {
        'ping': 'pong',
        'ping-format': "nope",
    }

    with pytest.raises(SerializerError):
        serializer.format_value(data, 'nope')


@pytest.mark.parametrize('context,attempted', [
    # Default coerce to a list
    (
        {
            'names': "palette",
        },
        ["palette"],
    ),
    # Formerly asked a string
    (
        {
            'names': "palette",
            'names-format': "string",
        },
        "palette",
    ),
    # Formerly asked a list
    (
        {
            'names': "palette",
            'names-format': "list",
        },
        ["palette"],
    ),
    # Multiple items
    (
        {
            'names': "palette schemes foo bar",
        },
        ["palette", "schemes", "foo", "bar"],
    ),
])
def test_format_value_success(context, attempted):
    serializer = ManifestSerializer()

    data = serializer.format_value(context, 'names')

    assert data == attempted


@pytest.mark.parametrize('context,attempted', [
    (
        {
            'styleguide-metas-references': {
                'names': "palette",
            },
            'dummy': {
                'names': "yip",
            },
        },
        ["palette"],
    ),
    (
        {
            'styleguide-metas-references': {
                'names': "palette schemes foo bar",
            }
        },
        ["palette", "schemes", "foo", "bar"],
    ),
])
def test_get_meta_references_success(context, attempted):
    serializer = ManifestSerializer()

    reference_names = serializer.get_meta_references(context)

    assert reference_names == attempted


@pytest.mark.parametrize('context', [
    # Missing references meta
    {
        'styleguide-metas-foo': {
            'names': "palette",
        }
    },
    # Missing names property
    {
        'styleguide-metas-references': {
            'content': "palette",
        }
    },
    # Invalid name
    {
        'styleguide-metas-references': {
            'content': "foo-bar",
        }
    },
    # Empty list
    {
        'styleguide-metas-references': {
            'names': "",
        }
    },
])
def test_get_meta_references_error(context):
    serializer = ManifestSerializer()

    with pytest.raises(SerializerError):
        serializer.get_meta_references(context)


@pytest.mark.parametrize('context,attempted', [
    # Nested mode with single property and 'flat' is an ignored keyword
    (
        {
            'keys': "black white",
            'value': "#000000 #ffffff",
            "flat": "whatever",
        },
        {
            'black': {
                'value': "#000000",
            },
            'white': {
                'value': "#ffffff",
            },
        },
    ),
    # Nested mode with multiple property
    (
        {
            'keys': "black white",
            'selectors': ".bg-black .bg-white",
            'values': "#000000 #ffffff",
        },
        {
            'black': {
                'selectors': ".bg-black",
                'values': "#000000",
            },
            'white': {
                'selectors': ".bg-white",
                'values': "#ffffff",
            },
        },
    ),
])
def test_serialize_to_nested_success(context, attempted):
    serializer = ManifestSerializer()

    serialized = serializer.serialize_to_nested('foo', context)

    assert serialized == attempted


@pytest.mark.parametrize('context', [
    # Missing 'keys'
    {
        'value': "#000000 #ffffff",
    },
    # Length differences with keys
    {
        'keys': "black white",
        'selectors': ".bg-black",
    },
])
def test_serialize_to_nested_error(context):
    serializer = ManifestSerializer()

    with pytest.raises(SerializerError):
        serializer.serialize_to_nested('foo', context)


@pytest.mark.parametrize('context,attempted', [
    (
        {
            'keys': "black white",
            'values': "#000000 #ffffff",
        },
        {
            'black': "#000000",
            'white': "#ffffff",
        },
    ),
    (
        {
            'keys': "black white red",
            'values': "#000000 #ffffff #ff0000",
        },
        {
            'black': "#000000",
            'white': "#ffffff",
            'red': "#ff0000",
        },
    ),
    # keys/values only in flat mode, everything else is ignored
    (
        {
            'keys': "black white",
            'values': "#000000 #ffffff",
            'dummy': 'whatever',
        },
        {
            'black': "#000000",
            'white': "#ffffff",
        },
    ),
])
def test_serialize_to_flat_success(context, attempted):
    serializer = ManifestSerializer()

    serialized = serializer.serialize_to_flat('foo', context)

    assert serialized == attempted


@pytest.mark.parametrize('context', [
    # Missing 'keys'
    {
        'values': "#000000 #ffffff",
    },
    # Missing 'values'
    {
        'keys': "black white",
    },
    # Length differences between keys and values
    {
        'keys': "black white red",
        'values': "#000000",
    },
])
def test_serialize_to_flat_error(context):
    serializer = ManifestSerializer()

    with pytest.raises(SerializerError):
        serializer.serialize_to_flat('foo', context)


@pytest.mark.parametrize('name,context,attempted', [
    # Nested mode with single value
    (
        'palette',
        {
            'styleguide-reference-palette': {
                'keys': "black white",
                'value': "#000000 #ffffff",
            },
        },
        {
            'black': {
                'value': "#000000",
            },
            'white': {
                'value': "#ffffff",
            },
        },
    ),
    # Flat mode
    (
        'palette',
        {
            'styleguide-reference-palette': {
                'flat': 'true',
                'keys': "black white",
                'values': "#000000 #ffffff",
            },
            'styleguide-reference-dummy': {
                'keys': "foo",
                'values': "bar",
            },
        },
        {
            'black': "#000000",
            'white': "#ffffff",
        },
    ),
])
def test_get_reference_success(name, context, attempted):
    serializer = ManifestSerializer()

    reference = serializer.get_reference(context, name)

    assert reference == attempted


@pytest.mark.parametrize('name,context', [
    # Missing reference with single rule
    (
        'palette',
        {
            'styleguide-reference-foo': {
                'keys': "black white",
                'value': "#000000 #ffffff",
            },
        },
    ),
    # Invalid property name
    (
        'palette',
        {
            'styleguide-reference-palette': {
                'keys': "black white",
                'font-color': "red",
                'value': "#000000 #ffffff",
            },
        },
    ),
    # Missing reference with multiple rules
    (
        'foo',
        {
            'styleguide-reference-palette': {
                'keys': "black white",
                'value': "#000000 #ffffff",
            },
            'styleguide-reference-bar': {
                'keys': "black white",
                'value': "#000000 #ffffff",
            },
        },
    ),
])
def test_get_reference_error(name, context):
    serializer = ManifestSerializer()

    with pytest.raises(SerializerError):
        serializer.get_reference(context, name)


@pytest.mark.parametrize('context,attempted', [
    # Default dict mode for a reference
    (
        {
            'styleguide-metas-references': {
                'names': "palette",
            },
            'dummy': {
                'content': "foo",
            },
            'styleguide-reference-palette': {
                'keys': "black white",
                'value': "#000000 #ffffff",
                'selector': ".bg-black .bg-white",
            },
        },
        {
            'palette': {
                'black': {
                    'value': "#000000",
                    'selector': ".bg-black",
                },
                'white': {
                    'value': "#ffffff",
                    'selector': ".bg-white",
                },
            },
        },
    ),
    # Flat mode for a reference
    (
        {
            'styleguide-metas-references': {
                'names': "palette schemes",
            },
            'styleguide-reference-palette': {
                'flat': 'true',
                'keys': "black white",
                'values': "#000000 #ffffff",
            },
            'styleguide-reference-schemes': {
                'keys': "black white gray25",
                'background': "#000000 #ffffff #404040",
                'font_color': "#ffffff #000000 #ffffff",
                'selector': ".black .white .gray25",
            },
        },
        {
            'palette': {
                'black': "#000000",
                'white': "#ffffff",
            },
            'schemes': {
                'black': {
                    'background': "#000000",
                    'selector': ".black",
                    'font_color': "#ffffff",
                },
                'gray25': {
                    'background': "#404040",
                    'selector': ".gray25",
                    'font_color': "#ffffff",
                },
                'white': {
                    'background': "#ffffff",
                    'selector': ".white",
                    'font_color': "#000000",
                },
            },
        },
    ),
])
def test_get_references(context, attempted):
    serializer = ManifestSerializer()

    enabled_references = serializer.get_meta_references(context)
    references = serializer.get_enabled_references(context, enabled_references)

    assert references == attempted


@pytest.mark.parametrize('context,attempted', [
    # Basic test to check serialize() glue method is ok
    (
        {
            'styleguide-metas-references': {
                'names': "palette",
            },
            'dummy': {
                'content': "foo",
            },
            'styleguide-reference-palette': {
                'flat': 'true',
                'keys': "black white",
                'values': "#000000 #ffffff",
            },
        },
        {
            'palette': {
                'black': "#000000",
                'white': "#ffffff",
            },
        },
    ),
])
def test_serialize(context, attempted):
    serializer = ManifestSerializer()

    references = serializer.serialize(context)

    assert references == attempted
