
==============================
Automatic with name exclusions
==============================

This way is still in "automatic describing all references" but you are able to exclude
some references.

Write a Sass file that will use the helpers and settings to build a CSS manifest:

.. literalinclude:: ../../tests/data_fixtures/sass/scss/sample_excludes.scss
   :language: scss

.. note::
    From ``styleguide-metas-references`` we require to serialize every existing
    references with rule ``--auto: "true"`` but ignoring some names within rule
    ``--excludes: "..."``.

Build CSS manifest with your Sass compiler and you should get:

.. literalinclude:: ../../tests/data_fixtures/sass/css/sample_excludes.css
   :language: css

Then load this manifest with script ``styleguide.py`` and it will return this JSON:

.. literalinclude:: ../../tests/data_fixtures/json/sample_excludes.json
   :language: json
