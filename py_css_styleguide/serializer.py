"""
Serializer
==========

"""
import json

from collections import OrderedDict

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
        SerializerError: When there is an invalid syntax in datas.

    Attributes:
        _metas (collections.OrderedDict): Buffer to store serialized metas
            from parsed source. Default is an empty dict which reseted and
            filled from ``serialize`` method.
        _DEFAULT_SPLITTER (string): Default value splitter used for some
            structure kinds.
    """
    _DEFAULT_SPLITTER = 'white-space'

    def __init__(self):
        self._metas = OrderedDict()

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
            msg = "Rule name '{}' must starts with a letter"
            raise SerializerError(msg.format(name))

        for item in name:
            if item not in RULE_ALLOWED_CHARS:
                msg = ("Invalid rule name '{}': it must only contains "
                       "letters, numbers and '_' character")
                raise SerializerError(msg.format(name))

        return True

    def validate_variable_name(self, name):
        """
        Validate variable name.

        Arguments:
            name (string): Property name.

        Returns:
            bool: ``True`` if variable name is valid.
        """
        if not name:
            raise SerializerError("Variable name is empty".format(name))

        if name[0] not in PROPERTY_ALLOWED_START:
            msg = "Variable name '{}' must starts with a letter"
            raise SerializerError(msg.format(name))

        for item in name:
            if item not in PROPERTY_ALLOWED_CHARS:
                msg = ("Invalid variable name '{}': it must only contains "
                       "letters, numbers and '_' character")
                raise SerializerError(msg.format(name))

        return True

    def value_splitter(self, reference, prop, value, mode):
        """
        Split a string into a list items.

        Default behavior is to split on white spaces.


        Arguments:
            reference (string): Reference name used when raising possible
                error.
            prop (string): Property name used when raising possible error.
            value (string): Property value to split.
            mode (string): Splitter mode. Default should come from
                ``ManifestSerializer._DEFAULT_SPLITTER``.

                Available splitter are:

                * ``white-space``: Simply split a string on white spaces;
                * ``json-list``: Assume the string is a JSON list to parse;

        Returns:
            list:
        """
        items = []

        if mode == 'json-list':
            try:
                items = json.loads(value)
            except json.JSONDecodeError as e:
                print(value)
                msg = ("Reference '{ref}' raised JSON decoder error when "
                       "splitting values from '{prop}': {err}'")
                raise SerializerError(msg.format(ref=reference, prop=prop,
                                                 err=e))
        else:
            if len(value) > 0:
                items = value.split(" ")

        return items

    def serialize_to_json(self, name, datas):
        """
        Serialize given datas to any object from assumed JSON string.

        Arguments:
            name (string): Name only used inside possible exception message.
            datas (dict): Datas to serialize.

        Returns:
            object: Object depending from JSON content.
        """
        data_object = datas.get('object', None)

        if data_object is None:
            msg = ("JSON reference '{}' lacks of required 'object' variable")
            raise SerializerError(msg.format(name))

        try:
            content = json.loads(data_object, object_pairs_hook=OrderedDict)
        except json.JSONDecodeError as e:
            msg = "JSON reference '{}' raised error from JSON decoder: {}"
            raise SerializerError(msg.format(name, e))
        else:
            return content

    def serialize_to_nested(self, name, datas):
        """
        Serialize given datas to a nested structure where each key create an
        item and each other variable is stored as a subitem with corresponding
        value (according to key index position).

        Arguments:
            name (string): Name only used inside possible exception message.
            datas (dict): Datas to serialize.

        Returns:
            dict: Nested dictionnary of serialized reference datas.
       """
        keys = datas.get('keys', None)
        splitter = datas.get('splitter', self._DEFAULT_SPLITTER)

        if not keys:
            msg = ("Nested reference '{}' lacks of required 'keys' variable "
                   "or is empty")
            raise SerializerError(msg.format(name))
        else:
            keys = self.value_splitter(name, 'keys', keys, mode=splitter)

        # Initialize context dict with reference keys
        context = OrderedDict()
        for k in keys:
            context[k] = OrderedDict()

        # Tidy each variable value to its respective item
        for k, v in datas.items():
            # Ignore reserved internal keywords
            if k not in ('keys', 'structure', 'splitter'):
                values = self.value_splitter(name, 'values', v, mode=splitter)

                if len(values) != len(keys):
                    msg = ("Nested reference '{}' has different length for "
                           "values of '{}' and 'keys'")
                    raise SerializerError(msg.format(name, k))

                # Put each value to its respective key using position index.
                for i, item in enumerate(values):
                    ref = keys[i]
                    context[ref][k] = item

        return context

    def serialize_to_flat(self, name, datas):
        """
        Serialize given datas to a flat structure ``KEY:VALUE`` where ``KEY``
        comes from ``keys`` variable and ``VALUE`` comes from ``values``
        variable.

        This means both ``keys`` and ``values`` are required variable to be
        correctly filled (each one is a string of item separated with an empty
        space). Both resulting list must be the same length.

        Arguments:
            name (string): Name only used inside possible exception message.
            datas (dict): Datas to serialize.

        Returns:
            dict: Flat dictionnay of serialized reference datas.
        """
        keys = datas.get('keys', None)
        values = datas.get('values', None)
        splitter = datas.get('splitter', self._DEFAULT_SPLITTER)

        if not keys:
            msg = ("Flat reference '{}' lacks of required 'keys' variable or "
                   "is empty")
            raise SerializerError(msg.format(name))
        else:
            keys = self.value_splitter(name, 'keys', keys, mode=splitter)

        if not values:
            msg = ("Flat reference '{}' lacks of required 'values' variable "
                   "or is empty")
            raise SerializerError(msg.format(name))
        else:
            values = self.value_splitter(name, 'values', values, mode=splitter)

        if len(values) != len(keys):
            msg = ("Flat reference have different length of 'keys' ands "
                   "'values' variable")
            raise SerializerError(msg.format(name))

        return OrderedDict(zip(keys, values))

    def serialize_to_list(self, name, datas):
        """
        Serialize given datas to a list structure.

        List structure is very simple and only require a variable ``--items``
        which is a string of values separated with an empty space. Every other
        properties are ignored.

        Arguments:
            name (string): Name only used inside possible exception message.
            datas (dict): Datas to serialize.

        Returns:
            list: List of serialized reference datas.
        """
        items = datas.get('items', None)
        splitter = datas.get('splitter', self._DEFAULT_SPLITTER)

        if items is None:
            msg = ("List reference '{}' lacks of required 'items' variable "
                   "or is empty")
            raise SerializerError(msg.format(name))
        else:
            items = self.value_splitter(name, 'items', items, mode=splitter)

        return items

    def serialize_to_string(self, name, datas):
        """
        Serialize given datas to a string.

        Simply return the value from required variable``value``.

        Arguments:
            name (string): Name only used inside possible exception message.
            datas (dict): Datas to serialize.

        Returns:
            string: Value.
        """
        value = datas.get('value', None)

        if value is None:
            msg = ("String reference '{}' lacks of required 'value' variable "
                   "or is empty")
            raise SerializerError(msg.format(name))

        return value

    def get_meta_references(self, datas):
        """
        Get manifest enabled references declaration

        This required declaration is readed from
        ``styleguide-metas-references`` rule that require either a ``--names``
        or ``--auto`` variable, each one define the mode to enable reference:

        Manually
            Using ``--names`` which define a list of names to enable, every
            other non enabled rule will be ignored.

            Section name (and so Reference name also) must not contains special
            character nor ``-`` so they still be valid variable name for almost
            any languages. For word separator inside name, use ``_``.
        Automatic
            Using ``--auto`` variable every reference rules will be enabled.
            The value of this variable is not important since it is not empty.

        If both of these variables are defined, the manual enable mode is used.

        Arguments:
            datas (dict): Data where to search for meta references declaration.
                This is commonly the fully parsed manifest.

        Returns:
            list: A list of reference names.
        """
        rule = datas.get(RULE_META_REFERENCES, {})

        if not rule:
            msg = "Manifest lacks of '.{}' or is empty"
            raise SerializerError(msg.format(RULE_META_REFERENCES))
        else:
            if rule.get('names', None):
                names = rule.get('names').split(" ")
            elif rule.get('auto', None):
                names = self.get_available_references(datas)
            else:
                msg = ("'.{}' either require '--names' or '--auto' variable "
                       "to be defined")
                raise SerializerError(msg.format(RULE_META_REFERENCES))

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

        A reference can contains variable ``--structure`` setted to ``"flat"``,
        ``"list"`` or ``"string"`` to define serialization structure.

        Arguments:
            datas (dict): Data where to search for reference declaration. This
                is commonly the fully parsed manifest.
            name (string): Reference name to get and serialize.

        Returns:
            collections.OrderedDict: Serialized reference datas.
        """
        rule_name = '-'.join((RULE_REFERENCE, name))
        structure_mode = 'nested'

        if rule_name not in datas:
            msg = "Unable to find enabled reference '{}'"
            raise SerializerError(msg.format(name))

        properties = datas.get(rule_name)

        # Search for "structure" variable
        if 'structure' in properties:
            if properties['structure'] == 'flat':
                structure_mode = 'flat'
            elif properties['structure'] == 'list':
                structure_mode = 'list'
            elif properties['structure'] == 'string':
                structure_mode = 'string'
            elif properties['structure'] == 'json':
                structure_mode = 'json'
            elif properties['structure'] == 'nested':
                pass
            else:
                msg = "Invalid structure mode name '{}' for reference '{}'"
                raise SerializerError(msg.format(structure_mode, name))
            del properties['structure']

        # Validate variable names
        for item in properties.keys():
            self.validate_variable_name(item)

        # Perform serialize according to structure mode
        if structure_mode == 'flat':
            context = self.serialize_to_flat(name, properties)
        elif structure_mode == 'list':
            context = self.serialize_to_list(name, properties)
        elif structure_mode == 'string':
            context = self.serialize_to_string(name, properties)
        elif structure_mode == 'nested':
            context = self.serialize_to_nested(name, properties)
        elif structure_mode == 'json':
            context = self.serialize_to_json(name, properties)

        return context

    def get_available_references(self, datas):
        """
        Get available manifest reference names.

        Every rules starting with prefix from ``nomenclature.RULE_REFERENCE``
        are available references.

        Only name validation is performed on these references.

        Arguments:
            datas (dict): Data where to search for reference declarations.

        Returns:
            list: List of every available reference names. This is the real
                name unprefixed.
        """
        names = []

        for k, v in datas.items():
            if k.startswith(RULE_REFERENCE):
                names.append(k[len(RULE_REFERENCE)+1:])

        return names

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
            collections.OrderedDict: Serialized enabled references datas.
        """
        references = OrderedDict()

        for section in meta_references:
            references[section] = self.get_reference(datas, section)

        return references

    def serialize(self, datas):
        """
        Serialize datas to manifest structure with metas and references.

        Only references are returned, metas are assigned to attribute
        ``ManifestSerializer._metas``.

        Arguments:
            datas (dict): Data where to search for reference declarations. This
                is commonly the fully parsed manifest.

        Returns:
            collections.OrderedDict: Serialized enabled references datas.
        """
        self._metas = OrderedDict({
            'references': self.get_meta_references(datas),
        })

        return self.get_enabled_references(datas, self._metas['references'])
