
============
Usage sample
============

1. Writing a CSS manifest
*************************

Write it to a ``styleguide_manifest.css`` file: ::

    .styleguide-metas-references{
        names: "palette text_color";
    }

    .styleguide-reference-palette{
        flat: "true";
        keys: "black white";
        values: "#000000 #ffffff";
    }

    .styleguide-reference-text_color{
        keys: "black white";
        selectors: ".bg-black .bg-white";
        values: "#000000 #ffffff";
    }

2. Writing Python script to load manifest
*****************************************

Once you have a CSS manifest you will need to load it as a Manifest model through PyCssStyleguide library.

Create a Python script ``styleguide.py`` in the same directory than previous writed CSS file: ::

    import io

    from py_css_styleguide.manifest import Manifest

    manifest = Manifest()

    with io.open('styleguide_manifest.css', 'r') as fp:
        manifest.load(fp)

    print(manifest.to_json())

And here you go, when executed this basic script will output JSON datas from your manifest.

Starting from this you should be able to use this in your application to build a styleguide page.

3. Don't write CSS manifest
***************************

Everything before was to introduce you to manifest to know how they work. But this not really easy to manually write and maintain CSS manifest.

The real benefit comes when you build manifest from Sass sources so this will automatically update manifest when you change your Sass settings.

So go into your Sass source directory and copy `this Sass file <https://github.com/sveetch/py-css-styleguide/blob/master/py_css_styleguide/scss/_styleguide_helpers.scss>`_ to ``_styleguide_helpers.scss``. It contains some mixin helper to ease writing manifest from Sass maps.

Then for this sample purpose we will create a dummy settings file to ``_settings.scss``: ::

    $black: #000000;
    $white: #ffffff;

    // Palette
    // ---------
    $palette: (
        black: $black;
        white: $white;
    );

    // Text colors
    // ---------
    $text-colors: (
        black: $black;
        white: $white;
    );

This is very basic settings for some color schemes but this enough for our sample.

