PYTHON_INTERPRETER=python3
VENV_PATH=.venv

FRONTEND_DIR=frontend

PYTHON_BIN=$(VENV_PATH)/bin/python
PIP_BIN=$(VENV_PATH)/bin/pip
FLAKE_BIN=$(VENV_PATH)/bin/flake8
PYTEST_BIN=$(VENV_PATH)/bin/pytest
SPHINX_RELOAD_BIN=$(PYTHON_BIN) docs/sphinx_reload.py
TOX_BIN=$(VENV_PATH)/bin/tox
TWINE_BIN=$(VENV_PATH)/bin/twine

PACKAGE_NAME=py-css-styleguide
PACKAGE_SLUG=py_css_styleguide
APPLICATION_NAME=py_css_styleguide

# Formatting variables, FORMATRESET is always to be used last to close formatting
FORMATBLUE:=$(shell tput setab 4)
FORMATGREEN:=$(shell tput setab 2)
FORMATRED:=$(shell tput setab 1)
FORMATBOLD:=$(shell tput bold)
FORMATRESET:=$(shell tput sgr0)

help:
	@echo "Please use 'make <target> [<target>...]' where <target> is one of"
	@echo
	@echo "  Cleaning"
	@echo "  ========"
	@echo
	@echo "  clean                      -- to clean EVERYTHING (Warning)"
	@echo "  clean-doc                  -- to remove documentation builds"
	@echo "  clean-frontend-install     -- to clean frontend installation"
	@echo "  clean-install              -- to clean Python side installation"
	@echo "  clean-pycache              -- to recursively remove all Python cache files"
	@echo
	@echo "  Documentation"
	@echo "  ============="
	@echo
	@echo "  docs                       -- to build documentation"
	@echo "  livedocs                   -- to run a 'live reloaded' server for documentation"
	@echo
	@echo "  Installation"
	@echo "  ============"
	@echo
	@echo "  freeze-dependencies        -- to write installed dependencies versions in frozen.txt"
	@echo "  install                    -- to install this project with virtualenv and Pip"
	@echo "  install-frontend           -- to install frontend (used for tests)"
	@echo
	@echo "  Frontend commands"
	@echo "  ================="
	@echo
	@echo "  css                        -- to build uncompressed CSS from Sass sources"
	@echo "  watch-css                  -- to watch for Sass changes to rebuild CSS"
	@echo "  css-prod                   -- to build compressed and minified CSS from Sass sources"
	@echo "  js                         -- to build uncompressed Javascript from sources"
	@echo "  watch-js                   -- to watch for Javascript sources changes to rebuild assets"
	@echo "  js-prod                    -- to build minified JS assets"
	@echo "  frontend                   -- to build uncompressed frontend assets (CSS, JS, etc..)"
	@echo "  frontend-prod              -- to build minified frontend assets (CSS, JS, etc..)"
	@echo
	@echo "  Quality"
	@echo "  ======="
	@echo
	@echo "  check-release              -- to check package release before uploading it to PyPi"
	@echo "  flake                      -- to launch Flake8 checking"
	@echo "  quality                    -- to launch run quality tasks and checks"
	@echo "  test                       -- to launch base test suite using Pytest"
	@echo "  tox                        -- to launch tests for every Tox environments"
	@echo
	@echo "  Release"
	@echo "  ======="
	@echo
	@echo "  release                    -- to release latest package version on PyPi"
	@echo

clean-pycache:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Clear Python cache <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf .pytest_cache
	find . -type d -name "__pycache__"|xargs rm -Rf
	find . -name "*\.pyc"|xargs rm -f
.PHONY: clean-pycache

clean-frontend-install:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Cleaning frontend install <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf $(FRONTEND_DIR)/node_modules
.PHONY: clean-frontend-install

clean: clean-var clean-doc clean-backend-install clean-frontend-install clean-frontend-build clean-pycache
.PHONY: clean

clean-install:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Clear installation <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf $(VENV_PATH)
	rm -Rf $(PACKAGE_SLUG).egg-info
.PHONY: clean-install

clean-doc:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Clear documentation <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf docs/_build
.PHONY: clean-doc

clean: clean-doc clean-install clean-pycache
.PHONY: clean

venv:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Install virtual environment <---$(FORMATRESET)\n"
	@echo ""
	virtualenv -p $(PYTHON_INTERPRETER) $(VENV_PATH)
.PHONY: venv

install-frontend:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Installing frontend requirements <---$(FORMATRESET)\n"
	@echo ""
	cd $(FRONTEND_DIR) && npm install
.PHONY: install-frontend

install: venv
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Install everything for development <---$(FORMATRESET)\n"
	@echo ""
	$(PIP_BIN) install -e .[dev,django,quality,doc,doc-live,release]
.PHONY: install

css:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Building CSS for development environment <---$(FORMATRESET)\n"
	@echo ""
	cd $(FRONTEND_DIR) && npm run-script css
.PHONY: css

watch-sass:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Watching Sass sources for development environment <---$(FORMATRESET)\n"
	@echo ""
	cd $(FRONTEND_DIR) && npm run-script watch-css
.PHONY: watch-sass

css-prod:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Building CSS for production environment <---$(FORMATRESET)\n"
	@echo ""
	cd $(FRONTEND_DIR) && npm run-script css-prod
.PHONY: css-prod

docs:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Build documentation <---$(FORMATRESET)\n"
	@echo ""
	cd docs && make html
.PHONY: docs

livedocs:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Watching documentation sources <---$(FORMATRESET)\n"
	@echo ""
	$(SPHINX_RELOAD_BIN)
.PHONY: livedocs

flake:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Flake <---$(FORMATRESET)\n"
	@echo ""
	$(FLAKE_BIN) --statistics --show-source $(APPLICATION_NAME) tests
.PHONY: flake

test:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Tests <---$(FORMATRESET)\n"
	@echo ""
	$(PYTEST_BIN) -vv tests/
.PHONY: test

freeze-dependencies:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Freeze dependencies versions <---$(FORMATRESET)\n"
	@echo ""
	$(PYTHON_BIN) freezer.py ${PACKAGE_NAME} --destination=frozen.txt
.PHONY: freeze-dependencies

build-package:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Build package <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf dist
	$(VENV_PATH)/bin/python setup.py sdist
.PHONY: build-package

release: build-package
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Release package <---$(FORMATRESET)\n"
	@echo ""
	$(TWINE_BIN) upload dist/*
.PHONY: release

check-release: build-package
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Check package <---$(FORMATRESET)\n"
	@echo ""
	$(TWINE_BIN) check dist/*
.PHONY: check-release

tox:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Launch all Tox environments <---$(FORMATRESET)\n"
	@echo ""
	$(TOX_BIN)
.PHONY: tox

quality: test flake docs check-release freeze-dependencies
	@echo ""
	@printf "$(FORMATGREEN)$(FORMATBOLD) ♥ ♥ Everything should be fine ♥ ♥ $(FORMATRESET)\n"
	@echo ""
	@echo ""
.PHONY: quality
