"""
Serializer
==========

"""
from py_css_styleguide.nomenclature import (
    RULE_META_REFERENCES,
    RULE_REFERENCE,
    RULE_ALLOWED_START,
    RULE_ALLOWED_CHARS,
    PROPERTY_ALLOWED_START,
    PROPERTY_ALLOWED_CHARS,
)


class SerializerError(Exception):
    """
    Exception to raise when there is a syntax issue during serialization.
    """
    pass


class ManifestSerializer(object):
    """
    Serialize parsed CSS to data suitable to Manifest

    Raises:
        SerializerError: When there is invalid syntax in datas.

    Attributes:
        _metas (dict): Buffer to store serialized metas from parsed source.
            Default is an empty dict which reseted and filled from
            ``serialize`` method.
    """
    def __init__(self):
        self._metas = {}

    def validate_rule_name(self, name):
        """
        Validate rule name.

        Arguments:
            name (string): Rule name.

        Returns:
            bool: ``True`` if rule name is valid.
        """
        if not name:
            raise SerializerError("Rule name is empty".format(name))

        if name[0] not in RULE_ALLOWED_START:
            raise SerializerError("Rule name '{}' must starts with a letter".format(name))

        for item in name:
            if item not in RULE_ALLOWED_CHARS:
                raise SerializerError("Invalid rule name '{}': it must only contains letters, numbers and '_' character".format(name))

        return True

    def validate_property_name(self, name):
        """
        Validate property name.

        Arguments:
            name (string): Property name.

        Returns:
            bool: ``True`` if property name is valid.
        """
        if not name:
            raise SerializerError("Property name is empty".format(name))

        if name[0] not in PROPERTY_ALLOWED_START:
            raise SerializerError("Property name '{}' must starts with a letter".format(name))

        for item in name:
            if item not in PROPERTY_ALLOWED_CHARS:
                raise SerializerError("Invalid property name '{}': it must only contains letters, numbers and '_' character".format(name))

        return True

    def format_value(self, data, name, default="list"):
        """
        Format value following its format declaration if given.

        Format declaration is defined using ``--NAME-format`` where ``NAME``
        is the name related property to format value.

        Actually supported format are:

        * string;
        * list where each element is separated by an empty space;

        ``list`` is allways the default format.

        Value is not getted from a safe get, if it does not exist it raises an
        exception.

        It is assumed that asked value is allways a string.

        Arguments:
            data (dict): Data where to search for property value and optional
                format definition.
            name (string): Property name to search for. Will also be joined to
                ``-format`` to search for format declaration.

        Keyword arguments:
            default (string): Default format to use when not defined for
                search property.

        Returns:
            Variable type following triggered format. Can be either a string
            or a list.
        """
        format_kind = data.get('{}-format'.format(name), default)

        value = data.get(name, None)
        if value is None:
            raise SerializerError("Asked value for item '{}' does not exist".format(name))

        if not format_kind:
            format_kind = default

        if format_kind not in ('string', 'list'):
            raise SerializerError("Format declaration '{}' for '{}' is not supported".format(name, format_kind))

        if format_kind == 'string':
            return value

        return value.split(" ")

    def serialize_to_nested(self, name, datas):
        """
        Serialize given datas to a nested structure where each key create an
        item and each other property is stored as a subitem with corresponding
        value (according to key index position).

        Arguments:
            name (string): Name only used inside possible exception message.
            datas (dict): Datas to serialize.

        Returns:
            dict: Serialized reference datas.
       """
        keys = datas.get('keys', None)

        if not keys:
            raise SerializerError("Item '{}' lacks of required 'keys' property".format(name))
        else:
            keys = keys.split(" ")

        # Initialize context dict with reference keys
        context = {k:{} for k in keys}

        # Tidy each property value to its respective reference
        for k,v in datas.items():
            # Ignore reserved internal keywords
            if k not in ('keys', 'flat'):
                values = v.split(" ")

                if len(values) != len(keys):
                    raise SerializerError("Length of '{}' property values for item '{}' is different from keys length".format(k, name))

                # Put each value to its respective key using position index.
                for i, item in enumerate(values):
                    ref = keys[i]
                    context[ref][k] = item

        return context

    def serialize_to_flat(self, name, datas):
        """
        Serialize given datas to a flat structure KEY:VALUE where ``KEY``
        comes from ``keys`` property and ``VALUE`` comes from ``values``
        property.

        This means both ``keys`` and ``values`` are required property to be
        correctly filled (each one is a string of item separated with an empty
        space). Both resulting list must be the same length.

        Arguments:
            name (string): Name only used inside possible exception message.
            datas (dict): Datas to serialize.

        Returns:
            dict: Serialized reference datas.
        """
        context = {}

        keys = datas.get('keys', None)
        values = datas.get('values', None)

        if not keys:
            raise SerializerError("Item '{}' lacks of required 'keys' property".format(name))
        else:
            keys = keys.split(" ")

        if not values:
            raise SerializerError("Item '{}' lacks of required 'values' property".format(name))
        else:
            values = values.split(" ")

        if len(values) != len(keys):
            raise SerializerError("Length of keys ands values for item '{}' are differents".format(name))

        return dict(zip(keys, values))

    def get_meta_references(self, datas):
        """
        Get manifest enabled references declaration

        This required declaration is readed from
        ``styleguide-metas-references`` rule that require a ``--names``
        property. Format kind should not be defined since attempted value is
        allways a list.

        Section name (and so Reference name also) must no contains special
        character nor ``-`` so they still be valid variable name for almost
        any languages. For word separator inside name, use ``_``.

        Arguments:
            datas (dict): Data where to search for meta references declaration.
                This is commonly the fully parsed manifest.

        Returns:
            list: A list of reference names.
        """
        rule = datas.get(RULE_META_REFERENCES, {})

        if not rule:
            raise SerializerError("Manifest lacks of '.{}' or is empty".format(RULE_META_REFERENCES))
        elif not rule.get('names', None):
            raise SerializerError("'.{}' lacks of '--names' variable or is empty".format(RULE_META_REFERENCES))

        names = self.format_value(rule, 'names')

        for item in names:
            self.validate_rule_name(item)

        return names

    def get_reference(self, datas, name):
        """
        Get serialized reference datas

        Because every reference is turned to a dict (that stands on ``keys``
        variable that is a list of key names), every variables must have the
        same exact length of word than the key name list.

        A reference name starts with 'styleguide-reference-' followed by
        name for reference.

        A reference can contains property ``flat`` setted to ``"true"`` (as a
        string since there is no boolean in CSS) to indicate reference must be
        serialized a simple pair keys/values.

        Arguments:
            datas (dict): Data where to search for reference declaration. This
                is commonly the fully parsed manifest.
            name (string): Reference name to get and serialize.

        Returns:
            dict: Serialized reference datas.
        """
        rule_name = '-'.join((RULE_REFERENCE, name))
        flat_mode = False
        context = {}

        if rule_name not in datas:
            raise SerializerError("Unable to find enabled reference '{}'".format(name))

        properties = datas.get(rule_name)

        # Search for "flat" flag
        if 'flat' in properties:
            if properties['flat'].lower() == 'true':
                flat_mode = True
            del properties['flat']

        # Validate property names
        for item in properties.keys():
            self.validate_property_name(item)

        # Perform serialize nested(default)/flat
        if flat_mode:
            context = self.serialize_to_flat(name, properties)
        else:
            context = self.serialize_to_nested(name, properties)

        return context

    def get_enabled_references(self, datas, meta_references):
        """
        Get enabled manifest references declarations.

        Enabled references are defined through meta references declaration,
        every other references are ignored.

        Arguments:
            datas (dict): Data where to search for reference declarations.
                This is commonly the fully parsed manifest.
            meta_references (list): List of enabled reference names.

        Returns:
            dict: Serialized enabled references datas.
        """
        references = {}

        for section in meta_references:
            references[section] = self.get_reference(datas, section)

        return references

    def serialize(self, datas):
        """
        Serialize datas to manifest structure

        Arguments:
            datas (dict): Data where to search for reference declarations. This
                is commonly the fully parsed manifest.
        """
        self._metas = {
            'references': self.get_meta_references(datas),
        }

        return self.get_enabled_references(datas, self._metas['references'])
