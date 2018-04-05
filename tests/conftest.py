"""
Some fixture methods
"""
import os
import pytest

import py_css_styleguide


class FixturesSettingsTestMixin(object):
    """Mixin containing some basic settings"""
    def __init__(self):
        # Base fixture datas directory
        self.tests_dir = 'tests'
        self.tests_path = os.path.normpath(
            os.path.join(
                os.path.abspath(os.path.dirname(py_css_styleguide.__file__)),
                '..',
                self.tests_dir,
            )
        )
        self.fixtures_dir = 'data_fixtures'
        self.fixtures_path = os.path.join(
            self.tests_path,
            self.fixtures_dir
        )


@pytest.fixture(scope="module")
def fixtures_settings():
    """Initialize and return settings (mostly paths) for fixtures (scope at module level)"""
    return FixturesSettingsTestMixin()
