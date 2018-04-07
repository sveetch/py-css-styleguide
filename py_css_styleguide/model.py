"""
Model
=====

The model manifest contains structured datas of parsed and serialized
CSS manifest.

Each reference rule is stored in as object attribute and every metas rules are
stored in ``Manifest.metas`` attribute.

"""
import json

from py_css_styleguide.parser import TinycssSourceParser
from py_css_styleguide.serializer import ManifestSerializer


class Manifest(object):
    """
    Manifest model

    During load process, every rule is stored as object attribute so you can
    reach them directly.

    Attributes:
        _path (string): Possible filepath for source if it has been given or
            finded from source file-object.
        _datas (dict): Dictionnary of every rules returned by parser. This
            is not something you would need to reach commonly.
        _rule_attrs (list): List of registered reference rules. You may use
            it in iteration to find available reference attribute names.
        metas (dict): Dictionnary of every metas returned by serializer.
    """
    def __init__(self):
        self._path = None
        self._datas = None
        self._rule_attrs = []

        self.metas = {}

    def load(self, source, filepath=None):
        """
        Load source as manifest attributes

        Arguments:
            source (string or file-object): CSS source to parse and serialize
                to find metas and rules. It can be either a string or a
                file-like object (aka with a ``read()`` method which return
                string).

        Keyword Arguments:
            filepath (string): Optional filepath to memorize if source comes
                from a file. Default is ``None`` as if source comes from a
                string. If ``source`` argument is a file-like object, you
                should not need to bother of this argument since filepath will
                be filled from source ``name`` attribute.

        Returns:
            dict: Dictionnary of serialized rules.
        """
        # Set _path if source is a file-like object
        try:
            self._path = source.name
        except AttributeError:
            self._path = filepath

        # Get source content either it's a string or a file-like object
        try:
            source_content = source.read()
        except AttributeError:
            source_content = source

        # Parse and serialize given source
        parser = TinycssSourceParser()
        self._datas = parser.parse(source_content)

        serializer = ManifestSerializer()
        references = serializer.serialize(self._datas)

        # Copy serialized metas
        self.metas = serializer._metas

        # Set every enabled rule as object attribute
        for k, v in references.items():
            self.set_rule(k, v)

        return self._datas

    def set_rule(self, name, properties):
        """
        Set a rules as object attribute.

        Arguments:
            name (string): Rule name to set as attribute name.
            properties (dict): Dictionnary of properties.
        """
        self._rule_attrs.append(name)
        setattr(self, name, properties)

    def remove_rule(self, name):
        """
        Remove a rule from attributes.

        Arguments:
            name (string): Rule name to remove.
        """
        self._rule_attrs.remove(name)
        delattr(self, name)

    def to_json(self, indent=4):
        """
        Serialize metas and reference attributes to a JSON string.

        Keyword Arguments:
            indent (int): Space indentation, default to ``4``.

        Returns:
            string: JSON datas.
        """
        agregate = {
            'metas': self.metas,
        }

        agregate.update({k: getattr(self, k) for k in self._rule_attrs})

        return json.dumps(agregate, indent=indent)
