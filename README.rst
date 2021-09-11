
.. _tinycss2: https://github.com/Kozea/tinycss2

PyCssStyleguide
===============

A Python library to build a styleguide from a CSS manifest file.

Goal
****

Many styleguide builders stand on comments in Sass or CSS sources. This is very verbose
in sources and sometime requires you to maintain every variables values when you change
them in sources.

In our modern era we mostly build CSS from Sass or Less sources with
variables/settings. This library encourages you to describe and structure your variables
in a manifest which will be compiled to a dedicated CSS file.

Manifest syntax rules are valid CSS (mostly using CSS3 variables).

Then the CSS manifest is parsed to return a Python object with all your descriptions so
you can use them to build your styleguide in code or a template.

Features
********

* A Sass source with some mixin helpers to help you to write CSS manifest from your
  Sass sources;
* An interface to load a CSS manifest and return it as dictionnary of datas;
* Django mixin and view to load manifest from your project or application (this library
  does not require Django, so you may use it in another way);

Links
*****

* Read the documentation on `Read the docs <https://pycssstyleguide.readthedocs.io/>`_;
* Download its `PyPi package <http://pypi.python.org/pypi/py-css-styleguide>`_;
* Clone it on its `Github repository <https://github.com/sveetch/py-css-styleguide>`_;

Dependancies
************

* `tinycss2`_;
