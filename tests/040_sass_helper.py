# -*- coding: utf-8 -*-
import io
import os
import shutil

import pytest

from boussole.project import ProjectBase
from boussole.finder import ScssFinder
from boussole.compiler import SassCompileHelper

from py_css_styleguide.model import Manifest


def test_boussole_compile(fixtures_settings, temp_builds_dir):
    basepath = temp_builds_dir.join('sass_helper_boussole_compile')
    basedir = basepath.strpath

    template_sassdir = os.path.join(fixtures_settings.fixtures_path, 'sass')

    test_sassdir = os.path.join(basedir, 'sass')
    test_config_filepath = os.path.join(test_sassdir, 'settings.json')

    # Copy Sass sources to compile from template
    shutil.copytree(template_sassdir, test_sassdir)

    # Get attempted CSS content from file in fixture
    attempted_css_filepath = os.path.join(
        fixtures_settings.fixtures_path,
        "sass",
        "css",
        "styleguide_manifest.css"
    )
    with io.open(attempted_css_filepath, 'r') as fp:
        attempted_css_content = fp.read()

    # Load boussole settings
    project = ProjectBase(backend_name="json")
    settings = project.backend_engine.load(filepath=test_config_filepath)
    # Search for compilable files
    compilable_files = ScssFinder().mirror_sources(
        settings.SOURCES_PATH,
        targetdir=settings.TARGET_PATH,
        excludes=settings.EXCLUDES
    )

    compiler = SassCompileHelper()
    # Its a loop but for now we only have one file to check
    for src, dst in compilable_files:
        success, message = compiler.safe_compile(settings, src, dst)

        # Output error to ease debug
        if not success:
            print(u"Compile error with: {}".format(src))
            print(message)
        else:
            with io.open(dst, 'r') as fp:
                compiled_content = fp.read()
            assert attempted_css_content == compiled_content
