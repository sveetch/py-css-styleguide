
========================
Explicit reference names
========================

This is the simplest way to use, you will let the serializer automatically describe
every reference rules existing within the CSS manifest.

Write a Sass file that will use the helpers and settings to build a CSS manifest:

.. literalinclude:: ../../tests/data_fixtures/sass/scss/styleguide_manifest_names.scss
   :language: scss

.. note::
    From ``styleguide-metas-references`` we explicitely define the allow reference
    names to serialize within rule ``--names: "..."``.

Build CSS manifest with your Sass compiler and you should get:

.. literalinclude:: ../../tests/data_fixtures/sass/css/styleguide_manifest_names.css
   :language: css

Then load this manifest with script ``styleguide.py`` and it will return this JSON:

.. literalinclude:: ../../tests/data_fixtures/json/styleguide_manifest_names.json
   :language: json
