.. _Libsass: https://github.com/sass/libsass
.. _Dart Sass: https://github.com/sass/dart-sass


.. _serializer_structures:

========================
Serialization structures
========================

.. _serializer_structures_intro:

Introduction
************

Available serialization structure are:

* String;
* List;
* Nested dictionnary (default);
* Flat dictionnary;
* Complex;

.. _serializer_structures_string:

String
******

A very basic structure to serialize a value as a simple string.

It is enabled when there is a variable ``--structure`` with value ``string``.

It requires a ``--value`` which value is returned.

So for example, a reference like this: ::

    .styleguide-reference-dummy {
        --structure: "string";
        --value: "my value";
    }

Will be serialized to this in JSON: ::

    {
        "dummy": "my value"
    }


.. _serializer_structures_list:

List
****

A structure that serialize to a list.

It is enabled when there is a variable ``--structure`` containing ``"list"``.

It requires a ``--items`` variable which value will be splitted on white space to a
list items.

So for example, a reference like this: ::

    .styleguide-reference-dummy {
        --structure: "list";
        --items: "foo bar";
    }

Will be serialized to this in JSON: ::

    {
        "dummy": [
            "foo",
            "bar"
        ]
    }


.. _serializer_structures_flat:

Flat
****

A serialization structure when you only have key/value pair to store.

It is enabled when there is a variable ``--structure`` containing ``"flat"``.

In this mode there is two other variables: ``--keys`` and ``--values``. And they are
both required.

Obviously ``--keys`` is for key names and ``--values`` for key values. All other
variables are ignored.

So for example, a reference like this: ::

    .styleguide-reference-dummy {
        --structure: "flat";
        --keys: "foo bar";
        --values: "#000000 #ffffff";
    }

Will be serialized to this in JSON: ::

    {
        "dummy": {
            "foo": "#000000",
            "bar": "#ffffff"
        }
    }


.. _serializer_structures_nested:

Nested
******

This is the default serialization structure. It requires a ``--keys`` variable to
define map keys to create where each other variable will be stored.

Variables values are stored in their respective map key according to their order
position, so order does matter when defining values in your variables. Also a variable
that contains much or less values than the ``--keys`` values will raise an error, it
must be the exact same length.

So for example, a reference like this: ::

    .styleguide-reference-dummy {
        --keys: "foo bar";
        --selector: ".myfoo .mybar";
        --value: "#000000 #ffffff";
    }

Will be serialized to this in JSON: ::

    {
        "dummy": {
            "foo": {
                "selector": ".myfoo",
                "value": "#000000"
            },
            "bar": {
                "selector": ".mybar",
                "value": "#ffffff"
            }
        }
    }


.. _serializer_structures_complex:

Complex
*******

When every other structures does not fit to your needs, complex structure may be the
way to go but be aware that this is not easy to build complex object from Sass.

It is enabled when there is a variable ``--structure`` containing ``"object-complex"``.

It requires a ``--object`` which contains a string of a valid JSON object.

Remember than array item names and string values must be double quoted, single quotes
usage for them is invalid in JSON.

So for example, a reference like this: ::

    .styleguide-reference-dummy {
        --structure: "object-complex";
        --value: '["my value", "foo"]';
    }

Will be serialized to this in JSON: ::

    {
        "dummy": [
            "my value",
            "foo"
        ]
    }
