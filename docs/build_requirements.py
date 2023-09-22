"""
This requires ``Python>=3.8`` and ``packaging>=23.1``.
"""
from importlib.metadata import requires
from pathlib import Path

from packaging.requirements import Requirement


class RequirementBuilder:
    """
    Build requirements file content from requirements collected from a package
    metadata with support of extras (optional requirements).

    Package metadata format returned by importlib is not very simple to parse so this
    implementation is naive and won't support everything that could exists in Python
    packages:

    * It lacks of support for 'python_version' marker. Requirement defined with this
      will fail;
    * CVS url or local path for package won't be properly defined in requirement file
      with the right Pip option;

    Usage of importlib metadata is compatible with almost any package instead of the
    TOML way which is more efficient but only available with ``pyproject.toml``
    configuration.

    .. Hint::
        * Requirements file is the standard from Pip, commonly seen in a
          ``requirements.txt`` file;
        * Package metadata is the package configuration collected by setuptools during
          package installation. This collection comes from either ``setup.cfg``,
          ``setup.py`` or ``pyproject.toml`` depending from what package has used to
          define its configuration;
        * Extras requirements are optional requirements defined in package option
          ``options.extras_require``;

    Keyword Arguments:
        blocking (boolean): If False, any exception from parsing will not raise and
            instead print the error without blocking further script operations. If
            True, any exception from parsing are raised. Default to True.
    """
    def __init__(self, blocking=True):
        self.blocking = blocking

    def print_debug(self, source, r):
        """
        Just print Requirement item debug informations.

        Arguments:
            source (string): Requirement item as collected from ``import.metadata``.
            r (packaging.requirements.Requirement): ``Requirement`` object to get its
                informations.
        """
        print("-", source)
        print("  🎨 {name} - ver:{specifier} - [{extras}] - marker:{marker}".format(
            name=r.name,
            specifier=r.specifier,
            extras=r.extras,
            marker=r.marker
        ))
        print("   🚀 name:", r.name)
        print("   🚀 specifier:", r.specifier)

    def parse_metadata_requirements(self, pkgname):
        """
        Parse package requirement from importlib metadata on a package.

        Arguments:
            pkgname (string): The package name to inspect its requirements defined
                from its metadata. Obviously the package must be installed in your
                environment.

        Returns:
            dict: A dictionnary of package requirements gathered by their extras name.
                For requirement unrelated to any extras, they will be stored in ``None``
                item.
        """
        requirements = requires(pkgname)

        store = {}
        extra_pattern = "extra == "
        # python_version_pattern = "python_version == " # Unused for now

        # Parse all requirement to dress a map index on extra
        for item in requirements:
            extra_rule = None

            # Parse requirement item
            r = Requirement(item)

            # Normalize version specifier if any
            specifier = str(r.specifier) if r.specifier else ""

            # As tested with packaging==23.1, extras is always an empty set and extra
            # name is located instead in 'marker'
            if list(r.extras):
                print(self.print_debug(item, r))
                msg = (
                    "Item '{name}' extras is not empty, this is "
                    "unexpected: {extras_set}"
                )
                raise NotImplementedError(
                    msg.format(name=r.name, extras_set=list(r.extras))
                )
            elif r.marker and " and " in str(r.marker):
                print(self.print_debug(item, r))
                msg = (
                    "Item '{name}' have unimplemented marker content: {marker}"
                )
                raise NotImplementedError(
                    msg.format(name=r.name, marker=r.marker)
                )
            elif r.marker and not str(r.marker).startswith(extra_pattern):
                print(self.print_debug(item, r))
                msg = (
                    "Item '{name}' have unimplemented marker content: {marker}"
                )
                raise NotImplementedError(
                    msg.format(name=r.name, marker=r.marker)
                )

            # Normalize extra name if any
            if r.marker:
                extra_rule = str(r.marker)[len(extra_pattern):]
                # Remove quotes around name
                if extra_rule.startswith("'") or extra_rule.startswith('"'):
                    extra_rule = extra_rule[1:-1].strip()

            if extra_rule not in store:
                store[extra_rule] = []

            store[extra_rule].append((r.name, specifier))

        return store

    def create_requirements_file(self, requirements, extras, destination=None):
        """
        Create requirements file content and possibly file.

        If a same requirement name (version specifier is ignored) exists in multiple
        extras, only the first occurence is listed.

        Arguments:
            requirements (dict): Dict of requirements as returned from
                ``parse_metadata_requirements``.
            extras (string or list): List of extras names to select requirements.
                Use ``None`` value as name to get non optional requirements.
                Instead of list, you can just give the string name ``all`` which will
                collect every requirements, both non optional and optional requirements.

        Keyword Arguments:
            destination (pathlib.Path): File path where to write requirement file if
                given.

        Returns:
            string: Requirement file content.
        """
        lines = []
        collected = set()

        if extras == "all":
            extras = [None] + list(requirements.keys())

        for extra in extras:
            if extra in requirements:
                # Search in extra section
                for item in requirements[extra]:
                    # Don't collect twice the same requirement depending its name.
                    if item[0] not in collected:
                        lines.append("".join(item))
                        collected.add(item[0])

        content = "\n".join(lines)

        if destination:
            destination.write_text(content)

        return content

    def get_requirements(self, pkgname, extras, destination=None):
        """
        Shortand to inspect, return requirements file content and possibly write it
        on filesystem.

        Arguments:
            pkgname (string): The package name to inspect its requirements defined
                from its metadata. Obviously the package must be installed in your
                environment.
            extras (string or list): List of extras names to select requirements.
                Use ``None`` value as name to get non optional requirements.
                Instead of list, you can just give the string name ``all`` which will
                collect every requirements, both non optional and optional requirements.

        Keyword Arguments:
            destination (pathlib.Path): File path where to write requirement file if
                given.

        Returns:
            string: Requirement file content if there was no parsing error else it
            will return None.
        """
        try:
            pkg_requirements = self.parse_metadata_requirements(pkgname)
        except NotImplementedError as e:
            if not self.blocking:
                created = None
                print(e)
            else:
                raise e
        else:
            created = self.create_requirements_file(
                pkg_requirements,
                extras=extras,
                destination=destination,
            )

        return created


if __name__ == "__main__":
    builder = RequirementBuilder()
    destination = Path("./docs/requirements.txt")
    content = builder.get_requirements(
        "py-css-styleguide",
        ["doc", "django"],
        destination=destination,
    )
