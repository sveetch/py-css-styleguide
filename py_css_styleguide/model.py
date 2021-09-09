"""
Model
=====

The model manifest contains structured datas of parsed and serialized
CSS manifest.

Each reference rule is stored in as object attribute and every metas rules are
stored in ``Manifest.metas`` attribute.

"""
import json

from .parser import TinycssSourceParser
from .serializer import ManifestSerializer
from .nomenclature import RULE_META


class Manifest(object):
    """
    Manifest model.

    During load process, every rule is stored as object attribute so you can
    reach them directly.

    Attributes:
        _path (string): Possible filepath for source if it has been given or
            finded from source file-object.
        _datas (dict): Dictionnary of every rules returned by parser. This
            is not something you would need to reach commonly.
        _rule_attrs (list): List of registered reference rules. You may use
            it in iteration to find available reference attribute names.
        metas (dict): Dictionnary of every meta datas from manifest. Either filled by
            serializer (with ``load`` method) or dump content (with ``from_dict``
            method).
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
            self._set_rule(k, v)

        return self._datas

    def _set_rule(self, name, properties):
        """
        Set a rules as object attribute.

        Arguments:
            name (string): Rule name to set as attribute name.
            properties (dict): Dictionnary of properties.
        """
        # Reference name to internal index
        if name not in self._rule_attrs:
            self._rule_attrs.append(name)

        # Set rule as object attribute
        setattr(self, name, properties)

    def _remove_rule(self, name):
        """
        Remove a rule from attributes.

        Arguments:
            name (string): Rule name to remove. The rule name must have been correctly
                registered through ``_set_rule``.
        """
        # Drop name from internal index
        self._rule_attrs.remove(name)

        # Drop attribute
        delattr(self, name)

    def to_dict(self):
        """
        Serialize metas and reference attributes to a dictionnary.

        Returns:
            dict: Data dictionnary.
        """
        agregate = {
            RULE_META: self.metas,
        }

        agregate.update({k: getattr(self, k) for k in self._rule_attrs})

        return agregate

    def to_json(self, indent=4):
        """
        Serialize metas and reference attributes to a JSON string.

        Keyword Arguments:
            indent (int): Space indentation, default to ``4``.

        Returns:
            string: JSON datas.
        """
        return json.dumps(self.to_dict(), indent=indent)

    def from_dict(self, data):
        """
        Load given data as manifest attributes.

        Alike ``load`` method this initialize the manifest object with references (and
        metas) but without to parse CSS, only from a dictionnary.

        Arguments:
            data (dict): A dictionnary of datas to load. This dictionnary have to be
                in the same format and structure than the one returned by ``to_dict``
                method.
        """
        self.metas = data[RULE_META]

        for name, properties in data.items():
            if name != RULE_META:
                self._set_rule(name, properties)
