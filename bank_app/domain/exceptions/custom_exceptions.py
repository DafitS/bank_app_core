from .base import DomainError


class NotFoundError(DomainError):
    pass


class DuplicatedError(DomainError):
    pass


class DatabaseError(DomainError):
    pass


class AmountTooSmallError(DomainError):
    pass


class ErrorConversionType(DomainError):
    pass


class AuthenticationException(DomainError):
    pass