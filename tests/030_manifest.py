# -*- coding: utf-8 -*-
import pytest

from py_css_styleguide.manifest import Manifest


def test_manifest_load():
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
