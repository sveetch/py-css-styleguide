"""
Exceptions
==========

Specific application exceptions.
"""


class PyCssStyleguideException(Exception):
    """
    Exception base.

    You should never use it directly except for test purpose. Instead make or
    use a dedicated exception related to the error context.
    """

    pass


class ParserErrors(PyCssStyleguideException):
    """
    Exception to raise when there is errors when parsing a manifest.

    Attribute ``error_payload`` contains a dict of runned command details.

    Keyword Arguments:
        error_payload (dict): A dictionnary of command response error details. It
            won't output as exception message from traceback, you need to exploit it
            yourself if needed.
    """
    def __init__(self, *args, **kwargs):
        self.error_payload = kwargs.pop("error_payload", None)
        super().__init__(*args, **kwargs)


class SerializerError(PyCssStyleguideException):
    """
    Exception to raise when there is a syntax issue during serialization.
    """

    pass


class StyleguideValidationError(PyCssStyleguideException):
    """
    Exception to raise when there is invalid naming in reference rules and properties.
    """

    pass


class StyleguideDeprecationWarning(DeprecationWarning):
    """
    A deprecation warning explicitely named after application to distinct it from
    DeprecationWarning.
    """

    pass


class StyleguideUserWarning(UserWarning):
    """
    An usage warning explicitely named after application to distinct it from
    UserWarning.
    """

    pass
