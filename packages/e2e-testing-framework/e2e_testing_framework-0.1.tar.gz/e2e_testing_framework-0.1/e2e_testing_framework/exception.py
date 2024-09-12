"""
    Module: exception
    Author: Neethukrishnan P
    
    Description:
    
    License:
    
    Created on: 08-17-2024
"""
from enum import Enum

from fastapi import HTTPException


class ErrorCodes(str, Enum):
    """class for error codes"""
    INVALID_STATUS_CODE = "INVALID_STATUS_CODE"
    INVALID_OUTPUT = "INVALID_OUTPUT"


class TestException(HTTPException):
    """Generic exception class for the project. Formats exceptions the way FastApi needs them to be."""

    def __init__(
            self, error_code: ErrorCodes, status_code: int = 422, detail=""
    ):
        """
        Constructor for the exception class
        :param error_code: Has to be an option from the enum
        :param status_code: HTTP Status code
        """
        self.error_code = error_code
        detail = [
            {
                "msg": (
                    f"{error_code.value}"
                    if not detail
                    else f"{error_code.value}. {detail}"
                ),
                "type": "test_exception_error.semantic",
            }
        ]
        super().__init__(status_code=status_code, detail=detail)