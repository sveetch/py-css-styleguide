
======================
The full automatic way
======================

This is the simplest way to use, you will let the serializer automatically describe
every reference rules existing within the CSS manifest.

Write a Sass file that will use the helpers and settings to build a CSS manifest:

.. literalinclude:: ../../tests/data_fixtures/sass/scss/sample_libsass.scss
   :language: scss

.. note::
    From ``styleguide-metas-references`` we require to serialize every existing
    references with the simple rule ``--auto: "true"``.

Build CSS manifest with your Sass compiler and you should get:

.. literalinclude:: ../../tests/data_fixtures/sass/css/sample_libsass.css
   :language: css

Then load this manifest with script ``styleguide.py`` and it will return this JSON:

.. literalinclude:: ../../tests/data_fixtures/json/sample_libsass.json
   :language: json
