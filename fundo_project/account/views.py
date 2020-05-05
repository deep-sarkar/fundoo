#imports from rest-framework
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

#import from django
from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator


#import from status
from .status import (CREATED, 
            USERNAME_ALREADY_EXISTS,
             EMAIL_ID_ALREAADY_EXISTS,
              PASSWORD_DIDNT_MATCHED,
              VALIDATION_ERROR
              )

#import from serializers
from .serializers import RegistrationSerializer

from .jwt_token import generate_token

#errors
from django.core.exceptions import ValidationError

#User model
User = get_user_model()



class Registration(GenericAPIView):
    serializer_class = RegistrationSerializer
    

    def post(self, request, *args, **kwargs):
        first_name    = request.data.get('first_name')
        last_name     = request.data.get('last_name')
        username      = request.data.get('username')
        email         = request.data.get('email')
        password      = request.data.get('password')
        password2     = request.data.get('confirm_password')
        try:
            EmailValidator(email)
        except ValidationError:
            return Response(ValidationError)
        if password != password2:
            return Response(PASSWORD_DIDNT_MATCHED)
        queryset      = User.objects.filter(username=username)
        if queryset.count() != 0:
            return Response(USERNAME_ALREADY_EXISTS)
        queryset      = User.objects.filter(email=email)
        if queryset.count() != 0:
            return Response(EMAIL_ID_ALREAADY_EXISTS)
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


        

        