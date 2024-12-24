
.. _usage_intro:

=====
Usage
=====

You need a CSS manifest to describe your styleguide references then you will parse the
manifest with a Python script to parse and serialize your references.

.. Note::
    This document does not explain the reference rules syntax in detail, you will
    find them in :ref:`manifest_intro`.

.. _usage_manifest:

Create a manifest
*****************

You may write directly a CSS manifest but this is better to build it from a Sass source
that will be able to use your project Sass settings, so manifest can be automatically
updated on each build.

Usage samples in this documentation will only demonstrate this process using Sass
sources.

So in the same directory than your Sass manifest you will copy the
:ref:`sassmixins_intro` file to ``_styleguide_helpers.scss``. It contains some Sass
helpers to ease writing manifest from Sass maps.

.. Hint::
    You can use the command :ref:`cli_parse` to check your CSS manifest.


.. _usage_demo_settings:

Demonstration settings
**********************

We will use some Sass settings for demonstration which Sass manifest will use to create
manifest references.

You will create a file ``_settings.scss`` in your Sass directory with this content:

.. literalinclude:: ../../tests/data_fixtures/sass/scss/_settings.scss
   :language: scss

This is basic Sass settings for demonstration purpose and obviously for a real project
you will use your own (like from Bootstrap, Foundation or a totally custom one)
depending your project.


.. _usage_loader:

Manifest loader
***************

Once you have a CSS manifest you will need to load it as a Manifest model through
PyCssStyleguide library. There is a commandline script :ref:`cli_parse` to do it but
for integration in a project you may prefer to use your own script.

The following Python snippet is a sample of a custom script you can start from: ::

    from pathlib import Path

    from py_css_styleguide.model import Manifest

    manifest = Manifest()

    manifest.load(Path("styleguide_manifest.css").read_text())

    print(manifest.to_json())

When executed this basic script will output JSON datas from your manifest.

.. Note::
    This sample use ``Manifest.to_json()`` for simplicity but you could also use
    manifest object attributes to reach references rules.


.. _usage_samples:

Samples
*******

For the following samples, you will use the ``_settings.scss``, the
:ref:`sassmixins_intro` and the manifest parser commandline script from
:ref:`cli_parse`.

.. toctree::
   :maxdepth: 2

   auto_full.rst
   auto_excludes.rst
   explicit_names.rst
