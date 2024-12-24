
======================
The full automatic way
======================

This is the simplest way to use where you will let the serializer automatically
describes every reference rules existing within the CSS manifest.

First write a Sass file that will use the helpers and settings to build a CSS manifest:

.. literalinclude:: ../../tests/data_fixtures/sass/scss/sample_libsass.scss

.. note::
    From ``styleguide-metas-references`` we require to serialize every existing
    references with the simple rule ``--auto: "true"``.

Then build CSS manifest with your Sass compiler and you should get:

.. literalinclude:: ../../tests/data_fixtures/sass/css/sample_libsass.css
   :language: css

Finally load this manifest with command :ref:`cli_parse` and it will return this JSON:

.. literalinclude:: ../../tests/data_fixtures/json/sample_libsass.json
   :language: json
