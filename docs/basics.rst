
======
Basics
======

A manifest is composed of **meta rules** and **reference rules**.

Meta rules
**********

Meta rules is on charge to define some global parameters for references and their content.

There is actually only one meta rule named **styleguide-metas-references** that is required.

It's worth to notice than parser should be able to read CSS property (without the leading ``--``) as variable (with the leading ``--``) in references and this should serialize without problems but the manifest file won't be valid CSS file, you should remember to allways use variable instead of property.

styleguide-metas-references
---------------------------

Contains either a variable ``--names`` or a variable ``-auto`` to enable
references. If both of these variables are defined ``--names`` is used.

Manually
    Using ``--names`` which define a list of names to enable, every
    other non enabled rule will be ignored.

    Reference name must not contains special character nor ``-`` so they still
    be valid variable name for almost any languages. For word separator inside
    name, use ``_``.

    ::

        --names: "reference1 reference2";

    Which will enable ``styleguide-reference-foo`` and
    ``styleguide-reference-bar`` references. If enabled reference name does
    not exist as a CSS rule, it will raises an error.
Automatic
    Using ``--auto`` variable every reference rules will be enabled.
    The value of this variable is not important as long as it is not empty.

    ::

        --auto: "true";

    Which will enable every CSS rule starting with ``styleguide-reference-``.

    In this mode, another variable is watched for, it is ``excludes`` which is a list
    of reference names to ignore: ::

        --auto: "true";
        --excludes: "reference2 reference3";

    This would ignore ``reference2`` and ``reference3`` but will allow every other
    references.

Reference rules
***************

Reference rule is on charge to declare your CSS component settings or whatever you want to expose in your styleguide. A reference contains properties to declare values and some options.

Every reference rule starts with ``styleguide-reference-`` followed by its name as defined in enabled reference names.

Available serialization structure are:

* Nested dictionnary (default);
* JSON;
* Flat dictionnary;
* List;
* String;

Serialization structures
************************

Nested
------

This is the default serialization structure. It requires a ``--keys`` variable to define map keys to create where each other variable will be stored.

Variables values are stored in their respective map key according to their order position, so order does matter when defining values in your variables. Also a variable that contains much or less values than the ``--keys`` values will raise an error, it must be the exact same length.

So for example, a reference like this: ::

    .styleguide-reference-dummy{
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
----

A serialization structure when you only have key/value pair to store.

It is enabled when there is a variable ``--structure`` containing ``"flat"``.

In this mode there is two other variables: ``--keys`` and ``--values``. And they are both required.

Obviously ``--keys`` is for key names and ``--values`` for key values. All other variables are ignored.

So for example, a reference like this: ::

    .styleguide-reference-dummy{
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
----

A structure that serialize to a list.

It is enabled when there is a variable ``--structure`` containing ``"list"``.

It requires a ``--items`` variable which value will be splitted on white space to a list items.

So for example, a reference like this: ::

    .styleguide-reference-dummy{
        --structure: "list";
        --items: "foo bar";
    }

Will be serialized to this in JSON: ::

    [
        'foo',
        'bar'
    ]

String
------

A very basic structure to serialize a value as a simple string.

It is enabled when there is a variable ``--structure`` containing ``"string"``.

It requires a ``--value`` which value is returned.

So for example, a reference like this: ::

    .styleguide-reference-dummy{
        --structure: "string";
        --value: "my value";
    }

Will be serialized to this in JSON: ::

    'my value'

JSON
----

When every other structures does not fit to your needs, JSON structure is the way to go but be aware that this is not easy to build complex JSON object from Sass.

It is enabled when there is a variable ``--structure`` containing ``"json"``.

It requires a ``--object`` which contains a string of a valid JSON object.

Remember than array item names and string values must be double quoted, single quotes usage for them is invalid in JSON.

This serializer use a hook to preserve dict item orders but this is only guaranteed since Python 3.6.

So for example, a reference like this: ::

    .styleguide-reference-dummy{
        --structure: "json";
        --value: '["my value", "foo"]';
    }

Will be serialized to this in JSON: ::

    [
        'my value',
        'foo'
    ]


Values items separator
**********************

Some serialization structures split their values in a list items to fit them to their Python structure, they are:

* ``nested``;
* ``flat``;
* ``list``;

Split on white spaces
---------------------

Default behavior is to use a simple white space separator such as: ::

    "foo bar ping pong"

Is turned to a Python list: ::

    ["foo", "bar", "ping", "pong"]

Since it is default behavior, you don't need to declare anything to enable this mode, but if you want to explicitely declare it you just have to add variable ``--splitter`` with value ``"white-space"``: ::

    .styleguide-reference-dummy{
        --structure: "list";
        --splitter: "white-space";
        --items: "foo bar";
    }

This is the easiest and more human readable way to define value items.


JSON list
---------

The white space separator may not fit to every cases particularly when you have value items that contains spaces.

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

Be aware that you may encounter JSON decoder issues for invalid JSON syntax. The most common issue is the single quote usage around string, this invalid in JSON, every string is allways double quoted.
