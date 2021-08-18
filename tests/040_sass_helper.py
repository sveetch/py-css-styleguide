# -*- coding: utf-8 -*-
import io
import json
import os
import shutil

from boussole.project import ProjectBase
from boussole.finder import ScssFinder
from boussole.compiler import SassCompileHelper

from py_css_styleguide.model import Manifest


def test_boussole_compile(fixtures_settings, temp_builds_dir):
    """
    Testing everything, this implies Sass helpers correctly generate CSS,
    builded CSS is the same than stored one in data fixtures and
    manifest is correctly serialized to expected datas.
    """
    expected_serialization = {
        'styleguide_manifest.css': {
            "metas": {
                "references": [
                    "palette",
                    "schemes",
                    "borders",
                    "gradients",
                    "grid_cell_sizes",
                    "version"
                ]
            },
            "gradients": [
                "linear-gradient(#f69d3c, #3f87a6)",
                "radial-gradient(#f69d3c, #3f87a6 50px)"
            ],
            "borders": {
                "thin": {
                    "size": "rem-calc(1px)",
                    "style": "solid",
                    "color": "white"
                },
                "normal": {
                    "size": "rem-calc(3px)",
                    "style": "solid",
                    "color": "white"
                },
                "bold": {
                    "size": "rem-calc(5px)",
                    "style": "solid",
                    "color": "black"
                }
            },
            "grid_cell_sizes": {
                "5": "5",
                "25": "25",
                "33": "33.3333",
                "75": "75",
                "100": "100"
            },
            "version": "42.0",
            "palette": {
                "black": "#000000",
                "white": "#ffffff",
                "grey": "#404040"
            },
            "schemes": {
                "black": {
                    "selector": ".bg-black",
                    "background": "#000000",
                    "font_color": "#ffffff"
                },
                "grey": {
                    "selector": ".bg-grey",
                    "background": "#404040",
                    "font_color": "#ffffff"
                },
                "white": {
                    "selector": ".bg-white",
                    "background": "#ffffff",
                    "font_color": "#000000"
                },
                "grey-gradient": {
                    "selector": ".bg-grey-gradient",
                    "background": "linear-gradient(#ffffff, #ffffff 85%, #404040)",
                    "font_color": "#000000"
                },
                "with-image": {
                    "selector": ".bg-with-image",
                    "background": "url(u0022foo/bar.pngu0022)",
                    "font_color": "#000000"
                }
            }
        },
    }

    basepath = temp_builds_dir.join('sass_helper_boussole_compile')
    basedir = basepath.strpath

    template_sassdir = os.path.join(fixtures_settings.fixtures_path, 'sass')

    test_sassdir = os.path.join(basedir, 'sass')
    test_config_filepath = os.path.join(test_sassdir, 'settings.json')

    # Copy Sass sources to compile from template
    shutil.copytree(template_sassdir, test_sassdir)

    # Get expected CSS content from file in fixture
    expected_css_filepath = os.path.join(
        fixtures_settings.fixtures_path,
        "sass",
        "css",
        "styleguide_manifest.css"
    )
    with io.open(expected_css_filepath, 'r') as fp:
        expected_css_content = fp.read()

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
            datas_keyname = os.path.basename(dst)

            with io.open(dst, 'r') as fp:
                compiled_content = fp.read()
            assert expected_css_content == compiled_content

            manifest = Manifest()
            manifest.load(compiled_content)
            dump = json.loads(manifest.to_json())

            assert expected_serialization[datas_keyname] == dump
