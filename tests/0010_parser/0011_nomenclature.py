import pytest

from py_css_styleguide.exceptions import StyleguideValidationError
from py_css_styleguide.nomenclature import (
    is_reserved_rule,
    is_reserved_property,
    is_valid_rule,
    is_valid_property,
)


@pytest.mark.parametrize(
    "name, expected",
    [("palette", False), ("load", True), ("to_dict", True), ("to_json", True)],
)
def test_nomenclature_is_reserved_rule(name, expected):
    assert is_reserved_rule(name) == expected


@pytest.mark.parametrize("name, expected", [("palette", False), ("structure", True)])
def test_nomenclature_is_reserved_property(name, expected):
    assert is_reserved_property(name) == expected


@pytest.mark.parametrize("name", ["palette", "foo_bar", "f123"])
def test_nomenclature_is_valid_rule_success(name):
    is_valid_rule(name)


@pytest.mark.parametrize(
    "name",
    ["", "_foo", "-foo", "foo-bar", "foo-bar", "foo bar", "1foo", "fooé", "load"],
)
def test_nomenclature_is_valid_rule_error(name):
    with pytest.raises(StyleguideValidationError):
        is_valid_rule(name)


@pytest.mark.parametrize("name", ["palette", "foo_bar", "f123"])
def test_nomenclature_is_valid_property_success(name):
    is_valid_property(name)


@pytest.mark.parametrize(
    "name",
    ["", "_foo", "-foo", "foo-bar", "foo-bar", "foo bar", "1foo", "fooé", "structure"],
)
def test_nomenclature_is_valid_property_error(name):
    with pytest.raises(StyleguideValidationError):
        is_valid_property(name)
