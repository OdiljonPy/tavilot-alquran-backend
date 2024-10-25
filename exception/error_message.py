from rest_framework import status
from enum import Enum


class ErrorCodes(Enum):
    INVALID_INPUT = 1
    NOT_FOUND = 2
    VALIDATION_FAILED = 3


error_messages = {
    1: {"result": "Invalid input provided", "http_status": status.HTTP_400_BAD_REQUEST},
    2: {"result": "Resource not found", "http_status": status.HTTP_404_NOT_FOUND},
    3: {"result": "Validate Error", "http_status": status.HTTP_400_BAD_REQUEST},
}


def get_error_message(code):
    return error_messages.get(code, 'Unknown error')