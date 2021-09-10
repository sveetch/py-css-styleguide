# -*- coding: utf-8 -*-
import io
import json
import os
import shutil

import pytest

from boussole.project import ProjectBase
from boussole.finder import ScssFinder
from boussole.compiler import SassCompileHelper

from py_css_styleguide.model import Manifest


@pytest.mark.parametrize('manifest_name', [
    "styleguide_manifest_full",
    "styleguide_manifest_excludes",
    "styleguide_manifest_names",
])
def test_boussole_compile_auto(tests_settings, temp_builds_dir, manifest_name):
    """
    Testing everything:

    * Sass helpers correctly generate CSS;
    * Manifest is correctly serialized to expected datas;
    * Builded CSS is the same than stored one in data fixtures;
    """
    manifest_css = manifest_name + ".css"
    manifest_json = os.path.join(
        tests_settings.fixtures_path,
        'json',
        manifest_name + ".json",
    )

    # Open JSON fixture for expected serialized data from parsed manifest
    with open(manifest_json, "r") as fp:
        expected = json.load(fp)

    basepath = temp_builds_dir.join(
        'sass_helper_boussole_compile_{}'.format(manifest_css)
    )
    basedir = basepath.strpath

    template_sassdir = os.path.join(tests_settings.fixtures_path, 'sass')

    test_sassdir = os.path.join(basedir, 'sass')
    test_config_filepath = os.path.join(test_sassdir, 'settings.json')

    # Copy Sass sources to compile from template
    shutil.copytree(template_sassdir, test_sassdir)

    # Get expected CSS content from file in fixture
    expected_css_filepath = os.path.join(
        tests_settings.fixtures_path,
        "sass",
        "css",
        manifest_css
    )
    with io.open(expected_css_filepath, 'r') as fp:
        expected_css_content = fp.read()

    # Load boussole settings and search for compilable files
    project = ProjectBase(backend_name="json")
    settings = project.backend_engine.load(filepath=test_config_filepath)
    compilable_files = ScssFinder().mirror_sources(
        settings.SOURCES_PATH,
        targetdir=settings.TARGET_PATH,
        excludes=settings.EXCLUDES
    )

    # Since Boussole list every compilable Sass source, we select only the entry
    # corresponding to the manifest we seek for (from "manifest_css")
    source_css_filename = None
    source_sass_filename = None
    for k, v in compilable_files:
        if v.endswith(manifest_css):
            source_sass_filename = k
            source_css_filename = v
            break

    # Compile only the source we target from "manifest_css"
    compiler = SassCompileHelper()
    success, message = compiler.safe_compile(
        settings,
        source_sass_filename,
        source_css_filename
    )

    # Output error to ease debug
    if not success:
        print(u"Compile error with: {}".format(source_sass_filename))
        print(message)
    else:
        # Builded CSS is identical to the expected one from fixture
        with io.open(source_css_filename, 'r') as fp:
            compiled_content = fp.read()
        assert expected_css_content == compiled_content

        # Described manifest is the same as expected payload from fixture
        manifest = Manifest()
        manifest.load(compiled_content)
        dump = json.loads(manifest.to_json())
        assert expected == dump
