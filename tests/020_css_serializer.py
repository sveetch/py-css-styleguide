# -*- coding: utf-8 -*-
"""
Some test define manifest datas with an OrderedDict when they assert some
value against a list. A simple dict can be used when there is no assertion
about ordered sequences.
"""
from collections import OrderedDict

import pytest

from py_css_styleguide.exceptions import SerializerError, StyleguideValidationError
from py_css_styleguide.serializer import ManifestSerializer


@pytest.mark.parametrize('value,mode,expected', [
    # White space separator
    (
        "",
        "white-space",
        [],
    ),
    (
        "foo",
        "white-space",
        ["foo"],
    ),
    (
        "foo bar",
        "white-space",
        ["foo", "bar"],
    ),
    (
        "foo bar téléphone maison",
        "white-space",
        ["foo", "bar", "téléphone", "maison"],
    ),
    (
        "foo bar téléphone-maison",
        "white-space",
        ["foo", "bar", "téléphone-maison"],
    ),
    # JSON list parsing
    (
        "[]",
        "json-list",
        [],
    ),
    (
        '["foo"]',
        "json-list",
        ["foo"],
    ),
    (
        '["foo\'", "bar"]',
        "json-list",
        ["foo'", "bar"],
    ),
    (
        '["foo", "ping pong", "bar", "téléphone"]',
        "json-list",
        ["foo", "ping pong", "bar", "téléphone"],
    ),
])
def test_value_splitter_success(value, mode, expected):
    serializer = ManifestSerializer()

    data = serializer.value_splitter('ref', 'prop', value, mode)

    assert data == expected


@pytest.mark.parametrize('value,mode', [
    # Invalid JSON syntax
    (
        "[",
        "json-list",
    ),
    (
        "['nope']",
        "json-list",
    ),
])
def test_value_splitter_error(value, mode):
    serializer = ManifestSerializer()

    with pytest.raises(SerializerError):
        serializer.value_splitter('ref', 'prop', value, mode)


@pytest.mark.parametrize('context,expected', [
    (
        {
            'styleguide-metas-references': {
                'names': "palette",
            },
            'styleguide-reference-foo': {
                'content': "bar",
            },
        },
        ["foo"],
    ),
    # Enforce the right item order to match returned list order
    (
        OrderedDict((
            ('styleguide-reference-foo', {
                'content': "bar",
            }),
            ('styleguide-reference-pika', {
                'content': "chu",
            }),
            ('dummy', {
                'names': "yip",
            }),
            ('styleguide-reference-ping', {
                'content': "pong",
            }),
        )),
        ["foo", "pika", "ping"],
    ),
])
def test_get_available_references(context, expected):
    serializer = ManifestSerializer()

    reference_names = serializer.get_available_references(context)

    assert reference_names == expected


@pytest.mark.parametrize('context,expected', [
    # With a dummy ignored rule just for fun
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
    # Every enabled rules are returned
    (
        {
            'styleguide-metas-references': {
                'names': "palette schemes foo bar",
            }
        },
        ["palette", "schemes", "foo", "bar"],
    ),
    # Automatically enable every references but no reference defined
    (
        {
            'styleguide-metas-references': {
                'auto': "true",
            }
        },
        [],
    ),
    # Automatically enable every references and explicitely ignore some ones
    (
        OrderedDict((
            ('styleguide-metas-references', {
                'auto': "true",
                'excludes': "bar pong",
            }),
            ('styleguide-reference-foo', {
                'content': "dummy",
            }),
            ('styleguide-reference-bar', {
                'content': "dummy",
            }),
            ('styleguide-reference-ping', {
                'content': "dummy",
            }),
            ('styleguide-reference-pong', {
                'content': "dummy",
            }),
        )),
        ['foo', 'ping'],
    ),
])
def test_get_meta_references_success(context, expected):
    serializer = ManifestSerializer()

    reference_names = serializer.get_meta_references(context)

    assert reference_names == expected


@pytest.mark.parametrize('context, expected', [
    # Missing references meta
    (
        {
            'styleguide-metas-foo': {
                'names': "palette",
            }
        },
        SerializerError,
    ),
    # Missing names or auto property
    (
        {
            'styleguide-metas-references': {
                'content': "palette",
            }
        },
        SerializerError,
    ),
    # Invalid name (from '-' character)
    (
        {
            'styleguide-metas-references': {
                'names': "foo-bar",
            }
        },
        StyleguideValidationError,
    ),
    # Empty list
    (
        {
            'styleguide-metas-references': {
                'names': "",
            }
        },
        SerializerError,
    ),
])
def test_get_meta_references_error(context, expected):
    serializer = ManifestSerializer()

    with pytest.raises(expected):
        serializer.get_meta_references(context)


@pytest.mark.parametrize('context,expected', [
    # Empty list
    (
        {
            'object': '[]',
        },
        [],
    ),
    # Empty dict
    (
        {
            'object': '{}',
        },
        {},
    ),
    # Simple list and encoding
    (
        {
            'object': '["foo", "téléphone"]',
        },
        ['foo', 'téléphone'],
    ),
    # Simple dict
    (
        {
            'object': '{"foo": "ping", "bar": "pong"}',
        },
        {
            "foo": "ping",
            "bar": "pong"
        },
    ),
    # Nested dict
    (
        {
            'object': '{"foo": "bar", "plop": {"ping": "pang", "pong": "pung"}}',
        },
        {
            "foo": "bar",
            "plop": {
                "ping": "pang",
                "pong": "pung"
            }
        },
    ),
    # Various type in a dict
    (
        {
            'object': ("""{"foo": "bar", "life": 42, "moo": true,"""
                       """"plop": ["ping", "pong"]}"""),
        },
        {
            "foo": "bar",
            "life": 42,
            "moo": True,
            "plop": [
                "ping",
                "pong"
            ]
        },
    ),
])
def test_serialize_to_json_success(context, expected):
    serializer = ManifestSerializer()

    serialized = serializer.serialize_to_json('foo', context)

    assert serialized == expected


@pytest.mark.parametrize('context', [
    # Missing 'object'
    {
        'value': "#000000 #ffffff",
    },
    # Empty object
    {
        'object': '',
    },
    # Single quote encoding issue
    {
        'object': "['foo']",
    },
    # Syntax error
    {
        'object': '["foo"',
    },
])
def test_serialize_to_json_error(context):
    serializer = ManifestSerializer()

    with pytest.raises(SerializerError):
        serializer.serialize_to_json('foo', context)


@pytest.mark.parametrize('context,expected', [
    # Nested mode with single property and ensure 'structure' is an ignored
    # keyword
    (
        {
            'keys': "black white",
            'value': "#000000 #ffffff",
            "structure": "whatever",
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
    # With JSON list splitter
    (
        {
            'keys': '["black", "white"]',
            'value': '["#000000", "#ffffff"]',
            "structure": "whatever",
            "splitter": "json-list",
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
])
def test_serialize_to_nested_success(context, expected):
    serializer = ManifestSerializer()

    serialized = serializer.serialize_to_nested('foo', context)

    assert serialized == expected


@pytest.mark.parametrize('context', [
    # Missing 'keys'
    {
        'value': "#000000 #ffffff",
    },
    # Length difference with keys
    {
        'keys': "black white",
        'selectors': ".bg-black",
    },
])
def test_serialize_to_nested_error(context):
    serializer = ManifestSerializer()

    with pytest.raises(SerializerError):
        serializer.serialize_to_nested('foo', context)


@pytest.mark.parametrize('context,expected,order', [
    (
        OrderedDict((
            ('keys', "black white"),
            ('values', "#000000 #ffffff"),
        )),
        OrderedDict((
            ('black', "#000000"),
            ('white', "#ffffff"),
        )),
        ['black', 'white'],
    ),
    (
        OrderedDict((
            ('keys', "black white red"),
            ('values', "#000000 #ffffff #ff0000"),
        )),
        OrderedDict((
            ('black', "#000000"),
            ('white', "#ffffff"),
            ('red', "#ff0000"),
        )),
        ['black', 'white', 'red'],
    ),
    (
        OrderedDict((
            ('keys', "cyan black white red"),
            ('values', "#48999b #000000 #ffffff #ff0000"),
        )),
        OrderedDict((
            ('cyan', "#48999b"),
            ('black', "#000000"),
            ('white', "#ffffff"),
            ('red', "#ff0000"),
        )),
        ['cyan', 'black', 'white', 'red'],
    ),
    # keys/values only in flat mode, everything else is ignored
    (
        OrderedDict((
            ('keys', "black white"),
            ('values', "#000000 #ffffff"),
            ('dummy', 'whatever'),
        )),
        OrderedDict((
            ('black', "#000000"),
            ('white', "#ffffff"),
        )),
        ['black', 'white'],
    ),
    # With JSON list splitter
    (
        OrderedDict((
            ('splitter', 'json-list'),
            ('keys', '["black", "white"]'),
            ('values', '["#000000", "#ffffff"]'),
        )),
        OrderedDict((
            ('black', "#000000"),
            ('white', "#ffffff"),
        )),
        ['black', 'white'],
    ),
])
def test_serialize_to_flat_success(context, expected, order):
    serializer = ManifestSerializer()

    serialized = serializer.serialize_to_flat('foo', context)

    assert serialized == expected
    assert order == list(serialized.keys())


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


@pytest.mark.parametrize('context,expected', [
    # Single item list
    (
        {
            'items': "black",
        },
        ['black'],
    ),
    # Empty list is ok
    (
        {
            'items': "",
        },
        [],
    ),
    # Multiple list items
    (
        {
            'items': "black white",
        },
        ['black', 'white'],
    ),
    # Many items
    (
        {
            'items': "1 2 3 4 5 6 7 8 9 0",
        },
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
    ),
    # With JSON list splitter
    (
        {
            'splitter': "json-list",
            'items': '["black", "white"]',
        },
        ['black', 'white'],
    ),
])
def test_serialize_to_list_success(context, expected):
    serializer = ManifestSerializer()

    serialized = serializer.serialize_to_list('foo', context)

    assert serialized == expected


@pytest.mark.parametrize('context', [
    # Missing 'items'
    {
        'values': "#000000 #ffffff",
    },
    # None value although it can occurs from parsed data because it happen
    # only if 'items' is not defined
    {
        'items': None,
    },
])
def test_serialize_to_list_error(context):
    serializer = ManifestSerializer()

    with pytest.raises(SerializerError):
        serializer.serialize_to_list('foo', context)


@pytest.mark.parametrize('context,expected', [
    # Basic string
    (
        {
            'value': "ok",
        },
        "ok",
    ),
    # Empty string is ok
    (
        {
            'value': "",
        },
        "",
    ),
    # Looks like a space separated list but it's a string
    (
        {
            'value': "black white",
        },
        "black white",
    ),
    # Some unicode
    (
        {
            'value': "¿ pœp ?",
        },
        "¿ pœp ?",
    ),
])
def test_serialize_to_string_success(context, expected):
    serializer = ManifestSerializer()

    serialized = serializer.serialize_to_string('foo', context)

    assert serialized == expected


@pytest.mark.parametrize('context', [
    # Missing 'value'
    {
        'content': "nope",
    },
    # None value for when variable is not defined
    {
        'value': None,
    },
])
def test_serialize_to_string_error(context):
    serializer = ManifestSerializer()

    with pytest.raises(SerializerError):
        serializer.serialize_to_string('foo', context)


@pytest.mark.parametrize('name,context,expected', [
    # JSON object with a list
    (
        'palette',
        {
            'styleguide-reference-palette': {
                'structure': 'json',
                'object': '["foo", "bar"]',
            },
        },
        [
            'foo',
            'bar'
        ],
    ),
    # Nested structure with single property
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
    # Nested structure with multiple properties
    (
        'palette',
        {
            'styleguide-reference-palette': {
                'keys': "black white",
                'value': "#000000 #ffffff",
                'foo': "one two",
            },
        },
        {
            'black': {
                'value': "#000000",
                'foo': "one",
            },
            'white': {
                'value': "#ffffff",
                'foo': "two",
            },
        },
    ),
    # Flat structure
    (
        'palette',
        {
            'styleguide-reference-palette': {
                'structure': 'flat',
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
    # List structure
    (
        'palette',
        {
            'styleguide-reference-palette': {
                'structure': 'list',
                'items': "black white",
            },
            'styleguide-reference-dummy': {
                'keys': "foo",
                'values': "bar",
            },
        },
        [
            'black',
            'white',
        ],
    ),
    # String structure
    (
        'palette',
        {
            'styleguide-reference-palette': {
                'structure': 'string',
                'value': "ok",
            },
            'styleguide-reference-dummy': {
                'keys': "foo",
                'values': "bar",
            },
        },
        "ok",
    ),
])
def test_get_reference_success(name, context, expected):
    serializer = ManifestSerializer()

    reference = serializer.get_reference(context, name)

    assert reference == expected


@pytest.mark.parametrize('name,context,expected', [
    # Missing reference with single rule
    (
        'palette',
        {
            'styleguide-reference-foo': {
                'keys': "black white",
                'value': "#000000 #ffffff",
            },
        },
        SerializerError,
    ),
    # Invalid property name
    (
        'palette',
        {
            'styleguide-reference-palette': {
                'keys': "black white",
                'font-color': "red blue",
                'value': "#000000 #ffffff",
            },
        },
        StyleguideValidationError,
    ),
    # Invalid structure mode name
    (
        'palette',
        {
            'styleguide-reference-palette': {
                'structure': "whatever",
                'keys': "black white",
                'values': "#000000 #ffffff",
            },
        },
        SerializerError,
    ),
    # Missing required reference from enabled references
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
        SerializerError,
    ),
])
def test_get_reference_error(name, context, expected):
    serializer = ManifestSerializer()

    with pytest.raises(expected):
        serializer.get_reference(context, name)


@pytest.mark.parametrize('context,expected,order', [
    # Default nested structure for a reference
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
        ['palette'],
    ),
    # Reference order comes from explicitely enabled reference names order
    (
        OrderedDict((
            ('styleguide-metas-references', {
                'names': "foo pika ping",
            }),
            ('styleguide-reference-ping', {
                'structure': "string",
                'value': "pong",
            }),
            ('styleguide-reference-pika', {
                'structure': "string",
                'value': "chu",
            }),
            ('styleguide-reference-foo', {
                'structure': "string",
                'value': "bar",
            }),
        )),
        {
            'foo': "bar",
            'pika': "chu",
            'ping': "pong",
        },
        ['foo', 'pika', 'ping'],
    ),
    # Every structure modes and splitter with automatic enabling
    (
        OrderedDict((
            ('styleguide-metas-references', {
                'auto': "true",
            }),
            ('styleguide-reference-palette', {
                'structure': 'flat',
                'keys': "black white",
                'values': "#000000 #ffffff",
            }),
            ('styleguide-reference-schemes', {
                'keys': "black white gray25",
                'background': "#000000 #ffffff #404040",
                'font_color': "#ffffff #000000 #ffffff",
                'selector': ".black .white .gray25",
            }),
            ('styleguide-reference-spaces', {
                'structure': 'list',
                'items': "short normal large",
            }),
            ('styleguide-reference-version', {
                'structure': 'string',
                'value': "V42.0",
            }),
            ('styleguide-reference-jsonstruct', {
                'structure': 'json',
                'object': '{"foo": "bar", "ping": "pong"}',
            }),
            ('styleguide-reference-flatjson', {
                'structure': 'flat',
                'splitter': 'json-list',
                'keys': '["black", "white"]',
                'values': '["#000000", "#ffffff"]',
            }),
        )),
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
            'spaces': [
                'short',
                'normal',
                'large',
            ],
            'version': "V42.0",
            'jsonstruct': {
                'foo': "bar",
                'ping': "pong",
            },
            'flatjson': {
                'black': "#000000",
                'white': "#ffffff",
            },
        },
        ["palette", "schemes", "spaces", "version", "jsonstruct", "flatjson"],
    ),
])
def test_get_enabled_references(context, expected, order):
    serializer = ManifestSerializer()

    enabled_references = serializer.get_meta_references(context)
    references = serializer.get_enabled_references(context, enabled_references)

    assert expected == references
    assert order == list(references.keys())


@pytest.mark.parametrize('context,expected', [
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
                'structure': 'flat',
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
def test_serialize(context, expected):
    serializer = ManifestSerializer()

    references = serializer.serialize(context)

    assert references == expected
