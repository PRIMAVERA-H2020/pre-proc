"""
exceptions.py

Custom exceptions for the pre-proc module
"""
__all__ = ['PreProcError', 'CannotLoadSourceFileError',
           'AttributeNotFoundError', 'AttributeConversionError',
           'AttributeEditError']


class PreProcError(Exception):
    """
    Base class for all custom exceptions
    """
    pass


class CannotLoadSourceFileError(PreProcError):
    """
    When a netCDF file can't be opened to find a required attribute.
    """
    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return 'Unable to load file {}'.format(self.filename)


class AttributeNotFoundError(PreProcError):
    """
    When the attribute that is due to be edited cannot be found in the
    input file.
    """
    def __init__(self, filename, attribute):
        self.filename = filename
        self.attribute = attribute

    def __str__(self):
        return 'Cannot find attribute {} in file {}'.format(self.attribute,
                                                            self.filename)


class AttributeConversionError(PreProcError):
    """
    When converting the attribute to the desired type fails.
    """
    def __init__(self, filename, attribute, new_type):
        self.filename = filename
        self.attribute = attribute
        self.new_type = new_type

    def __str__(self):
        return ('Cannot convert attribute {} to new type {} in file {}'.
                format(self.attribute, self.new_type, self.filename))


class AttributeEditError(PreProcError):
    """
    When converting the attribute to the desired type fails.
    """
    def __init__(self, filename, attribute, message):
        self.filename = filename
        self.attribute = attribute
        self.message = message

    def __str__(self):
        return ('Cannot edit attribute {} in file {}. {}'.
                format(self.attribute, self.filename, self.message))
