
.. _serializer_item_separator:

==============
Item separator
==============

.. _serializer_item_separator_intro:

Introduction
************

Some serialization structures split values in list items to fit to their Python
structure:

* ``nested``
* ``flat``
* ``list``

These structure can set a variable ``--splitter`` to select the way to split value
items.

Once enable into a rule, the selected splitter is applied on every rule variables,
you can not use different separators in a same rule.


.. _serializer_item_separator_whitespace:

Split on white spaces
*********************

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


.. _serializer_item_separator_list:

Object list
***********

The white space separator may not fit to every cases particularly when you have value
items that contains spaces.

For such cases you have possibility to declare your item values as an object list such
as: ::

    '["foo", "bar", "ping pong"]'

Is turned to a Python list: ::

    ["foo", "bar", "ping pong"]

You can enable this mode by using variable ``--splitter`` with value ``"json-list"``: ::

    .styleguide-reference-dummy{
        --structure: "list";
        --splitter: "object-list";
        --items: '["foo", "bar", "ping pong"]';
    }

.. admonition:: Syntax
   :class: caution

   You may encounter decoding issues for invalid syntax.

   The most common issue is the single quote usage around string, this is invalid in
   JSON since every string is expected to be double quoted.
