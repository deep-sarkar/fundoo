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
from .exceptions import PasswordDidntMatched
#regular expression
import re

#validator
from .validate import validate_password_match

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
            return Response(response_code[404])
        try:
           validate_password_match(password,confirm_password)
        except PasswordDidntMatched as e:
            return Response({"code":e.code,"msg":e.msg})
        if User.objects.filter(username=username).count() != 0:
            return Response(response_code[401])
        if User.objects.filter(email=email).count() != 0:
            return Response(response_code[402])
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
        return Response(response_code[201])


        

        