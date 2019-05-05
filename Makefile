PYTHON_INTERPRETER=python3
VENV_PATH=.venv
PIP=$(VENV_PATH)/bin/pip
FLAKE=$(VENV_PATH)/bin/flake8
PYTEST=$(VENV_PATH)/bin/pytest
PACKAGE_NAME=py_css_styleguide

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo
	@echo "  clean               -- to clean EVERYTHING (Warning)"
	@echo "  clean-pycache       -- to remove all __pycache__, this is recursive from current directory"
	@echo "  clean-install       -- to clean Python side installation"
	@echo ""
	@echo "  install             -- to install this project with virtualenv and Pip with everything for development"
	@echo ""
	@echo "  flake               -- to launch Flake8 checking on code (not the tests)"
	@echo "  tests               -- to launch tests using py.test"
	@echo "  quality             -- to launch Flake8 checking and tests with py.test"
	@echo

clean-pycache:
	rm -Rf .pytest_cache
	find . -type d -name "__pycache__"|xargs rm -Rf
	find . -name "*\.pyc"|xargs rm -f
.PHONY: clean-pycache

clean-install:
	rm -Rf $(VENV_PATH)
	rm -Rf dist
	rm -Rf .tox
	rm -Rf $(PACKAGE_NAME).egg-info
.PHONY: clean-install

clean: clean-install clean-pycache
.PHONY: clean

venv:
	virtualenv -p $(PYTHON_INTERPRETER) $(VENV_PATH)
	# This is required for those ones using ubuntu<16.04
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade setuptools
.PHONY: venv

install: venv
	$(PIP) install -e .[dev]
.PHONY: install

flake:
	$(FLAKE) --show-source $(PACKAGE_NAME)
.PHONY: flake

tests:
	$(PYTEST) -vv tests
.PHONY: tests

quality: tests flake
.PHONY: quality
