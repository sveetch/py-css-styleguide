.. _Python: https://www.python.org/
.. _tinycss2: https://github.com/Kozea/tinycss2

PyCssStyleguide
===============

This is a Python library to build a design styleguide from a CSS manifest file.

Opposed to many styleguide builders this does not require to documentate styles from
your stylesheets. Instead it is based on Sass variables to build a map of your style
rules.


Features
********

* Python interface to load a CSS manifest and return it as a Python dictionnary or
  JSON data;
* (Optional) Tiny Sass mixin library to write CSS manifest from your Sass project
  settings;
* (Optional) Django mixin and view to load manifest from your project or application;


Links
*****

* Read the documentation on `Read the docs <https://pycssstyleguide.readthedocs.io/>`_;
* Download its `PyPi package <http://pypi.python.org/pypi/py-css-styleguide>`_;
* Clone it on its `Github repository <https://github.com/sveetch/py-css-styleguide>`_;


Dependencies
************

* `Python`_>=3.8;
* `tinycss2`_>=1.1.0;


Credits
*******

Logo vector and icon by `SVG Repo <https://www.svgrepo.com>`_.
