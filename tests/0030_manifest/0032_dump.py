import json

from freezegun import freeze_time

from py_css_styleguide.model import Manifest


@freeze_time("2012-10-15 10:00:00")
def test_manifest_to_dict():
    """
    Manifest.to_dict() should dump a dictionnary of references with its metas.
    """
    source = (
        ".styleguide-metas-references{\n"
        '    --names: "size ratio palette text_color";\n'
        "}\n"
        "\n"
        ".styleguide-reference-ratio{\n"
        '    --structure: "number";\n'
        '    --value: 42.123;\n'
        "}\n"
        "\n"
        ".styleguide-reference-size{\n"
        '    --structure: "number";\n'
        '    --value: 42;\n'
        "}\n"
        "\n"
        ".styleguide-reference-palette{\n"
        '    --structure: "flat";\n'
        '    --keys: "black white";\n'
        '    --values: "#000000 #ffffff";\n'
        "}\n"
        "\n"
        ".styleguide-reference-text_color{\n"
        '    --structure: "nested";\n'
        '    --keys: "black white";\n'
        '    --selectors: ".bg-black .bg-white";\n'
        '    --values: "#000000 #ffffff";\n'
        "}"
    )

    manifest = Manifest()
    manifest.load(source)

    dump = manifest.to_dict()

    expected = {
        "size": 42,
        "ratio": 42.123,
        "metas": {
            "compiler_support": "libsass",
            "references": ["size", "ratio", "palette", "text_color"],
            "created": "2012-10-15T10:00:00",
        },
        "palette": {"white": "#ffffff", "black": "#000000"},
        "text_color": {
            "black": {"selectors": ".bg-black", "values": "#000000"},
            "white": {"values": "#ffffff", "selectors": ".bg-white"},
        },
    }

    assert dump == expected


@freeze_time("2012-10-15 10:00:00")
def test_manifest_to_json():
    """
    Manifest.to_json() should dump a JSON of serialized dict from 'Manifest.to_dict()'
    """
    source = (
        ".styleguide-metas-references{\n"
        '    --names: "size ratio palette text_color";\n'
        "}\n"
        "\n"
        ".styleguide-reference-ratio{\n"
        '    --structure: "number";\n'
        '    --value: 42.123;\n'
        "}\n"
        "\n"
        ".styleguide-reference-size{\n"
        '    --structure: "number";\n'
        '    --value: 42;\n'
        "}\n"
        "\n"
        ".styleguide-reference-palette{\n"
        '    --structure: "flat";\n'
        '    --keys: "black white";\n'
        '    --values: "#000000 #ffffff";\n'
        "}\n"
        "\n"
        ".styleguide-reference-text_color{\n"
        '    --structure: "nested";\n'
        '    --keys: "black white";\n'
        '    --selectors: ".bg-black .bg-white";\n'
        '    --values: "#000000 #ffffff";\n'
        "}"
    )

    manifest = Manifest()
    manifest.load(source)

    dump = json.loads(manifest.to_json())

    expected = {
        "metas": {
            "compiler_support": "libsass",
            "references": ["size", "ratio", "palette", "text_color"],
            "created": "2012-10-15T10:00:00",
        },
        "palette": {"white": "#ffffff", "black": "#000000"},
        "ratio": 42.123,
        "size": 42,
        "text_color": {
            "black": {"selectors": ".bg-black", "values": "#000000"},
            "white": {"values": "#ffffff", "selectors": ".bg-white"},
        },
    }

    assert dump == expected
