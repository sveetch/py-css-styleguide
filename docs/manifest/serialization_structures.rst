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
* Number (either integer or float);
* List;
* Nested dictionnary;
* Flat dictionnary;
* Complex;

.. _serializer_structures_string:

String
******

A very basic structure to serialize a value as a simple string.

Enabled by
    ``--structure: "string";``

Required variables
    ``--value`` that will contain a string.

Reference source sample
    ::

        .styleguide-reference-dummy {
            --structure: "string";
            --value: "my value";
        }

Reference serialization
    ::

        {
            "dummy": "my value"
        }


.. _serializer_structures_number:

Number
******

A structure to serialize a value as a number, meaning in Python it would be
either integer or float.

Enabled by
    ``--structure: "number";``

Required variables
    ``--value`` that will contain a number like ``42`` or ``42.123``. In fact you can
    also define it in a string like ``"42.123"``.

Reference source sample
    ::

        .styleguide-reference-dummy {
            --structure: "number";
            --value: 42;
        }
        .styleguide-reference-dumber {
            --structure: "number";
            --value: "43";
        }

Reference serialization
    ::

        {
            "dummy": 42,
            "dumber": 43
        }


.. _serializer_structures_list:

List
****

A structure that serialize to a list.

Enabled by
    ``--structure: "list";``

Required variables
    ``--items`` which value will be splitted using
    :ref:`serializer_item_separator`.

Reference source sample
    ::

        .styleguide-reference-dummy {
            --structure: "list";
            --items: "foo bar";
        }

Reference serialization
    ::

        {
            "dummy": [
                "foo",
                "bar"
            ]
        }


.. _serializer_structures_flat:

Flat
****

A serialization structure when you only have key/value pair to store. Key and value
pairs are associated following order.

Enabled by
    ``--structure: "flat";``

Required variables
    * ``--keys`` is for key name list splitted using :ref:`serializer_item_separator`;
    * ``--values`` is for key value list splitted using
      :ref:`serializer_item_separator`.

Reference source sample
    ::

        .styleguide-reference-dummy {
            --structure: "flat";
            --keys: "foo bar";
            --values: "#000000 #ffffff";
        }

Reference serialization
    ::

        {
            "dummy": {
                "foo": "#000000",
                "bar": "#ffffff"
            }
        }


.. _serializer_structures_nested:

Nested
******

A structure that will serialize to a dictionnary.

Enabled by
    ``--structure: "nested";``

Required variables
    * ``--keys`` to define map keys to create where each other variable will be stored.
      It is splitted using :ref:`serializer_item_separator`;

Optional variables
    Any other variable values are stored in their respective map key according to their
    order position. A variable that contains much or less values than the ``--keys``
    values will raise an error, it must be the exact same length.

Reference source sample
    ::

        .styleguide-reference-dummy {
            --structure: "nested";
            --keys: "foo bar";
            --selector: ".myfoo .mybar";
            --value: "#000000 #ffffff";
        }
        .styleguide-reference-alternative {
            --structure: "nested";
            --keys: "foo bar ping";
            --selector: ".myfoo .mybar .myping";
            --value: "#000000 #ffffff #ff0000";
            --content: "black white red";
            --size: "1rem 2rem 3rem";
        }

Reference serialization
    ::

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
            },
            "alternative": {
                "foo": {
                    "selector": ".myfoo",
                    "value": "#000000",
                    "content": "black",
                    "size": "1rem"
                },
                "bar": {
                    "selector": ".mybar",
                    "value": "#ffffff",
                    "content": "white",
                    "size": "2rem"
                },
                "ping": {
                    "selector": ".myping",
                    "value": "#ff0000",
                    "content": "red",
                    "size": "3rem"
                }
            }
        }


.. _serializer_structures_complex:

Complex
*******

When every other structures does not fit to your needs, complex structure may be the
way to go but be aware that this is not easy to build complex object from Sass.

Enabled by
    ``--structure: "object-complex";``

Required variables
    ``--object`` which contains a string of a valid JSON or Python object depending on
    :ref:`manifest_meta_compiler`.

Reference source sample
    ::

        .styleguide-reference-dummy {
            --structure: "object-complex";
            --value: '["my value", "foo"]';
        }

Reference serialization
    ::

        {
            "dummy": [
                "my value",
                "foo"
            ]
        }
