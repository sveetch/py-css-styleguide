"""
Serializer
==========

"""
import ast
import datetime
import json

from collections import OrderedDict
from warnings import warn

from .nomenclature import (
    RULE_META_REFERENCES,
    RULE_META_COMPILER,
    RULE_REFERENCE,
    REFERENCE_STRUCTURES,
    is_valid_rule,
    is_valid_property,
)

from .exceptions import SerializerError, StyleguideUserWarning


class ManifestSerializer(object):
    """
    Serialize parsed CSS to data suitable to Manifest.

    Raises:
        SerializerError: When there is an invalid syntax in parsed manifest.

    Keyword Arguments:
        compiler_support (string): Sass compiler name to assume when it has not been
            defined in meta references. Default to
            ``ManifestSerializer._DEFAULT_COMPILER_SUPPORT``.
        evaluation_limit (int): A limit of string character length for
            evaluation to avoid possibly Python crash with very large string to evaluate
            with ``ast.literal_eval`` (see Python documentation for detail). Default to
            ``ManifestSerializer._DEFAULT_EVALUATION_LIMIT``.

    Attributes:
        _metas (collections.OrderedDict): Buffer to store serialized metas
            from parsed source.
        _DEFAULT_SPLITTER (string): Default value splitter used for some
            structure kinds.
        _DEFAULT_COMPILER_SUPPORT (string): Default Sass compiler name.
        _DEFAULT_EVALUATION_LIMIT (int): Default limit of string character length for
            evaluation. It has been set to 1000 characters which should be a
            reasonnable large limit in our context.
    """

    _DEFAULT_SPLITTER = "white-space"
    _DEFAULT_COMPILER_SUPPORT = "libsass"
    _DEFAULT_EVALUATION_LIMIT = 1000

    def __init__(self, compiler_support=None, evaluation_limit=None):
        self.compiler_support = compiler_support or self._DEFAULT_COMPILER_SUPPORT
        self.evaluation_limit = evaluation_limit or self._DEFAULT_EVALUATION_LIMIT

        self._metas = OrderedDict({"compiler_support": self.compiler_support})

    def get_ref_varname(self, name):
        """
        Shortcut to format a reference name to a reference selector name.

        Internally we pass a reference name (like `bar`) to methods which was parsed in
        manifest from a CSS selector name (like ``.styleguide-foo-bar``) but for some
        messages we need to display CSS selector name again.

        Arguments:
            name (string): A reference name.

        Returns:
            string: CSS selector name.
        """
        return "-".join((RULE_REFERENCE, name))

    def value_splitter(self, name, prop, value, mode):
        """
        Split a string into a list items.

        Behavior depend on argument ``mode``, either a simple split on white spaces or
        an evaluation for a list syntax.

        Arguments:
            name (string): Reference name used when raising possible
                error.
            prop (string): Property name used when raising possible error.
            value (string): Property value to split.
            mode (string): Splitter mode. Default should come from
                ``ManifestSerializer._DEFAULT_SPLITTER``.

                Available splitter are:

                * ``white-space``: Simply split a string on white spaces;
                * ``object-list``: Assume the string is a list object to parse;
                * ``json-list``: Old name for object-list, deprecated;

        Returns:
            list: List of values parsed from given original JSON list.
        """
        items = []
        # NOTE: Maybe we should emits a StyleguideUserWarning if "compiler_support" has
        # not been set, but not exclusively from this method, it is something to put up
        # level
        compiler_support = self._metas.get("compiler_support", self.compiler_support)

        if mode == "object-list" or mode == "json-list":
            if mode == "json-list":
                message = (
                    "Reference '{ref}' use deprecated '--splitter: \"json-list\";', "
                    "change it to '--splitter: \"object-list\";' instead."
                )
                warn(
                    message.format(ref=self.get_ref_varname(name)),
                    StyleguideUserWarning,
                )

            if compiler_support == "dartsass":
                try:
                    items = ast.literal_eval(value[: self.evaluation_limit])
                except SyntaxError as e:
                    msg = (
                        "Reference '{ref}' raised a syntax error when "
                        "splitting values from '{prop}': {err}'"
                    )
                    raise SerializerError(
                        msg.format(ref=self.get_ref_varname(name), prop=prop, err=e)
                    )
            else:
                try:
                    items = json.loads(value)
                except json.JSONDecodeError as e:
                    msg = (
                        "Reference '{ref}' raised JSON decoder error when "
                        "splitting values from '{prop}': {err}'"
                    )
                    raise SerializerError(
                        msg.format(ref=self.get_ref_varname(name), prop=prop, err=e)
                    )
        else:
            if len(value) > 0:
                items = value.split(" ")

        return items

    def limit_evaluation_string(self, name, value):
        """
        Truncate given string value to the string evaluation length limit.

        If ``ManifestSerializer.evaluation_limit`` is 0 or None, no limit will be
        applied.

        Arguments:
            name (string): Reference name only used in possible warning message.
            value (string): String value to limit if needed

        Returns:
            string: Truncated string if needed depending
            ``ManifestSerializer.evaluation_limit`` value.
        """
        if not self.evaluation_limit:
            return value

        # If string is over the limit, emit a warning.
        if len(value) > self.evaluation_limit:
            message = (
                "Reference '{ref}' has a string value length that is over the "
                "evaluation limit ({limit}). It has been truncated and may leads to "
                "errors or unexpected results. Either you upgrade the limit or ensure "
                "your string values keeps below the limit."
            )
            warn(
                message.format(
                    ref=self.get_ref_varname(name), limit=self.evaluation_limit
                ),
                StyleguideUserWarning,
            )

        return value[: self.evaluation_limit]

    def serialize_to_complex(self, name, datas):
        """
        Serialize given datas to any object from assumed JSON string.

        Arguments:
            name (string): Name only used inside possible exception message.
            datas (dict): Datas to serialize.

        Returns:
            object: Object depending from content.
        """
        data_object = datas.get("object", None)
        compiler_support = self._metas.get("compiler_support", self.compiler_support)

        if data_object is None:
            msg = "JSON reference '{refname}' lacks of required 'object' variable"
            raise SerializerError(msg.format(refname=self.get_ref_varname(name)))

        if compiler_support == "dartsass":
            try:
                content = ast.literal_eval(data_object[: self.evaluation_limit])
            except SyntaxError as e:
                msg = (
                    "Reference '{ref}' raised a syntax error when "
                    "parsing values '{values}': {err}'"
                )
                raise SerializerError(
                    msg.format(
                        ref=self.get_ref_varname(name), values=data_object, err=e
                    )
                )
            else:
                return content
        else:
            try:
                content = json.loads(data_object, object_pairs_hook=OrderedDict)
            except json.JSONDecodeError as e:
                msg = "JSON reference '{refname}' raised error from JSON decoder: {err}"
                raise SerializerError(
                    msg.format(refname=self.get_ref_varname(name), err=e)
                )
            else:
                return content

    def serialize_to_json(self, name, datas):
        """
        Shortcut around ``ManifestSerializer.serialize_to_complex()`` to maintain
        support for deprecated structure name ``json`` and emit a deprecation warning.

        Arguments:
            name (string): Name only used inside possible exception message.
            datas (dict): Datas to serialize.

        Returns:
            object: Object depending from content.
        """
        message = (
            "Reference '{ref}' use deprecated '--structure: \"json\";', change it to "
            "'--structure: \"object-complex\";' instead."
        )
        warn(message.format(ref=self.get_ref_varname(name)), StyleguideUserWarning)
        return self.serialize_to_complex(name, datas)

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
        keys = datas.get("keys", None)
        splitter = datas.get("splitter", self._DEFAULT_SPLITTER)

        if not keys:
            msg = (
                "Nested reference '{}' lacks of required 'keys' variable " "or is empty"
            )
            raise SerializerError(msg.format(name))
        else:
            keys = self.value_splitter(name, "keys", keys, mode=splitter)

        # Initialize context dict with reference keys
        context = OrderedDict()
        for k in keys:
            context[k] = OrderedDict()

        # Tidy each variable value to its respective item
        for k, v in datas.items():
            # Ignore reserved internal keywords
            if k not in ("keys", "structure", "splitter"):
                values = self.value_splitter(name, "values", v, mode=splitter)

                if len(values) != len(keys):
                    msg = (
                        "Nested reference '{}' has different length for "
                        "values of '{}' and 'keys'"
                    )
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
        keys = datas.get("keys", None)
        values = datas.get("values", None)
        splitter = datas.get("splitter", self._DEFAULT_SPLITTER)

        if not keys:
            msg = "Flat reference '{}' lacks of required 'keys' variable or " "is empty"
            raise SerializerError(msg.format(name))
        else:
            keys = self.value_splitter(name, "keys", keys, mode=splitter)

        if not values:
            msg = (
                "Flat reference '{}' lacks of required 'values' variable " "or is empty"
            )
            raise SerializerError(msg.format(name))
        else:
            values = self.value_splitter(name, "values", values, mode=splitter)

        if len(values) != len(keys):
            msg = (
                "Flat reference have different length of 'keys' ands "
                "'values' variable"
            )
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
        items = datas.get("items", None)
        splitter = datas.get("splitter", self._DEFAULT_SPLITTER)

        if items is None:
            msg = (
                "List reference '{}' lacks of required 'items' variable " "or is empty"
            )
            raise SerializerError(msg.format(name))
        else:
            items = self.value_splitter(name, "items", items, mode=splitter)

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
        value = datas.get("value", None)

        if value is None:
            msg = (
                "String reference '{}' lacks of required 'value' variable "
                "or is empty"
            )
            raise SerializerError(msg.format(name))

        return value

    def get_meta_compiler(self, datas):
        """
        Get enabled compiler declarations.
        """
        rule = datas.get(RULE_META_COMPILER, {})

        if rule and rule.get("support", None):
            return rule.get("support")

        return self.compiler_support

    def get_meta_reference_names(self, datas):
        """
        Get enabled reference declarations.

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
            The value of this variable is not important as long as it is not empty.

            In this mode, another variable is watched for, it is ``excludes`` which is a
            list of reference names to ignore.

        If both of these variables are defined, only the manual enable mode "--names" is
        used.

        Arguments:
            datas (dict): Data where to search for meta references declaration.
                This is commonly the fully parsed manifest.

        Returns:
            list: A list of reference names.
        """
        rule = datas.get(RULE_META_REFERENCES, {})

        # There is no meta reference rule
        if not rule:
            msg = "Manifest lacks of '.{}' or is empty"
            raise SerializerError(msg.format(RULE_META_REFERENCES))
        else:
            # For explicitely allowed reference names
            if rule.get("names", None):
                names = rule.get("names").split(" ")
            # For automatic reference names storing
            elif rule.get("auto", None):
                names = self.get_available_references(datas)
                # Filter out references explicitely named in possible "excludes"
                # property.
                if rule.get("excludes", None):
                    excludes = rule.get("excludes").split(" ")
                    names = [item for item in names if item not in excludes]
            # Meta reference rule lacks of required properties
            else:
                msg = (
                    "'.{}' either require '--names' or '--auto' variable "
                    "to be defined"
                )
                raise SerializerError(msg.format(RULE_META_REFERENCES))

        for item in names:
            is_valid_rule(item)

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
        rule_name = self.get_ref_varname(name)

        if rule_name not in datas:
            msg = "Unable to find enabled reference '{}'"
            raise SerializerError(msg.format(name))

        properties = datas.get(rule_name)

        # Search for "structure" variable
        if "structure" in properties:
            if properties["structure"] in REFERENCE_STRUCTURES:
                structure_mode = properties["structure"]
            else:
                msg = "Invalid structure mode name '{}' for reference '{}'"
                raise SerializerError(msg.format(properties["structure"], name))
            # Clean structure from props so it does not trigger validation
            del properties["structure"]
        else:
            msg = "Structure variable '--structure' is missing from reference '{}'"
            raise SerializerError(msg.format(rule_name))

        # Validate variable names
        for item in properties.keys():
            is_valid_property(item)

        # Perform serialize according to structure mode
        if structure_mode == "flat":
            context = self.serialize_to_flat(name, properties)
        elif structure_mode == "list":
            context = self.serialize_to_list(name, properties)
        elif structure_mode == "string":
            context = self.serialize_to_string(name, properties)
        elif structure_mode == "nested":
            context = self.serialize_to_nested(name, properties)
        elif structure_mode == "json":
            context = self.serialize_to_json(name, properties)
        elif structure_mode == "object-complex":
            context = self.serialize_to_complex(name, properties)
        else:
            msg = "Unexpected error for reference '{}': '{}'"
            raise SerializerError(msg.format(name, properties))

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
                names.append(k[len(RULE_REFERENCE) + 1 :])

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
                "compiler_support": self.get_meta_compiler(datas),
                "references": self.get_meta_reference_names(datas),
                "created": datetime.datetime.now().isoformat(timespec="seconds"),
        })

        return self.get_enabled_references(datas, self._metas["references"])
