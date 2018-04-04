.. _Sveetoy: https://sveetch.github.io/Sveetoy/

==============
CSS Styleguide
==============

A Python library to build a styleguide from a CSS manifest file.

It is way of building a styleguide without to write declarations inside CSS comments in your stylesheets.

You build a manifest in a dedicated CSS file and it will be parsed and serialized so you can use it in your code or templates to build a styleguide.

Why a dedicated CSS file for a manifest ? Because it can be automatically writed from your Sass sources. Obviously it would only work if your design is driven by variables like with *Foundation for Site* or *Bootstrap*.

Manifest syntax rules are writed so the CSS file is still a valid CSS, mostly using CSS3 variables.

Actually this library provide an API to load a CSS manifest and return it has structured datas.

Links
*****

* Download its `PyPi package <http://pypi.python.org/pypi/py-css-styleguide>`_;
* Clone it on its `Github repository <https://github.com/sveetch/py-css-styleguide>`_;

Dependancies
************

* ``tinycss2``;

Usage
-----

TODO

