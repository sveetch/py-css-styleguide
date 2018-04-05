# -*- coding: utf-8 -*-
import io
import json
import os
import pytest

from py_css_styleguide.manifest import Manifest


def test_manifest_load_string():
    source = (
        '.styleguide-metas-references{\n'
        '    names: "palette schemes";\n'
        '}\n'
        '\n'
        '.styleguide-reference-palette{\n'
        '    flat: "true";\n'
        '    keys: "black white";\n'
        '    values: "#000000 #ffffff";\n'
        '}\n'
        '\n'
        '.styleguide-reference-schemes{\n'
        '    keys: "black white";\n'
        '    selectors: ".bg-black .bg-white";\n'
        '    values: "#000000 #ffffff";\n'
        '}'
    )

    manifest = Manifest()
    manifest.load(source)

    assert manifest._path == None

    assert sorted(manifest.metas.get('references')) == sorted([
        'palette',
        'schemes'
    ])

    assert manifest.palette == {
        'white': '#ffffff',
        'black': '#000000',
    }

    assert manifest.schemes == {
        'black': {
            'selectors': ".bg-black",
            'values': "#000000",
        },
        'white': {
            'values': "#ffffff",
            'selectors': ".bg-white",
        },
    }


def test_manifest_load_fileobject(fixtures_settings):
    source_filepath = os.path.join(
        fixtures_settings.fixtures_path,
        "manifest_sample.css"
    )

    manifest = Manifest()

    with io.open(source_filepath, 'r') as fp:
        manifest.load(fp)

    assert manifest._path == source_filepath

    assert sorted(manifest.metas.get('references')) == sorted([
        'palette',
        'schemes'
    ])

    assert manifest.palette == {
        'white': '#ffffff',
        'black': '#000000',
    }

    assert manifest.schemes == {
        'black': {
            'selectors': ".bg-black",
            'values': "#000000",
        },
        'white': {
            'values': "#ffffff",
            'selectors': ".bg-white",
        },
    }


def test_manifest_to_json():
    source = (
        '.styleguide-metas-references{\n'
        '    names: "palette schemes";\n'
        '}\n'
        '\n'
        '.styleguide-reference-palette{\n'
        '    flat: "true";\n'
        '    keys: "black white";\n'
        '    values: "#000000 #ffffff";\n'
        '}\n'
        '\n'
        '.styleguide-reference-schemes{\n'
        '    keys: "black white";\n'
        '    selectors: ".bg-black .bg-white";\n'
        '    values: "#000000 #ffffff";\n'
        '}'
    )

    manifest = Manifest()
    manifest.load(source)

    dump = json.loads(manifest.to_json())

    attempted = {
        'metas': {
            'references': [
                'palette',
                'schemes',
            ],
        },
        'palette': {
            'white': '#ffffff',
            'black': '#000000',
        },
        'schemes': {
            'black': {
                'selectors': ".bg-black",
                'values': "#000000",
            },
            'white': {
                'values': "#ffffff",
                'selectors': ".bg-white",
            },
        },
    }

    assert dump == attempted
