# -*- coding: utf-8 -*-
import logging
import os
import pytest

from py_css_styleguide.django.mixin import StyleguideMixin


def test_resolve_css_filepath_existing_relative_path(tests_settings):
    """
    Pointing a relative path and existing in static dirs returns the resolved absolute
    path.
    """
    manifest_css_filepath = "manifest_sample.css"

    mixin = StyleguideMixin()
    resolved_path = mixin.resolve_css_filepath(manifest_css_filepath)

    assert resolved_path == os.path.join(
        tests_settings.statics_path,
        manifest_css_filepath,
    )


def test_resolve_css_filepath_unexisting_relative_path(tests_settings):
    """
    Pointing a relative path but not existing in static dirs returns None.
    """
    manifest_css_filepath = "nope.css"

    mixin = StyleguideMixin()
    resolved_path = mixin.resolve_css_filepath(manifest_css_filepath)

    assert resolved_path == None


def test_resolve_css_filepath_existing_absolute_path(tests_settings):
    """
    Pointing an existing absolute path returns the same path.
    """
    manifest_css_filepath = os.path.join(
        tests_settings.fixtures_path, "manifest_sample.css"
    )

    mixin = StyleguideMixin()
    resolved_path = mixin.resolve_css_filepath(manifest_css_filepath)

    assert resolved_path == manifest_css_filepath


def test_resolve_css_filepath_unexisting_absolute_path(tests_settings):
    """
    Pointing a non existing absolute path returns None.
    """
    manifest_css_filepath = os.path.join(
        tests_settings.package_path, "nope.css"
    )

    mixin = StyleguideMixin()
    resolved_path = mixin.resolve_css_filepath(manifest_css_filepath)

    assert resolved_path == None


def test_mixin_dev_css_fail():
    """
    Mixin in development mode and is unable to find CSS file, should turn in "failed"
    status and have an error message stored.
    """
    manifest_css_filepath = "nope.css"
    manifest_json_filepath = "nope.json"

    mixin = StyleguideMixin()
    manifest = mixin.get_manifest(
        manifest_css_filepath,
        manifest_json_filepath,
        save_dump=False,
        development_mode=True,
    )

    assert manifest.loading_error == "Unable to find CSS manifest from: nope.css"
    assert manifest.status == "failed"


def test_mixin_dev_css_succeed(caplog, tests_settings, temp_builds_dir):
    """
    Mixin in development mode and is able to find CSS file, it should write to JSON
    dump, turn to "live" status and no error message stored.
    """
    caplog.set_level(logging.DEBUG, logger="py-css-styleguide")

    # Create test temporary directory where to save JSON dump
    basedir = temp_builds_dir.join("mixin_dev_css_succeed").strpath
    os.makedirs(basedir)

    manifest_css_filepath = os.path.join(
        tests_settings.fixtures_path, "manifest_sample.css"
    )

    manifest_json_filepath = os.path.join(
        basedir, "manifest_sample.json"
    )

    mixin = StyleguideMixin()
    manifest = mixin.get_manifest(
        manifest_css_filepath,
        manifest_json_filepath,
        save_dump=True,
        development_mode=True,
    )

    print(caplog.record_tuples)

    assert manifest.loading_error == None

    assert manifest.status == "live"

    assert os.path.exists(manifest_json_filepath) == True
