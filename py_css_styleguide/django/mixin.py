import json
import logging
import os

from django.contrib.staticfiles import finders
from django.core.exceptions import SuspiciousFileOperation

from ..model import Manifest


# Set the logger related to styleguide app
logger = logging.getLogger("py-css-styleguide")


class StyleguideMixin:
    """
    Display styleguide from CSS manifest
    """
    def resolve_css_filepath(self, path):
        """
        Validate path or resolve static filepath if needed.

        path (string): Either an absolute path or a relative path to an enabled static
            directory.

        Returns:
            string: Resolved path if success, else return None.
        """
        print("🧪 resolve_css_filepath:path:", path)

        # Absolute path, just check it exists
        if os.path.isabs(path):
            print("  💫 is isabs")
            if os.path.exists(path):
                print("  💫 exists")
                return path

            print("  💫 does not exists")
            return None
        else:
            print("  💫 is relativepath")
            resolved = finders.find(path)
            if resolved:
                print("  💫 found")
                return resolved

            print("  💫 not found")
            return None

    def get_css_manifest(self, manifest, path, json_filepath=None, save_dump=False):
        """
        From given path, load CSS with manifest model and possibly save it if required.

        Arguments:
            manifest (py_css_styleguide.model.Manifest): Manifest model object to use
                to parse CSS manifest.
            path (string): Path to the CSS manifest. If this is a relative path, it is
                assumed it is a file inside static directory to resolve by Django
                static finder. Give a full absolute path if your file is out of the
                enabled static directories.

        Keywords Arguments:
            json_filepath (string): Absolute filepath for JSON dump destination. If
                empty, no dump will be created.
            save_dump (boolean): To enable manifest JSON dump write. This can only works
                if CSS manifest has been correctly loaded.

        Returns:
            py_css_styleguide.model.Manifest: The manifest object with loaded
                references.
        """
        # Update status flag
        manifest.status = "live"

        # Ensure the path exists or try to resolve path if needed
        resolved_path = self.resolve_css_filepath(path)

        if resolved_path:
            # Open and parse CSS
            with open(path, "r") as fp:
                print("🧪 Attempt to load CSS from:", path)
                manifest.load(fp)

            # Save JSON manifest dump if required
            if save_dump and json_filepath:
                print("🧪 Attempt to write JSON to:", json_filepath)
                with open(json_filepath, "w") as fp:
                    fp.write(manifest.to_json())
        else:
            # Log CSS load fail details
            manifest.status = "failed"
            msg = (
                "Unable to find CSS manifest from: {}"
            )
            logger.warning(msg.format(path))
            manifest.loading_error = msg.format(path)

        return manifest

    def get_json_manifest(self, manifest, path):
        """
        From given path, load JSON dump with manifest model.

        Arguments:
            manifest (py_css_styleguide.model.Manifest): Manifest model object to use
                to parse CSS manifest.
            path (string): Path to the CSS manifest.

        Returns:
            py_css_styleguide.model.Manifest: The manifest object with loaded
                references.
        """
        # Update status flag
        manifest.status = "dump"

        try:
            with open(path, "r") as fp:
                content = json.load(fp)
        # TODO: Add another exception for JSON error with another error message
        except FileNotFoundError:
            # Log details
            msg = (
                "Unable to find JSON manifest dump from: {}"
            )
            logger.warning(msg.format(path))

            manifest.status = "failed"
        else:
            # Load dump from manifest model object "from dict"
            manifest.from_dict(content)

        return manifest

    def get_manifest(self, css_filepath, json_filepath=None, save_dump=True,
                     development_mode=True):
        """
        TODO:
            A new better way to get and load manifest ?

        PRODUCTION/INTEGRATION:
            * Never CSS
            * Try for JSON
            * Never save JSON dump
            * Should never raise exceptions (output them to frontend)

        DEVELOPMENT
            * Always try for CSS first
            * May fallback to JSON
            * May not raise exceptions (output them to frontend)


        Arguments:
            css_filepath (string): Path to CSS manifest.

        Keyword Arguments:
            json_filepath (string): Path to JSON manifest (to read or write).
            save_dump (boolean): To enable manifest JSON dump write. This can only works
                if CSS manifest has been correctly loaded.
            development_mode (boolean): In development mode, the JSON dump is written
                when CSS manifest has been correctly loaded first and ``json_filepath``
                has been given.

        Returns:
            py_css_styleguide.model.Manifest: Manifest object.
        """
        print()
        print("🧐 CSS manifest path:", css_filepath)
        print("🧐 JSON manifest path:", json_filepath)

        # Init manifest with additional flags for loading status and possible error
        manifest = Manifest()
        # Default mode flag assume CSS is parsed
        manifest.status = "empty"
        # No error by default
        manifest.loading_error = None

        if development_mode:
            print("🧪 Assume to load CSS")
            manifest = self.get_css_manifest(
                manifest,
                css_filepath,
                json_filepath=json_filepath,
                save_dump=save_dump,
            )
            return manifest

        print("🧪 Assume to load JSON")

        return

    def load_manifest(self, path):
        """
        TODO:
            By default, try to get and parse the CSS manifest, if succeed and according
            to a settings it may dump the manifest object to a JSON file in templates
            directory, so the app part on production would be able to get it (opposed to
            actually where the app part dont have access to the static server and so the
            CSS to parse also).

            If not possible to reach the CSS (or directly depending from DEBUG) and an
            according setting is enable, fallback to read a "cached" JSON manifest.
        """
        print()
        print("🧐 CSS manifest path:", path)
        print("🧐 Save destination:", json_filepath)

        # TODO: Force invalid path to trigger save read
        path = "foo/bar.css"

        # Init manifest with additional flags for loading status and possible error
        manifest = Manifest()
        # Default mode flag assume CSS is parsed
        manifest.status = "empty"
        # No error by default
        manifest.loading_error = None

        # If CSS have been found, load it and parse it
        # TODO: On "settings.DEBUG = False" it should even not try to load CSS
        resolved_css_path = finders.find(path)
        if resolved_css_path:
            manifest = self.get_css_manifest(
                manifest,
                resolved_css_path,
                json_filepath=json_filepath
            )
        # Else use additional flag to expose error
        else:
            # Log CSS load fail details
            msg = (
                "Unable to find CSS manifest from: {}"
            )
            logger.warning(msg.format(path))

            # Load saved JSON manifest if any
            if json_filepath:
                manifest = self.get_json_manifest(manifest, json_filepath)

        # Add final error to output on front if everything has failed
        if manifest.status == "failed":
            msg = (
                "Unable to find any manifest (either CSS or JSON save)."
            )
            manifest.loading_error = msg

        print()

        return manifest
