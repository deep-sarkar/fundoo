from .exceptions import PasswordDidntMatched
from .status import response_code

def validate_password_match(password1,password2):
    if password1 != password2:
        raise PasswordDidntMatched(code =403,msg=response_code[403])
