.. _overview_intro:

========
Overview
========

Introduction
************

Many styleguide builders stand on comments in Sass or CSS sources. This is very verbose
in sources and sometime requires you to maintain every variables values when you change
them in sources.

In our modern era we mostly build CSS from a pre-compiler like Sass or Less using
variable settings that we can stand on to automatize styleguide manifest.

.. Note::
    Since PyCssStyleguide only parse a CSS file, you would be able to use it with any
    pre-compiler like Sass, Less, Stylus, etc..

    However we only support a Sass mixin library and the documentation only have
    samples with Sass.

Finally our point of view of a styleguide is not to demonstrate every CSS components or
objects with their variants. You could do it but it is seems a long work that would
require a lot of maintenance.

We prefer to consider styleguide a as cheat sheet for your base settings like font
sizes, colors, basic object variants, etc.. that can be demonstrated visually in a
single page. You should focus first on establish these bases, once done you may possibly
start to demonstrate more high level objects or components.


Basic example
*************

With a basic CSS manifest like this: ::

    .styleguide-reference-dummy {
        --structure: "flat";
        --keys: "foo bar";
        --values: "#000000 #ffffff";
    }

Once given to PyCssStyleguide interface, you would get the following JSON : ::

    {
        "dummy": {
            "foo": "#000000",
            "bar": "#ffffff"
        }
    }

.. Note::
    In practice you won't write manifest directly in a CSS and there is a lot more data
    structures available to work with your settings diversity.


Workflow
********

This library encourages you to describe and structure your variables in a manifest
which will be compiled to a dedicated CSS file.

#. Build your design settings;
#. Reference your style rules using settings into a dedicated CSS for the manifest;
#. Use PyCssStyleguide to parse and load manifest;
#. Write a page view in your project that exploit manifest data to build styleguide;

PyCssStyleguide don't deliver a full ready to publish styleguide, only data that it is
on your own to use in a template to build the styleguide you whish.
