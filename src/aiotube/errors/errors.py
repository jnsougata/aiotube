class TooManyRequests(Exception):
    """
    Raised when the user has sent too many requests to the API.
    """
    def __init__(self, message):
        self.message = message


class InvalidURL(Exception):
    """
    Raised when the URL is invalid.
    """
    def __init__(self, message):
        self.message = message


class BadURL(Exception):
    """
    Raised when the URL format is invalid.
    """
    def __init__(self, message):
        self.message = message


class AIOError(Exception):
    """
    Raised when the response is not what we expected.
    """
    def __init__(self, message):
        self.message = message
