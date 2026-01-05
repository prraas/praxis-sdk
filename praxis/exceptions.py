class PraxisError(Exception):
    """
    Base exception for Praxis SDK.
    All SDK errors inherit from this.
    """
    pass


class APIError(PraxisError):
    """
    Network / protocol / unexpected API failure.
    """
    pass


class ValidationError(PraxisError):
    """
    Input validation failed on server.
    """
    pass


class PaymentError(PraxisError):
    """
    Payment / credits related failure.
    """
    pass


class ExecutionError(PraxisError):
    """
    Server-side execution failure.
    """
    pass
