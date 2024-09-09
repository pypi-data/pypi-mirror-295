class SuperException(Exception):

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class KdbxFileNotFound(SuperException):
    pass


class KdbxFileCredentialsError(SuperException):
    pass


class KeyBoardLayoutException(SuperException):
    pass
