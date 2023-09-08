from pathlib import Path

import pytest

import py_css_styleguide


class ApplicationTestSettings:
    """
    Object to store settings related to application. This is almost about useful
    paths which may be used in tests. This is not related to Django settings.

    Attributes:
        application_path (str): Absolute path to the application directory.
        package_path (str): Absolute path to the package directory.
        tests_dir (str): Directory name which include tests.
        tests_path (str): Absolute path to the tests directory.
        sandbox_dir (str): Directory name of project sandbox.
        sandbox_path (str): Absolute path to the project sandbox directory.
        statics_dir (str): Directory name of sandbox static directory.
        statics_path (str): Absolute path to the sandbox static directory.
        fixtures_dir (str): Directory name which include tests datas.
        fixtures_path (str): Absolute path to the tests datas.
    """

    def __init__(self):
        self.application_path = Path(py_css_styleguide.__file__).parents[0].resolve()

        self.package_path = self.application_path.parent

        self.tests_dir = "tests"
        self.tests_path = self.package_path / self.tests_dir

        self.fixtures_dir = "data_fixtures"
        self.fixtures_path = self.tests_path / self.fixtures_dir

        self.sandbox_dir = "sandbox"
        self.sandbox_path = self.package_path / self.sandbox_dir

        self.statics_dir = "static"
        self.statics_path = self.sandbox_path / self.statics_dir

    def format(self, content, extra={}):
        """
        Format given string to include some values related to this application.

        Arguments:
            content (str): Content string to format with possible values.

        Returns:
            str: Given string formatted with possible values.
        """
        variables = {
            "HOMEDIR": Path.home(),
            "PACKAGE": str(self.package_path),
            "APPLICATION": str(self.application_path),
            "TESTS": str(self.tests_path),
            "FIXTURES": str(self.fixtures_path),
            "SANDBOX": str(self.sandbox_path),
            "STATICS": str(self.statics_path),
            "VERSION": py_css_styleguide.__version__,
        }
        if extra:
            variables.update(extra)

        return content.format(**variables)


@pytest.fixture(scope="function")
def temp_builds_dir(tmp_path):
    """
    Prepare a temporary build directory.

    NOTE: You should use directly the "tmp_path" fixture in your tests.
    """
    return tmp_path


@pytest.fixture(scope="module")
def tests_settings():
    """
    Initialize and return settings for tests.

    Example:
        You may use it like: ::

            def test_foo(settings):
                print(settings.package_path)
                print(settings.format("Application version: {VERSION}"))
    """
    return ApplicationTestSettings()
