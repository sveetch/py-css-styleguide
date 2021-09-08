VENV_PATH=.venv
PYTHON_INTERPRETER=python3
PYTHON_BIN=$(VENV_PATH)/bin/python
PIP=$(VENV_PATH)/bin/pip
TWINE=$(VENV_PATH)/bin/twine
FLAKE=$(VENV_PATH)/bin/flake8
PYTEST=$(VENV_PATH)/bin/pytest
SPHINX_RELOAD=$(VENV_PATH)/bin/python sphinx_reload.py

PACKAGE_NAME=py-css-styleguide
PACKAGE_SLUG=`echo $(PACKAGE_NAME) | tr '-' '_'`
APPLICATION_NAME=py_css_styleguide

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo
	@echo "  install             -- to install this project with virtualenv and Pip"
	@echo "  freeze-dependencies -- to write a frozen.txt file with installed dependencies versions"
	@echo
	@echo "  clean               -- to clean EVERYTHING (Warning)"
	@echo "  clean-doc           -- to remove documentation builds"
	@echo "  clean-install       -- to clean Python side installation"
	@echo "  clean-pycache       -- to remove all __pycache__, this is recursive from current directory"
	@echo
	@echo "  docs                -- to build documentation"
	@echo "  livedocs            -- to run livereload server to rebuild documentation on source changes"
	@echo
	@echo "  flake               -- to launch Flake8 checking"
	@echo "  test                -- to launch base test suite using Pytest"
	@echo "  quality             -- to launch Flake8 checking, tests suites, documentation building, freeze dependencies and check release"
	@echo
	@echo "  check-release       -- to check package release before uploading it to PyPi"
	@echo "  release             -- to release package for latest version on PyPi (once release has been pushed to repository)"
	@echo

clean-pycache:
	@echo ""
	@echo "==== Clear Python cache ===="
	@echo ""
	rm -Rf .pytest_cache
	find . -type d -name "__pycache__"|xargs rm -Rf
	find . -name "*\.pyc"|xargs rm -f
.PHONY: clean-pycache

clean-install:
	@echo ""
	@echo "==== Clear installation ===="
	@echo ""
	rm -Rf dist
	rm -Rf .tox
	rm -Rf $(VENV_PATH)
	rm -Rf $(PACKAGE_SLUG).egg-info
.PHONY: clean-install

clean-doc:
	@echo ""
	@echo "==== Clear documentation ===="
	@echo ""
	rm -Rf docs/_build
.PHONY: clean-doc

clean: clean-doc clean-install clean-pycache
.PHONY: clean

venv:
	@echo ""
	@echo "==== Install virtual environment ===="
	@echo ""
	virtualenv -p $(PYTHON_INTERPRETER) $(VENV_PATH)
	# This is required for those ones using old distribution
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade setuptools
.PHONY: venv

install: venv
	@echo ""
	@echo "==== Install everything for development ===="
	@echo ""
	$(PIP) install -e .[dev]
.PHONY: install

docs:
	@echo ""
	@echo "==== Build documentation ===="
	@echo ""
	cd docs && make html
.PHONY: docs

livedocs:
	@echo ""
	@echo "==== Watching documentation sources ===="
	@echo ""
	$(SPHINX_RELOAD)
.PHONY: livedocs

flake:
	@echo ""
	@echo "==== Flake ===="
	@echo ""
	$(FLAKE) --show-source $(APPLICATION_NAME)
	$(FLAKE) --show-source tests
.PHONY: flake

test:
	@echo ""
	@echo "==== Tests ===="
	@echo ""
	$(PYTEST) -vv tests/
.PHONY: test

freeze-dependencies:
	@echo ""
	@echo "==== Freeze dependencies versions ===="
	@echo ""
	$(VENV_PATH)/bin/python freezer.py
.PHONY: freeze-dependencies

build-package:
	@echo ""
	@echo "==== Build package ===="
	@echo ""
	rm -Rf dist
	$(VENV_PATH)/bin/python setup.py sdist
.PHONY: build-package

release: build-package
	@echo ""
	@echo "==== Release ===="
	@echo ""
	$(TWINE) upload dist/*
.PHONY: release

check-release: build-package
	@echo ""
	@echo "==== Check package ===="
	@echo ""
	$(TWINE) check dist/*
.PHONY: check-release


quality: flake docs freeze-dependencies check-release
	@echo ""
	@echo "♥ ♥ Everything should be fine ♥ ♥"
	@echo ""
.PHONY: quality
