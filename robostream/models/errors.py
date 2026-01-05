# robostream/models/errors.py

class ModelError(Exception):
    """
    Base error for model / response parsing issues.
    """
    pass


class InvalidEnvelopeError(ModelError):
    """
    Raised when backend response does not match
    expected envelope schema.
    """
    pass
