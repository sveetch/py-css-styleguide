
=========
Changelog
=========

Version 1.2.0 - 2024/12/24
**************************

Minor version for new features and improvements.

* Fixed error message from ``ManifestSerializer.serialize_to_flat()`` that was missing
  reference name;
* Added support for Python 3.11 and 3.12;
* Added Django support from 5.0 to 5.1 for included optional Django mixins;
* Added minimal version for all requirements;
* Added new option ``--cleaner`` for splitters. When its value is ``whitespaces`` it
  will remove empty whitespaces that could happen with Sass mixin functions. When this
  property is not defined, the legacy behavior (keep whitespaces) is still used;
* Updated script to freeze local dependencies;
* Removed 'colorama' from requirements since it is automatically installed on Windows
  from 'colorlog';
* Sass mixin library does not include compatibility for both compiler Libsass and
  Dartsass. Now each compiler has its own mixin library;
* Updated documentation;


Version 1.1.1 - 2023/09/24
**************************

Another minor release to change the readthedocs configuration to install this package
and dependencies.

Now we use section ``python.install`` in readthedocs configuration to ask to install
local package from commit with extra requirements for doc building.


Version 1.1.0 - 2023/09/24
**************************

A minor release to fix documentation, add number structure and add a CLI.

* Added a new Python script to automatically build documentation requirements file
  from package setup;
* Changed documentation requirements files to only include the minimal requirements
  without to install package from Pypi;
* Added serialization structure ``number``;
* Added ``ParserErrors`` exception to raise when there is error from parsing CSS
  manifest with ``TinycssSourceParser``;
* Added commandline with ``click`` with ``version`` and ``parse`` commands;


Version 1.0.0 - 2023/09/21
**************************

A major release with breaking changes, see
`Migrations <https://pycssstyleguide.readthedocs.io/en/latest/migrations.html>`_ to
know about migrating your project.

* Dropped Python<3.8 support;
* Added Python support from 3.8 to 3.10;
* Added official Django support from 2.2 to 4.2 for included optional Django mixins;
* Improved Makefile;
* Modernized package configuration;
* Improved documentation:

  * Added Sphinx theme Furo usage;
  * Fixed typo;
  * Reworded some sentences;
  * Upgraded details to fit to last changes;
  * Restructured contents;
  * Added more details;

* Implemented Dart sass compile behaviors support, libsass compiler behaviors is still
  the default one:

  * Added new meta rule ``styleguide-metas-compiler``;
  * Serializer now emit some warnings in some situations;
  * Renamed ``json-list`` to ``object-list``, the first name is still working but
    deprecated with a clear warning about it;
  * Renamed ``json`` to ``object-complex``, the first name is still working but
    deprecated with a clear warning about it;
  * For now the only difference in Dart sass support is about string quotes from
    ``object-list`` and ``object-complex``, it expect strings to be quoted with
    single quotes;

* Changed reference structure validation so the variable ``--structure`` is required;
* Fixed Python code from usage example;
* Removed useless ``# -*- coding: utf-8 -*-`` lines;
* Moved from usage of ``os`` + ``io`` modules in favor of ``pathlib.Path``;
* Added Github issue templates;


Version 0.8.3 - 2023/08/18
**************************

A minor version only to update ``.readthedocs.yml`` file to follow service deprecations
changes.


Version 0.8.2 - 2021/09/12
**************************

* Fix a critical error with CSS manifest relative path to static directory;
* Add "created" item in manifest metas to include datetime of serialization;
* Fix Makefile for correct order of ``freeze-dependencies`` in ``quality`` action
  (freezing requirement must be done before check-release to ensure local package have
  been updated, else the frozen requirements may have a version delay);


Version 0.8.1 - 2021/09/12
**************************

Just a minor release to fix package Readme which was different from documentation.


Version 0.8.0 - 2021/09/12
**************************

* Add a Django view mixin ``StyleguideMixin`` to include in a view to use a manifest;
* Add a basic Django view ``StyleguideViewMixin`` based on ``TemplateView`` and
  ``StyleguideMixin``;
* Add a very basic Django project needed for testing;
* Add Django as a development environment requirement but the package is still not
  dependent from Django in default environment;
* Updated documentation;


Version 0.7.0 - 2021/09/09
**************************

* Rename some model methods:

    * ``set_rule`` to ``_set_rule``;
    * ``remove_rule`` to ``_remove_rule``;

* Implement model method ``from_dict`` to enable loading manifest directly from a
  dictionnary in the same format than ``to_dict`` so it can be used from a JSON dump
  made by ``to_json`` (after have been deserialized).
* Add more manifest reference validations;
* Add ``exceptions`` module for application exceptions;


Version 0.6.0 - 2021/08/19
**************************

* Fix documentation typo issue, close #13;
* Add ``Manifest.to_dict()`` and make ``Manifest.to_json()`` using it, close #14;
* Add property option ``--excludes`` in meta reference rule to ignore some explicitely
  defined reference names in automatic mode, close #10;
* Update Package structure to use more modern configurations;
* Drop support for Python 3.5;
* Add support for Python from 3.6 to 3.8;


Version 0.5.1 - 2019/07/16
**************************

* Added some Sass functions to escape a value from quotes;
* Enabled quote escape on ``get-props-to-json`` and ``get-values-to-json`` functions to
  avoid invalid JSON, close #9;


Version 0.5.0 - 2019/05/05
**************************

* Pinned ``tinycss2`` version to ``>=1.0.2``
* Updated parser so double dashes for CSS variable are correctly supported now, close #8;
* Rewrite package to use setup.cfg and virtualenv (instead of Python-venv);


Version 0.4.0 - 2018/05/09
**************************

* Enforce order on flat structure, close #6;
* Added ``splitter`` property for ``flat``,  ``nested`` and ``list`` structure to be
  able to use either white space separator or JSON list on values, close #7;
* Added JSON structure;
* Added new Sass helpers to build JSON list from Sass lists, map key names, values and
  properties;
* Removed unused method ``ManifestSerializer.format_value``;


Version 0.3.0 - 2018/04/19
**************************

* Added automatic enable references mode, close #1;
* Fixed Sass helper function ``to-string`` for empty list, close #2;
* Changed ``list`` and ``string`` structures so they can be empty, close #3;
* Internally use ``collection.OrderedDict`` instead of simple dictionnary in parser and
  serializer, close #4;
* Fixed code quality issues with Flake8, close #5;


Version 0.2.0 - 2018/04/08
**************************

* Added Sass function ``floor-number-items()``;
* Removed ``flat`` property in favor of ``structure`` to allow other structure modes;
* Added new structure mode ``list``;
* Added new structure mode ``string``;


Version 0.1.0 - 2018/04/07
**************************

* Added documentation with Sphinx;
* Changed ``Manifest.load()`` so it also accepts a file-like object;
* Added test for Sass mixin helper using Boussole;


Version 0.0.2 - 2018/04/04
**************************

* Added ``to_json`` method to Manifest model;
* Fixed some code quality issues;


Version 0.0.1 - 2018/04/02
**************************

First commit with a basic working version.
