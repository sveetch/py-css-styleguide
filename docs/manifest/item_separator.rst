
.. _serializer_item_separator:

==============
Item separator
==============

.. _serializer_item_separator_intro:

Introduction
************

The following serialization structures split values in list items to fit to a Python
structure:

* ``nested``
* ``flat``
* ``list``

These structure can set special properties:

* ``--splitter`` to select the way to split value items;
* ``--cleaner`` to select the way to manage whitespaces in values;

.. Warning::
    Once enabled into a reference rule the selected splitter and cleaner are applied on
    every rule values, you can not use different splitters or cleaners in a same rule.


.. _serializer_item_separator_splitter:

Splitter
********

.. _serializer_item_separator_whitespace:

White spaces
------------

Default behavior is to use a simple white space separator such as: ::

    "foo bar ping pong"

Is turned to a Python list: ::

    ["foo", "bar", "ping", "pong"]

Since it is default behavior, you don't need to declare anything to enable this mode,
but if you want to explicitely declare it you just have to add variable ``--splitter``
with value ``"white-space"``: ::

    .styleguide-reference-dummy {
        --structure: "list";
        --splitter: "white-space";
        --items: "foo bar";
    }

This is the easiest and more human readable way to define value items.

.. _serializer_item_separator_list:

Object list
-----------

The white space separator may not fit to every cases particularly when you have value
items that contains spaces.

For such cases you have possibility to declare your item values as an object list and
it will be turned to a true Python list. It stands on a simple trick, we put it in a
string since Sass does not support JSON syntax but encased in a string it is still
valid Sass.

You can enable this mode by using variable ``--splitter`` with value
``"object-list"``: ::

    --splitter: "object-list";

.. Note::
    This splitter was previously called ``json-list`` that is still working for now but
    deprecated, you will have warning about it until you change it to ``object-list``.

.. Hint::
    This allows to mix multiple value types like string, integer, float, boolean and
    null.

.. Caution::
   Since we parse content from either JSON or Python, it would allow to nest a list
   but this won't work with manifest serializer which only expect a list and any other
   type will raise error or lead to unexpected results.

This feature is subject to compiler behavior from :ref:`manifest_meta_compiler` so its
usage depends from enabled compiler support.

.. _serializer_item_separator_list_libsass:

Libsass behavior
................

This compiler allows to write basic JSON syntax since it does not enforce string
quotes. Your object list will have to be written in a correct JSON syntax.

In a reference source example: ::

    .styleguide-reference-dummy {
        --structure: "list";
        --splitter: "object-list";
        --items: '["foo", "bar", 42, null, true, "ping pong"]';
    }

.. admonition:: Syntax
   :class: caution

   You are required to surround your object list with simple quotes so your object
   list items can use double quotes for strings as required from JSON syntax. Don't
   mess with the quotes else you will have JSON syntax error or very unexpected
   content results.

Reference content will be parsed to a Python list: ::

    {
        "dummy": [
            "foo",
            "bar",
            42,
            None,
            True,
            "ping pong"
        ]
    }

.. Hint::
    Remember that in JSON  the boolean values are ``true`` or ``false`` and null value
    is ``null``.


.. _serializer_item_separator_list_dartsass:

Dart Sass behavior
..................

This compiler does not allow to write valid JSON due to enforcing double quotes on
Sass strings that prevent us to write JSON strings.

So instead of JSON, we are using Python syntax that is more versatile, it allows both
single or double quotes for a Python string.

In a reference source example: ::

    .styleguide-reference-dummy {
        --structure: "list";
        --splitter: "object-list";
        --items: "['foo', 'bar', 42, None, True, 'ping pong']";
    }

.. admonition:: Syntax
   :class: caution

   You are required to surround your object list with double quotes so your object
   list items can use single quotes for strings. Don't mess with the quotes else you
   will have Python syntax error or very unexpected content results.

Reference content will be parsed to a Python list: ::

    {
        "dummy": [
            "foo",
            "bar",
            42,
            None,
            True,
            "ping pong"
        ]
    }

.. Hint::
    Remember that in Python the boolean values are ``True`` or ``False`` and null value
    is ``None``.

Cleaner
*******

There is actually only a single effective cleaner named ``whitespaces`` but it has
different behavior depending the enabled splitter.

For White spaces splitter
-------------------------

Sometime your values may have many whitespaces, like this: ::

    .styleguide-reference-dummy {
        --structure: "list";
        --splitter: "white-space";
        --items: " foo   bar ";
    }

That would result to: ::

    {
        "dummy": [
            "",
            "foo",
            "",
            "bar",
            "",
        ]
    }

This is because *White spaces* splitter splits on a single whitespace, considering
every other whitespaces as meaningful.

You may however consider them as artefacts, you can easily remove them using cleaner: ::

    .styleguide-reference-dummy {
        --structure: "list";
        --splitter: "white-space";
        --cleaner: "whitespaces";
        --items: " foo   bar ";
    }

That would result to: ::

    {
        "dummy": [
            "foo",
            "bar",
        ]
    }

For Object list splitter
------------------------

Sometime your values may include leading or ending whitespaces, like this: ::

    .styleguide-reference-dummy {
        --structure: "list";
        --splitter: "object-list";
        --items: "[' foo', 'bar ', ' ping pong ']";
    }

That would result to: ::

    {
        "dummy": [
            " foo",
            "bar ",
            " ping pong "
        ]
    }

You may consider leading or ending whitespace as artefacts, you can easily remove them
using cleaner: ::

    .styleguide-reference-dummy {
        --structure: "list";
        --splitter: "object-list";
        --cleaner: "whitespaces";
        --items: "[' foo', 'bar ', ' ping pong ']";
    }

That would result to: ::

    {
        "dummy": [
            "foo",
            "bar",
            "ping pong"
        ]
    }

.. Note::
    * Only leading and ending whitespaces are removed, whitespace between word are
      keeped;
    * Whitespace between item (before or after the coma) are never meaningful, cleaner
      has no effect on them because they are initially ignored from parsed;
    * Cleaner is only effective on string type;
