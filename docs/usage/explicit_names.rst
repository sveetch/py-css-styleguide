
========================
Explicit reference names
========================

With this way, we don't use automatic desciption and explicitely define every
references we retain for description, obviously you will have to maintain correctly
the name list to ensure they exists in references.

Write a Sass file that will use the helpers and settings to build a CSS manifest:

.. literalinclude:: ../../tests/data_fixtures/sass/scss/sample_names.scss
   :language: scss

.. note::
    From ``styleguide-metas-references`` we explicitely define the allow reference
    names to serialize within rule ``--names: "..."``.

Build CSS manifest with your Sass compiler and you should get:

.. literalinclude:: ../../tests/data_fixtures/sass/css/sample_names.css
   :language: css

Then load this manifest with script ``styleguide.py`` and it will return this JSON:

.. literalinclude:: ../../tests/data_fixtures/json/sample_names.json
   :language: json
