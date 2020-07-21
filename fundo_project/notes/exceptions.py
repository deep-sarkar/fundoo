from rest_framework.exceptions import APIException

class DoesNotExistException(APIException):
    status_code = 409
    default_detail = 'Note does not exists'
    default_code = 'DOES NOT EXISTS'