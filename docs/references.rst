.. _Libsass: https://github.com/sass/libsass
.. _Dart Sass: https://github.com/sass/dart-sass


========
Manifest
========

A manifest is a valid CSS3 stylesheet composed of rules.

Even though it is a valid CSS3 stylesheet the purpose of a manifest is not to be
published on frontend, only to be parsed from manifest serializer.

Rule format
***********

A rule is a CSS classes using CSS variables to define rule values: ::

    .styleguide-TYPE-NAME {
        --foo: "foo bar";
    }


.. Note::
    Manifest serializer should be able to read CSS property (without the
    leading ``--``) as variable (with the leading ``--``) in a rule and it should
    serializes without problem but the manifest file won't be valid CSS file, you
    should allways use CSS variable instead of CSS property.

Rule names are normalized such as manifest serializer can parse them:

* A rule always starts with ``styleguide``, it is called the *rule base prefix*;
* Then the rule type that is either ``metas`` or ``reference``;
* Then the rule name that can be whatever you want;
* Finally all of these parts are joined with character ``-``;

.. Warning::
    A rule name must be valid in a CSS selector and not contains character ``-``
    (because it need to be a valid variable name for Python). To divide words inside a
    name, use ``_`` instead.

Every class selectors that does not start with the rule base prefix are ignored.


Meta rule
*********

Meta rules is on charge to define some global parameters for manifest serializer.

There is actually only one meta rule named **styleguide-metas-references** that is
required.


styleguide-metas-compiler
-------------------------

Historically, PyCssStyleguide has been developed with `Libsass`_ which has been superseded
with `Dart Sass`_. The latter has changed some syntax behaviors and especially the string
quoting.

The default compiler support is for `Libsass`_ that is able to compile both behaviors,
but `Dart Sass`_ is not flexible as well so it is required to inform serializer about
compiler behaviors to adopt.

This meta reference is not required, but recommended. If not present the default
compiler support is enabled and the manifest serializer will emit a warning  message.

To enable `Libsass`_ behaviors: ::

    .styleguide-metas-compiler {
        --support: "libsass";
    }

To enable `Dart Sass`_ behaviors: ::

    .styleguide-metas-compiler {
        --support: "dartsass";
    }


styleguide-metas-references
---------------------------

This meta defines what references rules to collect or to ignore.

It contains either a variable ``--names`` or a variable ``--auto`` to enable
references. If both of these variables are defined ``--names`` is used.

Enable manually
    Using ``--names`` you will explicitely define a list of reference names to enable,
    every other non enabled rules will be ignored ::

        .styleguide-metas-references {
            --names: "foo bar";
        }

    This will enable only references ``styleguide-reference-foo`` and
    ``styleguide-reference-bar``.

    .. Warning::
        If an enabled reference name does not exist as a CSS rule from manifest this
        will raises an error.

Enable automatically
    Using ``--auto`` variable every reference rules will be enabled.
    The value of this variable is not important as long as it is not empty.

    ::

        .styleguide-metas-references {
            --auto: "true";
        }

    Which will enable every CSS rule starting with ``styleguide-reference-``.

    In this mode, another variable is watched for, it is ``excludes`` which is a list
    of reference names to ignore: ::

        .styleguide-metas-references {
            --auto: "true";
            --excludes: "reference2 reference3";
        }

    This would ignore ``reference2`` and ``reference3`` but will allow every other
    references.


Reference rule
**************

Reference rule is on charge to declare your CSS component variables or whatever you
want to expose in your styleguide.


Serialization structures
------------------------

Available serialization structure are:

* Nested dictionnary (default);
* JSON;
* Flat dictionnary;
* List;
* String;

Nested
......

This is the default serialization structure. It requires a ``--keys`` variable to define map keys to create where each other variable will be stored.

Variables values are stored in their respective map key according to their order position, so order does matter when defining values in your variables. Also a variable that contains much or less values than the ``--keys`` values will raise an error, it must be the exact same length.

So for example, a reference like this: ::

    .styleguide-reference-dummy {
        --keys: "foo bar";
        --selector: ".foo .bar";
        --value: "#000000 #ffffff";
    }

Will be serialized to this in JSON: ::

    {
        'foo': {
            'selector': '.foo',
            'value': '#000000'
        },
        'bar': {
            'selector': '.bar',
            'value': '#ffffff'
        }
    }

Flat
....

A serialization structure when you only have key/value pair to store.

It is enabled when there is a variable ``--structure`` containing ``"flat"``.

In this mode there is two other variables: ``--keys`` and ``--values``. And they are both required.

Obviously ``--keys`` is for key names and ``--values`` for key values. All other variables are ignored.

So for example, a reference like this: ::

    .styleguide-reference-dummy {
        --structure: "flat";
        --keys: "foo bar";
        --values: "#000000 #ffffff";
    }

Will be serialized to this in JSON: ::

    {
        'foo': '#000000',
        'bar': '#ffffff'
    }

List
....

A structure that serialize to a list.

It is enabled when there is a variable ``--structure`` containing ``"list"``.

It requires a ``--items`` variable which value will be splitted on white space to a list items.

So for example, a reference like this: ::

    .styleguide-reference-dummy {
        --structure: "list";
        --items: "foo bar";
    }

Will be serialized to this in JSON: ::

    [
        'foo',
        'bar'
    ]

String
......

A very basic structure to serialize a value as a simple string.

It is enabled when there is a variable ``--structure`` containing ``"string"``.

It requires a ``--value`` which value is returned.

So for example, a reference like this: ::

    .styleguide-reference-dummy {
        --structure: "string";
        --value: "my value";
    }

Will be serialized to this in JSON: ::

    'my value'

JSON
....

When every other structures does not fit to your needs, JSON structure is the way to go but be aware that this is not easy to build complex JSON object from Sass.

It is enabled when there is a variable ``--structure`` containing ``"json"``.

It requires a ``--object`` which contains a string of a valid JSON object.

Remember than array item names and string values must be double quoted, single quotes usage for them is invalid in JSON.

This serializer use a hook to preserve dict item orders but this is only guaranteed since Python 3.6.

So for example, a reference like this: ::

    .styleguide-reference-dummy {
        --structure: "json";
        --value: '["my value", "foo"]';
    }

Will be serialized to this in JSON: ::

    [
        'my value',
        'foo'
    ]


Values items separator
----------------------

Some serialization structures split their values in a list items to fit them to their
Python structure, they are:

* ``nested``;
* ``flat``;
* ``list``;

Split on white spaces
.....................

Default behavior is to use a simple white space separator such as: ::

    "foo bar ping pong"

Is turned to a Python list: ::

    ["foo", "bar", "ping", "pong"]

Since it is default behavior, you don't need to declare anything to enable this mode,
but if you want to explicitely declare it you just have to add variable ``--splitter``
with value ``"white-space"``: ::

    .styleguide-reference-dummy{
        --structure: "list";
        --splitter: "white-space";
        --items: "foo bar";
    }

This is the easiest and more human readable way to define value items.


JSON list
.........

The white space separator may not fit to every cases particularly when you have value
items that contains spaces.

For such cases you have possibility to declare your item values as JSON list such as: ::

    '["foo", "bar", "ping pong"]'

Is turned to a Python list: ::

    ["foo", "bar", "ping pong"]

You can enable this mode by using variable ``--splitter`` with value ``"json-list"``: ::

    .styleguide-reference-dummy{
        --structure: "list";
        --splitter: "json-list";
        --items: '["foo", "bar", "ping pong"]';
    }

Be aware that you may encounter JSON decoder issues for invalid JSON syntax. The most
common issue is the single quote usage around string, this invalid in JSON, every
string is allways double quoted.
