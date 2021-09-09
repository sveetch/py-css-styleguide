"""
Nomenclature
============

This is the nomenclature about manifest references names (rules and properties).

* A rule name starts with a prefix from ``RULE_BASE_PREFIX``;
* Rule prefix is followed from its type that can be either:

  * The ``RULE_META`` value;
  * ``reference`` string;

* Then rule name ends with its component name;
* Rule name parts are separated with ``-``.

There is a limited set of allowed characters:

* For rule component name they are registred in ``RULE_ALLOWED_CHARS``;
* For rule property name they are registred in ``PROPERTY_ALLOWED_CHARS``;

There is some reserved name:

* For rule component name they are registred in ``RESERVED_RULE_NAMES``;
* For rule property name they are registred in ``RESERVED_PROPERTY_NAMES``;

"""
from string import ascii_letters, digits

from .exceptions import StyleguideValidationError


RULE_BASE_PREFIX = "styleguide"

RULE_META = "metas"

RULE_META_REFERENCES = "-".join((RULE_BASE_PREFIX, RULE_META, "references"))

RULE_REFERENCE = "-".join((RULE_BASE_PREFIX, "reference"))

RULE_ALLOWED_START = ascii_letters
RULE_ALLOWED_CHARS = ascii_letters + digits + "_"

PROPERTY_ALLOWED_START = ascii_letters
PROPERTY_ALLOWED_CHARS = ascii_letters + digits + "_"

FORBIDDEN_PREFIXES = (
    "_",
    "-",
)
"""
Rule and property names can not start with following strings
"""

RESERVED_RULE_NAMES = (
    "styleguide",
    "load",
    "to_dict",
    "to_json",
    "from_dict",
    "metas",
)
"""
Rule name can not be one of the following string
"""

RESERVED_PROPERTY_NAMES = (
    "structure",
)
"""
Property (variable) name can not be one of the following string
"""


def is_reserved_rule(name):
    """
    Validate name against ``RESERVED_RULE_NAMES``.

    Arguments:
        name (string): Rule name.

    Returns:
        bool: ``True`` if name match a reserved name.
    """
    return (name in RESERVED_RULE_NAMES)


def is_reserved_property(name):
    """
    Validate name against ``RESERVED_PROPERTY_NAMES``.

    Arguments:
        name (string): Property name.

    Returns:
        bool: ``True`` if name match a reserved name.
    """
    return (name in RESERVED_PROPERTY_NAMES)


def is_valid_rule(name):
    """
    Validate rule name.

    Arguments:
        name (string): Rule name.

    Returns:
        bool: ``True`` if rule name is valid.
    """
    if not name:
        raise StyleguideValidationError("Rule name is empty")

    if is_reserved_rule(name):
        msg = "Rule name '{}' is reserved, you can not use it for a rule"
        raise StyleguideValidationError(msg.format(name))

    if name.startswith(FORBIDDEN_PREFIXES):
        msg = "Rule name '{}' cannot starts with special characters"
        raise StyleguideValidationError(msg.format(name))

    if name[0] not in RULE_ALLOWED_START:
        msg = "Rule name '{}' must starts with a letter"
        raise StyleguideValidationError(msg.format(name))

    for item in name:
        if item not in RULE_ALLOWED_CHARS:
            msg = (
                "Invalid rule name '{}': it must only contains "
                "letters, numbers and '_' character"
            )
            raise StyleguideValidationError(msg.format(name))

    return True


def is_valid_property(name):
    """
    Validate property name.

    Arguments:
        name (string): Property name.

    Returns:
        bool: ``True`` if variable name is valid.
    """
    if not name:
        raise StyleguideValidationError("Variable name is empty")

    if is_reserved_property(name):
        msg = "Variable name '{}' is reserved, you can not use it for a variable"
        raise StyleguideValidationError(msg.format(name))

    if name.startswith(FORBIDDEN_PREFIXES):
        msg = "Variable name '{}' cannot starts with special characters"
        raise StyleguideValidationError(msg.format(name))

    if name[0] not in PROPERTY_ALLOWED_START:
        msg = "Variable name '{}' must starts with a letter"
        raise StyleguideValidationError(msg.format(name))

    for item in name:
        if item not in PROPERTY_ALLOWED_CHARS:
            msg = (
                "Invalid variable name '{}': it must only contains "
                "letters, numbers and '_' character"
            )
            raise StyleguideValidationError(msg.format(name))

    return True
