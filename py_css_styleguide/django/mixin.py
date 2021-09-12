"""
Mixin
*****

"""
import json
import logging
import os

from django.contrib.staticfiles import finders

from ..model import Manifest


# Set the logger related to styleguide app
logger = logging.getLogger("py-css-styleguide")


class StyleguideMixin:
    """
    A mixin to return a manifest object.
    """
    def resolve_css_filepath(self, path):
        """
        Validate path or resolve static filepath if needed.

        Arguments:
            path (string): Either an absolute path or a relative path to an enabled
                static directory.

        Returns:
            string: Resolved path if success, else return None.
        """
        # Absolute path, just check it exists
        if os.path.isabs(path):
            if os.path.exists(path):
                return path
            return None
        else:
            resolved = finders.find(path)
            if resolved:
                return resolved
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

        Keyword Arguments:
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
            with open(resolved_path, "r") as fp:
                manifest.load(fp)

            # Save JSON manifest dump if required
            if save_dump and json_filepath:
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
        From given path, load JSON manifest dump.

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
        except FileNotFoundError:
            # Log details
            msg = (
                "Unable to find JSON manifest from: {}"
            )
            logger.warning(msg.format(path))
            manifest.loading_error = msg.format(path)

            manifest.status = "failed"
        except json.decoder.JSONDecodeError as e:
            # Log details
            msg = (
                "Invalid JSON manifest: {}"
            )
            logger.warning(msg.format(str(e)))
            manifest.loading_error = msg.format(str(e))

            manifest.status = "failed"
        else:
            # Load dump from manifest model object "from dict"
            manifest.from_dict(content)

        return manifest

    def get_manifest(self, css_filepath, json_filepath=None, save_dump=True,
                     development_mode=True):
        """
        Get and load manifest, either from CSS or JSON file depending options.

        Arguments:
            css_filepath (string): Path to CSS manifest file. Either an absolute path
                or a relative path to an enabled static directory.

        Keyword Arguments:
            json_filepath (string): Path to JSON manifest (to read or write).
            save_dump (boolean): To enable manifest JSON dump write. This can only works
                if CSS manifest has been correctly loaded and ``json_filepath`` has
                been given.
            development_mode (boolean): In development mode, CSS manifest is readed if
                it exists then a JSON dump may be written depending ``save_dump``.

        Returns:
            py_css_styleguide.model.Manifest: Manifest object.
        """
        # Init manifest with additional flags for loading status and possible error
        manifest = Manifest()
        # Default mode flag assume CSS is parsed
        manifest.status = "empty"
        # No error by default
        manifest.loading_error = None

        if development_mode:
            manifest = self.get_css_manifest(
                manifest,
                css_filepath,
                json_filepath=json_filepath,
                save_dump=save_dump,
            )

        if manifest.status in ["empty", "failed"] and json_filepath:
            manifest = self.get_json_manifest(manifest, json_filepath)

        return manifest
