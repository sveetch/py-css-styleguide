
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

Contains a variable ``--names`` to list enabled reference names.

A reference name must be made of letters, numbers and ``_`` character. No unicode or other special character.

Reference rules
***************

Reference rule is on charge to declare your CSS component settings or whatever you want to expose in your styleguide. A reference contains properties to declare values and some options.

Every reference rule starts with ``styleguide-reference-`` followed by its name as defined in enabled reference names.

Default serialization results in a nested structure but it can possibly be a flat structure, see serialization structure below.

Data serialization
******************

Values
------

Default serialization for a variable value is a list. They are defined like this: ::

    "foo bar ping pong"

As you can see each item is separated by a white space.

If you only have an unique item this will be a simple string: ::

    "foo"

Structure
---------

Nested
......

This is the default structure serialization. It requires a ``--keys`` variable to define map keys to create where each other variable will be stored.

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
....

An optional structure mode when you only have key/value pair to store, this is enabled when there is ``--flat`` variable containing string ``"true"``. In this mode there is two other variables: ``--keys`` and ``--values``. And they are both required.

Obviously ``--keys`` is for key names and ``--values`` for key values. All other variables are ignored.

So for example, a reference like this: ::

    .styleguide-reference-dummy{
        --flat: "true";
        --keys: "foo bar";
        --values: "#000000 #ffffff";
    }

Will be serialized to this in JSON: ::

    {
        'foo': '#000000',
        'bar': '#ffffff'
    }

