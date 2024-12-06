from enum import Enum

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import ValidationError


class PaymeErrorCodes(Enum):
    INVALID_AMOUNT = -31001
    USER_NOT_FOUND = -31099
    TRANSACTION_EXISTS = -31050
    # TRANSACTION_INVALID = -31003
    SYSTEM_ERROR = -32400
    TRANSACTION_NOT_FOUND = -31003
    UNABLE_CANCEL = -31007
    OPERATION_CANNOT_PERFORMED = -31008
    ERROR_REQUEST = -32300
    INSUFFICIENT_METHOD = -32504


error_messages = {
    -31001: {"result": "Subscription price sent incorrectly", "http_status": status.HTTP_200_OK},
    -31099: {"result": "User not found", "http_status": status.HTTP_200_OK},
    -31050: {"result": "Payment already created", "http_status": status.HTTP_200_OK},
    -32400: {"result": "System error", "http_status": status.HTTP_200_OK},
    -31003: {"result": "Transaction not found.", "http_status": status.HTTP_200_OK},
    -31007: {"result": "Unable to cancel transaction", "http_status": status.HTTP_200_OK},
    -31008: {
        "result": "Operation cannot be performed. The error occurs if the transaction state does not allow the operation"
                  " to be performed.", "http_status": status.HTTP_200_OK},
    -32300: {"result": "The error occurs if the request method is not POST.", "http_status": status.HTTP_200_OK},
    -32504: {"result": "Insufficient privileges to execute the method..", "http_status": status.HTTP_200_OK}

}


def get_error_message(code):
    return error_messages.get(code, 'Unknown error')


class PaymeCustomApiException(APIException):

    def __init__(self, error_code=None, message=None, time=None):
        error_detail = get_error_message(error_code.value)
        self.status_code = error_detail['http_status']
        detail_message = message if message else error_detail['result']
        self.time = time
        self.detail = {
            "jsonrpc": "2.0",
            "error": {
                "message": detail_message,
                "code": error_code.value,
            },
        }


class ClickPrepareException(ValidationError):
    def __init__(self, enum_code, click_trans_id: int, merchant_trans_id: str, merchant_prepare_id: int):
        error, error_note = enum_code.value
        self.detail = {
            'error': error,
            'error_note': error_note,
            'click_trans_id': click_trans_id,
            'merchant_trans_id': merchant_trans_id,
            'merchant_prepare_id': merchant_prepare_id,
        }


class ClickCompleteException(ValidationError):
    def __init__(self, enum_code, click_trans_id: int, merchant_trans_id: str, merchant_confirm_id: int):
        error, error_note = enum_code.value
        self.detail = {
            'error': error,
            'error_note': error_note,
            'click_trans_id': click_trans_id,
            'merchant_trans_id': merchant_trans_id,
            'merchant_confirm_id': merchant_confirm_id,
        }


class ClickPrepareCode(Enum):
    ClickRequestError = (-8, 'Error in request from click')
    AlreadyPaidError = (-4, 'Already paid')
    SignCheckFailedError = (-1, 'SIGN CHECK FAILED!')
    UserNotFound = (-5, 'User does not exist')
    TransactionError = (-9, 'Transaction cancelled')
    IncorrectParameterAmount = (-2, 'Incorrect parameter amount')
    TransactionNotExist = (-6, 'Transaction does not exist')
    ActionNotFound = (-3, 'Action not found')
