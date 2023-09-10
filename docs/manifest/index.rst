.. _Libsass: https://github.com/sass/libsass
.. _Dart Sass: https://github.com/sass/dart-sass


.. _manifest_intro:

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

This **required meta** defines what references rules to collect or to ignore.

It contains either a variable ``--names`` or a variable ``--auto`` to enable
references. If both of these variables are defined ``--names`` is used.

Reference names (both includes and excludes) is a list of names (without rule prefix
and prefix type) divided by a single whitespace.

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

    In this mode another variable is watched for, it is ``excludes`` which is a list
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


.. toctree::
   :maxdepth: 2

   serialization_structures.rst
   item_separator.rst
