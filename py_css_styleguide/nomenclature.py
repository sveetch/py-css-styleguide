"""
Nomenclature
============

* A rule name starts with a prefix from ``RULE_BASE_PREFIX``;
* Rule prefix is followed from its type that can be either:

  * ``RULE_META``;
  * ``reference``;

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

RULE_BASE_PREFIX = "styleguide"

RULE_META = "metas"

RULE_META_REFERENCES = "-".join((RULE_BASE_PREFIX, RULE_META, 'references'))

RULE_REFERENCE = "-".join((RULE_BASE_PREFIX, 'reference'))

RULE_ALLOWED_START = ascii_letters
RULE_ALLOWED_CHARS = ascii_letters + digits + '_'

PROPERTY_ALLOWED_START = ascii_letters
PROPERTY_ALLOWED_CHARS = ascii_letters + digits + '_'

# Not validated, just here for mention
RESERVED_RULE_NAMES = (
    "styleguide",
    "load",
    "metas",
    "everythingstartingwith_",
)

# Not validated, just here for mention
RESERVED_PROPERTY_NAMES = (
    "structure",
)
