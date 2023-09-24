import logging

import pytest

from click.testing import CliRunner

from freezegun import freeze_time

from py_css_styleguide import __pkgname__
from py_css_styleguide.cli.entrypoint import cli_frontend


@freeze_time("2012-10-15 10:00:00")
def test_cli_parse_success(caplog, tmp_path, tests_settings):
    """
    With valid CSS manifest source, the parser command should succeed to write
    serialized manifest to JSON file at given destination path.
    """
    runner = CliRunner()

    source_filepath = tests_settings.fixtures_path / "manifest_sample.css"
    json_filepath = tests_settings.fixtures_path / "manifest_sample.json"
    destination_filepath = tmp_path / "manifest_sample.json"

    result = runner.invoke(
        cli_frontend,
        [
            "--verbose", "5",
            "parse",
            str(source_filepath),
            "--destination",
            str(destination_filepath),
        ]
    )

    assert result.exit_code == 0

    assert caplog.record_tuples == [
        (__pkgname__, logging.DEBUG, "Parsing: {}".format(source_filepath)),
    ]

    assert json_filepath.read_text() == destination_filepath.read_text()


@pytest.mark.parametrize(
    "source, expected",
    [
        (
            "wrong content",
            [
                (
                    __pkgname__,
                    logging.CRITICAL,
                    "Unable to parse CSS due to 1 parsing error(s)"
                ),
                (
                    __pkgname__,
                    logging.ERROR,
                    (
                        "Line 1 - Column 7 : [invalid] EOF reached before {} block "
                        "for a qualified rule."
                    )
                ),
            ],
        ),
        (
            ".foo {}",
            [
                (
                    __pkgname__,
                    logging.CRITICAL,
                    "Manifest lacks of '.styleguide-metas-references' or is empty"
                ),
            ],
        ),
        (
            (
                ".styleguide-metas-references {"
                "  --names: \"palette text_color spaces\";"
                "}"
            ),
            [
                (
                    __pkgname__,
                    logging.CRITICAL,
                    "Unable to find enabled reference 'palette'"
                ),
            ],
        ),
    ],
)
def test_cli_parse_error(caplog, tmp_path, tests_settings, source, expected):
    """
    Parser and serializer errors should be catched to be printed out with logging then
    program is properly aborted.
    """
    runner = CliRunner()

    source_filepath = tmp_path / "manifest_invalid.css"
    source_filepath.write_text(source)

    result = runner.invoke(
        cli_frontend,
        ["parse", str(source_filepath)]
    )

    assert result.exit_code == 1

    assert isinstance(result.exception, SystemExit) is True

    assert caplog.record_tuples == expected
