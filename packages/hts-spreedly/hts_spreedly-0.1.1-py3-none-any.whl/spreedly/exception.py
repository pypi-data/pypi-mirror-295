from dataclasses import dataclass


class SpreedlyException(Exception):
    pass


@dataclass
class AuthException(SpreedlyException):
    errors: list
    response: dict


@dataclass
class UnknownException(SpreedlyException):
    response: dict
