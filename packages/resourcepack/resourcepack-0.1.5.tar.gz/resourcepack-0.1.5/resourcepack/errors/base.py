class ValidFileError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class FileExtensionError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class DatabaseNameError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
