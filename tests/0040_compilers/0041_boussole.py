import json
import shutil

from pathlib import Path

import pytest

from freezegun import freeze_time

from boussole.project import ProjectBase
from boussole.finder import ScssFinder
from boussole.compiler import SassCompileHelper

from py_css_styleguide.model import Manifest


@freeze_time("2012-10-15 10:00:00")
@pytest.mark.parametrize(
    "manifest_name",
    ["sample_libsass", "sample_excludes", "sample_names"],
)
def test_boussole_compile_auto(tests_settings, tmp_path, manifest_name):
    """
    Testing everything:

    * Sass helpers correctly generate CSS;
    * Manifest is correctly serialized to expected datas;
    * Builded CSS is the same than stored one in data fixtures;

    .. TODO:
        The Dartsass version "sample_dartsass" is not tested anymore because Libsass
        used by Boussole is not able to manage "@use" rule to import builtin modules
        from Dartsass.

        Package development would need to install a Dart sass compiler that we could
        execute to compile the Dart sass version.
    """
    manifest_css = "{}.css".format(manifest_name)
    manifest_json = (
        tests_settings.fixtures_path / "json" / "{}.json".format(manifest_name)
    )

    # Open JSON fixture for expected serialized data from parsed manifest
    expected = json.loads(manifest_json.read_text())

    template_sassdir = tests_settings.fixtures_path / "sass"

    test_sassdir = tmp_path / "sass"
    test_config_filepath = test_sassdir / "settings.json"

    # Copy Sass sources to compile from template
    shutil.copytree(template_sassdir, test_sassdir)

    # Get expected CSS content from file in fixture
    expected_css_filepath = tests_settings.fixtures_path / "sass" / "css" / manifest_css
    expected_css_content = expected_css_filepath.read_text()

    # Load boussole settings and search for compilable files
    project = ProjectBase(backend_name="json")
    settings = project.backend_engine.load(filepath=test_config_filepath)
    compilable_files = ScssFinder().mirror_sources(
        settings.SOURCES_PATH,
        targetdir=settings.TARGET_PATH,
        excludes=settings.EXCLUDES,
    )

    # Since Boussole list every compilable Sass source, we select only the entry
    # corresponding to the manifest we seek for (from "manifest_css" dir)
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
        settings, source_sass_filename, source_css_filename
    )

    # Output error to ease debug
    if not success:
        print("Compile error with: {}".format(source_sass_filename))
        print(message)
        assert 1 == 42
    else:
        # Built CSS is identical to the expected one from fixture
        compiled_content = Path(source_css_filename).read_text()
        assert expected_css_content == compiled_content

        # Described manifest is the same as expected payload from fixture
        manifest = Manifest()
        manifest.load(compiled_content)
        dump = json.loads(manifest.to_json())
        assert expected == dump
