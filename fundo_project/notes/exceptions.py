from rest_framework.exceptions import APIException, NotFound

class DoesNotExistException(APIException):
    pass