.. _sassmixins_intro:

==================
Sass mixin library
==================

PyCssStyleguide package is shipped with some Mixin libraries to help writing a CSS
manifest from Sass sources.

A Mixin library provide some Sass functions to ease converting some variables to values
for the manifest rules structures.

We currently support two Sass compilers:

* Libsass is the legacy compiler that was used from tools like ``node-sass`` or
  ``Boussole``. This compiler is now deprecated and many modern CSS framework don't
  support them anymore;
* Dartsass is the successor of Libsass that implements every new Sass features;

.. Note::
    Previously we managed an unique mixin library for both compilers but now Dartsass
    has implemented some new feature and behavior changes that made it too difficult
    to manage compatilibity.

    So there is now a distinct mixin library for each compiler. If you were using
    PyCssStyleguide before version 1.2.0, with these new mixin libraries you don't
    need anymore to define variable ``$pycssstyleguide-compiler-support`` since it is
    already included.

You may find the mixin library files from the Python package: ::

    from py_css_styleguide import COMPILER_DARTSASS_HELPER
    from py_css_styleguide import COMPILER_LIBSASS_HELPER

These variables are ``pathlib.Path`` objects that point to the absolute file path.
Choose the one according to your Sass compiler.

Or copy one of the following code in your Sass sources and name it
``_styleguide_helpers.scss``.

.. _libsass_mixins_source:

For Libsass compiler
********************

.. literalinclude:: ../py_css_styleguide/scss/libsass/_styleguide_helpers.scss

.. _dartsass_mixins_source:

For Dartsass compiler
*********************

.. literalinclude:: ../py_css_styleguide/scss/dartsass/_styleguide_helpers.scss
