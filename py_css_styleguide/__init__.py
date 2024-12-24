"""CSS driven styleguide for your project"""
from importlib.metadata import version
from pathlib import Path


__pkgname__ = "py-css-styleguide"
__version__ = version(__pkgname__)

# Path location to the Sass mixin library file to use with a Dartsass compiler
COMPILER_DARTSASS_HELPER = (
    Path(__file__) / "scss" / "dartsass" / "_styleguide_helpers.scss"
)

# Path location to the Sass mixin library file to use with a Libsass compiler
COMPILER_LIBSASS_HELPER = (
    Path(__file__) / "scss" / "libsass" / "_styleguide_helpers.scss"
)
