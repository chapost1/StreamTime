from typing import Optional, Dict

class AppError(Exception):
    __slots__ = (
        'details'
    )

    def __init__(self, message: str='', details: Optional[Dict] = None):         
        super().__init__(message)
        self.details = details


class NotFoundError(AppError):
    """Request entity is not found"""

class InputError(AppError):
    """Caller input is not valid"""

class UnauthorizedError(AppError):
    """Caller is not authenticated, while authentication is required to access the requested resource"""

class AccessDeniedError(AppError):
    """Caller is may be authenticated but yet missing privileges to access the requested resource"""
