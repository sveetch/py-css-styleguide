
=========
Changelog
=========

Version 0.4.0 - 2018/05/09
--------------------------

* Enforce order on flat structure, close #6;
* Added ``splitter`` property for ``flat``,  ``nested`` and ``list`` structure to be able to use either white space separator or JSON list on values, close #7;
* Added JSON structure;
* Added new Sass helpers to build JSON list from Sass lists, map key names, values and properties;
* Removed unused method ``ManifestSerializer.format_value``;

Version 0.3.0 - 2018/04/19
--------------------------

* Added automatic enable references mode, close #1;
* Fixed Sass helper function ``to-string`` for empty list, close #2;
* Changed ``list`` and ``string`` structures so they can be empty, close #3;
* Internally use ``collection.OrderedDict`` instead of simple dictionnary in parser and serializer, close #4;
* Fixed code quality issues with Flake8, close #5;

Version 0.2.0 - 2018/04/08
--------------------------

* Added Sass function ``floor-number-items()``;
* Removed ``flat`` property in favor of ``structure`` to allow other structure modes;
* Added new structure mode ``list``;
* Added new structure mode ``string``;

Version 0.1.0 - 2018/04/07
--------------------------

* Added documentation with Sphinx;
* Changed ``Manifest.load()`` so it also accepts a file-like object;
* Added test for Sass mixin helper using Boussole;

Version 0.0.2 - 2018/04/04
--------------------------

* Added ``to_json`` method to Manifest model;
* Fixed some code quality issues;

Version 0.0.1 - 2018/04/02
--------------------------

First commit with a basic working version.
