import json

from freezegun import freeze_time

from py_css_styleguide.model import Manifest


def test_manifest_load_string():
    """
    Manifest.load() should load correctly manifest from given string of a CSS
    manifest.
    """
    source = (
        ".styleguide-metas-references{\n"
        '    --names: "palette text_color";\n'
        "}\n"
        "\n"
        ".styleguide-reference-palette{\n"
        '    --structure: "flat";\n'
        '    --keys: "black white";\n'
        '    --values: "#000000 #ffffff";\n'
        "}\n"
        "\n"
        ".styleguide-reference-text_color{\n"
        '    --keys: "black white";\n'
        '    --selectors: ".bg-black .bg-white";\n'
        '    --values: "#000000 #ffffff";\n'
        "}"
    )

    manifest = Manifest()
    manifest.load(source)

    assert manifest._path is None

    assert sorted(manifest.metas.get("references")) == sorted(["palette", "text_color"])

    assert manifest.palette == {"white": "#ffffff", "black": "#000000"}

    assert manifest.text_color == {
        "black": {"selectors": ".bg-black", "values": "#000000"},
        "white": {"values": "#ffffff", "selectors": ".bg-white"},
    }


def test_manifest_load_fileobject(tests_settings):
    """
    Manifest.load() should load correctly manifest from given fileobject of a CSS
    manifest file.
    """
    source_filepath = tests_settings.fixtures_path / "manifest_sample.css"

    manifest = Manifest()

    with source_filepath.open() as fp:
        manifest.load(fp)

    assert manifest._path == str(source_filepath)

    assert sorted(manifest.metas.get("references")) == sorted(
        ["palette", "text_color", "spaces"]
    )

    assert manifest.palette == {"white": "#ffffff", "black": "#000000"}

    assert manifest.spaces == ["tiny", "short", "normal", "large", "wide"]

    assert manifest.text_color == {
        "black": {"selectors": ".bg-black", "values": "#000000"},
        "white": {"values": "#ffffff", "selectors": ".bg-white"},
    }


@freeze_time("2012-10-15 10:00:00")
def test_manifest_to_dict():
    """
    Manifest.to_dict() should dump a dictionnary of references with its metas.
    """
    source = (
        ".styleguide-metas-references{\n"
        '    --names: "palette text_color";\n'
        "}\n"
        "\n"
        ".styleguide-reference-palette{\n"
        '    --structure: "flat";\n'
        '    --keys: "black white";\n'
        '    --values: "#000000 #ffffff";\n'
        "}\n"
        "\n"
        ".styleguide-reference-text_color{\n"
        '    --keys: "black white";\n'
        '    --selectors: ".bg-black .bg-white";\n'
        '    --values: "#000000 #ffffff";\n'
        "}"
    )

    manifest = Manifest()
    manifest.load(source)

    dump = manifest.to_dict()

    expected = {
        "metas": {
            "compiler_support": "libsass",
            "references": ["palette", "text_color"],
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
        '    --names: "palette text_color";\n'
        "}\n"
        "\n"
        ".styleguide-reference-palette{\n"
        '    --structure: "flat";\n'
        '    --keys: "black white";\n'
        '    --values: "#000000 #ffffff";\n'
        "}\n"
        "\n"
        ".styleguide-reference-text_color{\n"
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
            "references": ["palette", "text_color"],
            "created": "2012-10-15T10:00:00",
        },
        "palette": {"white": "#ffffff", "black": "#000000"},
        "text_color": {
            "black": {"selectors": ".bg-black", "values": "#000000"},
            "white": {"values": "#ffffff", "selectors": ".bg-white"},
        },
    }

    assert dump == expected


def test_manifest_from_dict():
    """
    Manifest.from_dict() should receive a dict of datas to load as manifest object
    attributes correctly.
    """
    source = {
        "metas": {
            "references": ["palette", "text_color"],
            "created": "2012-10-15T10:00:00",
        },
        "palette": {"white": "#ffffff", "black": "#000000"},
        "text_color": {
            "black": {"selectors": ".bg-black", "values": "#000000"},
            "white": {"values": "#ffffff", "selectors": ".bg-white"},
        },
    }

    manifest = Manifest()
    manifest.from_dict(source)

    assert manifest.metas["references"] == ["palette", "text_color"]

    assert manifest.palette["white"] == "#ffffff"

    assert manifest.text_color["black"] == {
        "selectors": ".bg-black",
        "values": "#000000",
    }

    assert manifest.to_dict() == source
