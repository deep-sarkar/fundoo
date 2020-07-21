from rest_framework.exceptions import APIException, NotFound

class DoesNotExistException(APIException):
    code=401
    detail="Not found"