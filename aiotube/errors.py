class TooManyRequests(Exception):
    def __init__(self, message):
        self.message = message


class InvalidURL(Exception):
    def __init__(self, message):
        self.message = message


class AIOError(Exception):
    def __init__(self, message):
        self.message = message
