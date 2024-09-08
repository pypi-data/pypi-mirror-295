class PodScanException(Exception):
    """Base exception for PodScan API errors."""

    pass


class AuthenticationError(PodScanException):
    """Raised when there's an authentication error."""

    pass


class APIError(PodScanException):
    """Raised when the API returns an error."""

    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class ValidationError(PodScanException):
    """Raised when there's a validation error in the request."""

    pass


class RateLimitError(PodScanException):
    """Raised when the rate limit is exceeded."""

    pass
