from rest_framework.exceptions import APIException
from account.status import response_code

class DoesNotExistException(APIException):
    status_code = 409
    default_detail = response_code[409]
    default_code = response_code[409]

class PassedTimeException(APIException):
    status_code = 415
    default_detail = response_code[415]
    default_code = response_code[415]