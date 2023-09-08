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
