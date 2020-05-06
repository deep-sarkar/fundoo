from .exceptions import PasswordDidntMatched, PasswordPatternMatchError
from .status import response_code

#Regex
import re

def validate_password_match(password1,password2):
    if password1 != password2:
        raise PasswordDidntMatched(code=403,msg=response_code[403])

def validate_password_pattern_match(password):
    if not re.search('^[a-zA-Z0-9]{8,}$',password):
        raise PasswordPatternMatchError(code=406,msg=response_code[406])
