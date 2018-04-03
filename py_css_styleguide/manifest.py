from py_css_styleguide.parser import TinycssSourceParser
from py_css_styleguide.serializer import ManifestSerializer


class Manifest(object):
    """
    Manifest model

    During load process, every rule is stored as object attribute so you can
    reach them directly.

    Attributes:
        _path (string): Possible filepath for source if it has been given.
        _datas (dict): Dictionnary of every rules returned by serializer. This
            is not something you would need to reach commonly.
        metas (dict): Dictionnary of every metas returned by serializer.
    """
    def __init__(self):
        self._path = None
        self._datas = None

        self.metas = {}

    def load(self, source, filepath=None):
        """
        Set a rules as object attribute.

        Args:
            source (string): CSS source to parse and serialize to find metas
                and rules.

        Keyword Arguments:
            filepath (string): Optional filepath to memorize if source comes
                from a file. Default is ``None`` as if source comes from a
                string.

        Returns:
            dict: Dictionnary of serialized rules.
        """
        self._path = filepath

        # Parse and serialize given source
        parser = TinycssSourceParser()
        self._datas = parser.parse(source)

        serializer = ManifestSerializer()
        references = serializer.serialize(self._datas)

        # Copy serialized metas
        self.metas = serializer._metas

        # Set every enabled rule as object attribute
        for k,v in references.items():
            self.set_rule(k, v)

        return self._datas

    def set_rule(self, name, properties):
        """
        Set a rules as object attribute.

        Args:
            name (string): Rule name to set as attribute name.
            properties (dict): Dictionnary of properties.
        """
        setattr(self, name, properties)
