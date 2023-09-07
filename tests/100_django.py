import logging
from pathlib import Path

import pytest

from freezegun import freeze_time

from py_css_styleguide.django.mixin import StyleguideMixin


def test_resolve_css_filepath_existing_relative_path(tests_settings):
    """
    Pointing a relative path and existing in static dirs returns the resolved absolute
    path.
    """
    manifest_css_filepath = "manifest_sample.css"

    mixin = StyleguideMixin()
    resolved_path = mixin.resolve_css_filepath(manifest_css_filepath)

    assert resolved_path == str(tests_settings.statics_path / manifest_css_filepath)


def test_resolve_css_filepath_unexisting_relative_path(tests_settings):
    """
    Pointing a relative path but not existing in static dirs returns None.
    """
    manifest_css_filepath = "nope.css"

    mixin = StyleguideMixin()
    resolved_path = mixin.resolve_css_filepath(manifest_css_filepath)

    assert resolved_path is None


def test_resolve_css_filepath_existing_absolute_path(tests_settings):
    """
    Pointing an existing absolute path returns the same path.
    """
    manifest_css_filepath = tests_settings.fixtures_path / "manifest_sample.css"

    mixin = StyleguideMixin()
    resolved_path = mixin.resolve_css_filepath(manifest_css_filepath)

    assert str(resolved_path) == str(manifest_css_filepath)


def test_resolve_css_filepath_unexisting_absolute_path(tests_settings):
    """
    Pointing a non existing absolute path returns None.
    """
    manifest_css_filepath = tests_settings.package_path / "nope.css"

    mixin = StyleguideMixin()
    resolved_path = mixin.resolve_css_filepath(manifest_css_filepath)

    assert resolved_path is None


@freeze_time("2012-10-15 10:00:00")
@pytest.mark.parametrize("css_filepath,kwargs,status,error,references,save_exists", [
    # CSS failing and no JSON available
    (
        "nope.css",
        {
            "json_filepath": None,
            "save_dump": False,
            "development_mode": True,
        },
        "failed",
        "Unable to find CSS manifest from: nope.css",
        None,
        None,
    ),
    # Both CSS and JSON are file not found
    (
        "nope.css",
        {
            "json_filepath": "nope.json",
            "save_dump": False,
            "development_mode": True,
        },
        "failed",
        "Unable to find JSON manifest from: {json_filepath}",
        None,
        None,
    ),
    # CSS failing and invalid JSON
    (
        "nope.css",
        {
            "json_filepath": "{FIXTURES}/manifest_invalid.json",
            "save_dump": False,
            "development_mode": True,
        },
        "failed",
        "Invalid JSON manifest: Expecting ',' delimiter: line 5 column 13 (char 75)",
        None,
        None,
    ),
    # CSS failing and fallback to JSON succeed
    (
        "nope.css",
        {
            "json_filepath": "{FIXTURES}/manifest_sample.json",
            "save_dump": True,
            "development_mode": True,
        },
        "dump",
        "Unable to find CSS manifest from: nope.css",
        ["palette", "text_color", "spaces"],
        True,
    ),
    # CSS failing then using existing JSON dump
    (
        "nope.css",
        {
            "json_filepath": "{FIXTURES}/manifest_sample.json",
            "save_dump": True,
            "development_mode": True,
        },
        "dump",
        "Unable to find CSS manifest from: nope.css",
        ["palette", "text_color", "spaces"],
        None,
    ),
    # CSS succeed with relative path to static dirs
    (
        "manifest_sample.css",
        {
            "json_filepath": "nope.json",
            "save_dump": False,
            "development_mode": True,
        },
        "live",
        None,
        ["palette", "text_color", "spaces"],
        False,
    ),
    # CSS succeed with absolute path then write dump
    (
        "{FIXTURES}/manifest_sample.css",
        {
            "json_filepath": "manifest_sample.json",
            "save_dump": True,
            "development_mode": True,
        },
        "live",
        None,
        ["palette", "text_color", "spaces"],
        True,
    ),
    # No development mode, directly try to read JSON
    (
        "{FIXTURES}/manifest_sample.css",
        {
            "json_filepath": "{FIXTURES}/manifest_sample.json",
            "save_dump": True,
            "development_mode": False,
        },
        "dump",
        None,
        ["palette", "text_color", "spaces"],
        True,
    ),
    # No development mode, both CSS and JSON failing
    (
        "nope.css",
        {
            "json_filepath": "nope.json",
            "save_dump": False,
            "development_mode": False,
        },
        "failed",
        "Unable to find JSON manifest from: {json_filepath}",
        None,
        False,
    ),
])
def test_mixin_get_manifest(caplog, tests_settings, tmp_path, css_filepath,
                            kwargs, status, error, references, save_exists):
    """
    "get_manifest" behaviors should be correct with given options.
    """
    caplog.set_level(logging.DEBUG, logger="py-css-styleguide")

    # Augment given path to absolute depending settings var
    css_filepath = tests_settings.format(css_filepath)

    if kwargs.get("json_filepath"):
        # Assume filepath is prefix with settings variable to format
        if kwargs["json_filepath"].startswith("{"):
            kwargs["json_filepath"] = Path(
                tests_settings.format(kwargs["json_filepath"])
            )
        # Else put JSON dump in temporary directory
        else:
            kwargs["json_filepath"] = tmp_path / kwargs["json_filepath"]

    # Error message is formatted with possible variables (since we cannot
    # always know full paths from parametrize)
    if error:
        error = tests_settings.format(error, extra={
            "css_filepath": css_filepath,
            "json_filepath": kwargs.get("json_filepath"),
        })

    # Use mixin to get and load manifest
    mixin = StyleguideMixin()
    manifest = mixin.get_manifest(
        css_filepath,
        **kwargs,
    )

    assert manifest.loading_error == error

    assert manifest.status == status

    assert manifest.metas.get("references") == references

    if save_exists is not None:
        assert kwargs["json_filepath"].exists() is save_exists
