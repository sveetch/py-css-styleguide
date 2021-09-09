.. _virtualenv: https://virtualenv.pypa.io
.. _pip: https://pip.pypa.io
.. _Pytest: http://pytest.org
.. _Napoleon: https://sphinxcontrib-napoleon.readthedocs.org
.. _Flake8: http://flake8.readthedocs.org
.. _Sphinx: http://www.sphinx-doc.org
.. _tox: http://tox.readthedocs.io
.. _livereload: https://livereload.readthedocs.io
.. _twine: https://twine.readthedocs.io

.. _intro_development:

===========
Development
===========

Development requirements
************************

py-css-styleguide is developed with:

* *Test Development Driven* (TDD) using `Pytest`_;
* Respecting flake and pip8 rules using `Flake8`_;
* `Sphinx`_ for documentation with enabled `Napoleon`_ extension (using
  *Google style*);
* `tox`_ to run tests on various environments;

Every requirements are available in package extra requirements in section
``dev``.

.. _install_development:

Install for development
***********************

First ensure you have `pip`_ and `virtualenv`_ packages installed then
type: ::

    git clone https://github.com/sveetch/py-css-styleguide.git
    cd py-css-styleguide
    make install

py-css-styleguide will be installed in editable mode from the
latest commit on master branch with some development tools.

Unittests
---------

Unittests are made to works on `Pytest`_, a shortcut in Makefile is available
to start them on your current development install: ::

    make test


Tox
---

To ease development against multiple Python versions a tox configuration has
been added. You are strongly encouraged to use it to test your pull requests.

Before using it you will need to install tox, you need to install it: ::

    .venv/bin/pip install tox

Then execute tox: ::

    .venv/bin/tox

Tox is a common utility which you may install globally on your system to avoid
installing it each time in your virtual environments.

Documentation
-------------

You can easily build the documentation from one Makefile action: ::

    make docs

There is Makefile action ``livedocs`` to serve documentation and automatically
rebuild it when you change documentation files: ::

    make livedocs

Then go on ``http://localhost:8002/`` or your server machine IP with port 8002.

Note that you need to build the documentation at least once before using
``livedocs``.

Releasing
---------

When you have a release to do, after you have correctly push all your commits
you can use the shortcut: ::

    make release

Which will build the package release and send it to Pypi with `twine`_.
You may think to
`configure your Pypi account <https://twine.readthedocs.io/en/latest/#configuration>`_
on your machine to avoid to input it each time.

Contribution
------------

* Every new feature or changed behavior must pass tests, Flake8 code quality
  and must be documented.
* Every feature or behavior must be compatible for all supported environment.
