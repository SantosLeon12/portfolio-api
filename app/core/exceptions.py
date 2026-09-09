class InvalidCredentialsError(Exception):
    pass


class InactiveAdminError(Exception):
    pass


class ResourceNotFoundError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ResourceConflictError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ResourceInUseError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class DomainValidationError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)