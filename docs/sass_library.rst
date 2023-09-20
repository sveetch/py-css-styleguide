.. _sassmixins_intro:

==================
Sass mixin library
==================

This is the included Sass mixin library you should use to build CSS manifest from Sass.
Copy the following source into your Sass project and import it, we recommend you to
name it ``_styleguide_helpers.scss``.

Once imported you will be able to write manifest using your Sass variables, remember
to define compiler behavior support in your Sass settings: ::

    $pycssstyleguide-compiler-support: "libsass";

Or: ::

    $pycssstyleguide-compiler-support: "dartsass";

Depending you are using a Libsass or Dart Sass compiler. This variable have to be set
after the library import.

.. _sassmixins_source:

_styleguide_helpers.scss
************************

.. literalinclude:: ../py_css_styleguide/scss/_styleguide_helpers.scss

Usage of these mixins depends of your Sass settings, see See :ref:`usage_samples` for
some usages with this Sass library.
