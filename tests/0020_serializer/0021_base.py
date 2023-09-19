from collections import OrderedDict

import pytest

from py_css_styleguide.exceptions import (
    SerializerError,
    StyleguideValidationError,
    StyleguideUserWarning,
)
from py_css_styleguide.serializer import ManifestSerializer


def test_limit_evaluation_string_limit_truncation(recwarn):
    """
    The string evaluation limit should truncate string over the limit and emit a
    warning.
    """
    # String is not over the limit, no warning or truncation
    serializer = ManifestSerializer(evaluation_limit=3)
    data = serializer.limit_evaluation_string("refname", "foo")
    assert data == "foo"
    assert len(recwarn) == 0

    # String is over the limit, warning is emitted and string is truncated
    serializer = ManifestSerializer(evaluation_limit=5)
    with pytest.warns(StyleguideUserWarning):
        data = serializer.limit_evaluation_string("refname", "123456")
    assert data == "12345"


@pytest.mark.parametrize(
    "context,expected",
    [
        (
            {
                "styleguide-metas-references": {"names": "palette"},
                "styleguide-reference-foo": {"content": "bar"},
            },
            ["foo"],
        ),
        # Enforce the right item order to match returned list order
        (
            OrderedDict(
                (
                    ("styleguide-reference-foo", {"content": "bar"}),
                    ("styleguide-reference-pika", {"content": "chu"}),
                    ("dummy", {"names": "yip"}),
                    ("styleguide-reference-ping", {"content": "pong"}),
                )
            ),
            ["foo", "pika", "ping"],
        ),
    ],
)
def test_get_available_references(context, expected):
    serializer = ManifestSerializer()

    reference_names = serializer.get_available_references(context)

    assert reference_names == expected


@pytest.mark.parametrize(
    "context,expected",
    [
        # With a dummy ignored rule just for fun
        (
            {
                "styleguide-metas-references": {"names": "palette"},
                "dummy": {"names": "yip"},
            },
            ["palette"],
        ),
        # Every enabled rules are returned
        (
            {"styleguide-metas-references": {"names": "palette schemes foo bar"}},
            ["palette", "schemes", "foo", "bar"],
        ),
        # Automatically enable every references but no reference defined
        ({"styleguide-metas-references": {"auto": "true"}}, []),
        # Automatically enable every references and explicitely ignore some ones
        (
            OrderedDict(
                (
                    (
                        "styleguide-metas-references",
                        {"auto": "true", "excludes": "bar pong"},
                    ),
                    ("styleguide-reference-foo", {"content": "dummy"}),
                    ("styleguide-reference-bar", {"content": "dummy"}),
                    ("styleguide-reference-ping", {"content": "dummy"}),
                    ("styleguide-reference-pong", {"content": "dummy"}),
                )
            ),
            ["foo", "ping"],
        ),
    ],
)
def test_get_meta_reference_names_success(context, expected):
    serializer = ManifestSerializer()

    reference_names = serializer.get_meta_reference_names(context)

    assert reference_names == expected


@pytest.mark.parametrize(
    "context, expected",
    [
        # Missing references meta
        ({"styleguide-metas-foo": {"names": "palette"}}, SerializerError),
        # Missing names or auto property
        ({"styleguide-metas-references": {"content": "palette"}}, SerializerError),
        # Invalid name (from '-' character)
        (
            {"styleguide-metas-references": {"names": "foo-bar"}},
            StyleguideValidationError,
        ),
        # Empty list
        ({"styleguide-metas-references": {"names": ""}}, SerializerError),
    ],
)
def test_get_meta_reference_names_error(context, expected):
    serializer = ManifestSerializer()

    with pytest.raises(expected):
        serializer.get_meta_reference_names(context)
