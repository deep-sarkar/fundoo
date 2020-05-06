from .exceptions import PasswordDidntMatched, PasswordPatternMatchError, UsernameAlreadyExistsError
from .status import response_code
from django.contrib.auth import get_user_model


User = get_user_model()


#Regex
import re

def validate_password_match(password1,password2):
    if password1 != password2:
        raise PasswordDidntMatched(code=403,msg=response_code[403])

def validate_password_pattern_match(password):
    if not re.search('^[a-zA-Z0-9]{8,}$',password):
        raise PasswordPatternMatchError(code=406,msg=response_code[406])

def validate_username_existance(username):
    if User.objects.filter(username=username).exists():
        raise UsernameAlreadyExistsError(code=407,msg=response_code[407])
