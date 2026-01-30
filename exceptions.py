class NotFoundError(Exception):
    pass

class DuplictedError(Exception):
    pass

class DatabaseError(Exception):
    pass

class AmountTooSmallError(Exception):
    pass

class ErrorConversionType(Exception):
    pass

class AuthenticationException(Exception):
    pass