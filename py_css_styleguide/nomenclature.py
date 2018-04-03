"""
Manifest nomenclature
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
    "flat",
)
