#imports from rest-framework
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

#import from django
from django.contrib.auth import get_user_model
from django.core.validators import validate_email


#import from status
from .status import response_code

#import from serializers
from .serializers import RegistrationSerializer

#token
from .jwt_token import generate_token

#errors
from django.core.exceptions import ValidationError
from .exceptions import (PasswordDidntMatched, 
                        PasswordPatternMatchError,
                        UsernameAlreadyExistsError,
                        EmailAlreadyExistsError,
                        )
#regular expression
import re

#validator
from .validate import (validate_password_match,
                       validate_password_pattern_match,
                       validate_duplicat_username_existance,
                       validate_duplicate_email_existance,
                      )   

#User model
User = get_user_model()



class Registration(GenericAPIView):
    serializer_class = RegistrationSerializer
    

    def post(self, request, *args, **kwargs):
        first_name           = request.data.get('first_name')
        last_name            = request.data.get('last_name')
        username             = request.data.get('username')
        email                = request.data.get('email')
        password             = request.data.get('password')
        confirm_password     = request.data.get('confirm_password')
        try:
            validate_email(email)
        except ValidationError:
            return Response({'code':404,'msg':response_code[404]})
        try:
            validate_password_match(password,confirm_password)
            validate_password_pattern_match(password)
        except PasswordDidntMatched as e:
            return Response({"code":e.code,"msg":e.msg})
        except PasswordPatternMatchError as e:
            return Response({"code":e.code,"msg":e.msg})
        try:
            validate_duplicat_username_existance(username)
        except UsernameAlreadyExistsError as e:
            return Response({"code":e.code,"msg":e.msg})
        try:
            validate_duplicate_email_existance(email)
        except EmailAlreadyExistsError as e:
            return Response({"code":e.code,"msg":e.msg})
        user_obj = User.objects.create(first_name=first_name,
                                       last_name=last_name,
                                       username=username,
                                       email=email 
                                        )
        user_obj.is_active = False
        user_obj.set_password(password)
        user_obj.save()
        payload = {
            'username':username,
            'password':password
        }
        token = generate_token(payload)
        return Response(token)


        

        