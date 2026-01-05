# robostream/exceptions.py

class RoboStreamError(Exception):
    """
    Base exception for RoboStream SDK.
    All SDK errors inherit from this.
    """
    pass


class APIError(RoboStreamError):
    """
    Network / protocol / unexpected API failure.
    """
    pass


class ValidationError(RoboStreamError):
    """
    Input validation failed on server.
    """
    pass


class PaymentError(RoboStreamError):
    """
    Payment / credits related failure.
    """
    pass


class ExecutionError(RoboStreamError):
    """
    Server-side execution failure.
    """
    pass
