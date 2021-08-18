
==============================
Automatic with name exclusions
==============================

This is the simplest way to use, you will let the serializer automatically describe
every reference rules existing within the CSS manifest.

Write a Sass file that will use the helpers and settings to build a CSS manifest:

.. literalinclude:: ../../tests/data_fixtures/sass/scss/styleguide_manifest_excludes.scss
   :language: scss

.. note::
    From ``styleguide-metas-references`` we require to serialize every existing
    references with rule ``--auto: "true"`` but ignoring some names within rule
    ``--excludes: "..."``.

Build CSS manifest with your Sass compiler and you should get:

.. literalinclude:: ../../tests/data_fixtures/sass/css/styleguide_manifest_excludes.css
   :language: css

Then load this manifest with script ``styleguide.py`` and it will return this JSON:

.. literalinclude:: ../../tests/data_fixtures/json/styleguide_manifest_excludes.json
   :language: json