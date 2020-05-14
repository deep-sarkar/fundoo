#imports from rest-framework
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

#import from django
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.core.validators import validate_email
from django.template.loader import render_to_string
from django.shortcuts import redirect, HttpResponse

#Short url
from django_short_url.views import get_surl
from django_short_url.models import ShortURL

#mailing
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from fundo_project.settings import EMAIL_HOST_USER


#import from status
from .status import response_code

#import from serializers
from .serializers import RegistrationSerializer, LoginSerializer, ResetPasswordSerializer, ForgotPasswordSerializer

#token
from .jwt_token import generate_token

#errors
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .exceptions import (PasswordDidntMatched, 
                        PasswordPatternMatchError,
                        UsernameAlreadyExistsError,
                        EmailAlreadyExistsError,
                        UsernameDoesNotExistsError,
                        EmailDoesNotExistsError
                        )
from smtplib import SMTPException

#regular expression
import re

#redis
import redis

#validator
from .validate import (validate_password_match,
                       validate_password_pattern_match,
                       validate_duplicat_username_existance,
                       validate_duplicate_email_existance,
                       validate_user_does_not_exists,
                       validate_email_does_not_exists,
                      )   

import jwt

#User model
User = get_user_model()

#redis object
redis_object = redis.Redis(host='localhost', port=6379,db=0)



class Registration(GenericAPIView):
    serializer_class = RegistrationSerializer
    

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'code':410,'msg':response_code[410]})
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
        user_obj = User.objects.create_user(first_name=first_name,
                                       last_name=last_name,
                                       username=username,
                                       email=email ,
                                       password=password
                                        )
        user_obj.is_active = False
        user_obj.save()
        payload = {
            'username':username,
            'password':password
        }
        token       = generate_token(payload)
        surl        = get_surl(str(token)) 
        final_url   = surl.split('/')
        curren_site = get_current_site(request)
        domain      = curren_site.domain
        subject     = "Account activation url"
        msg = render_to_string(
                'account/account_activation.html',
                {
                    'username': username, 
                    'domain': domain,
                    'surl': final_url[2],
                })
        try:
            send_mail(subject, msg, EMAIL_HOST_USER,
                        [email], fail_silently=False)
        except SMTPException:
            return Response({'code':301,'msg':response_code[301]})
        return Response({"code":201, "msg":response_code[201]})



class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'code':410,'msg':response_code[410]})
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            validate_user_does_not_exists(username)
            validate_password_pattern_match(password)
        except UsernameDoesNotExistsError as e:
            return Response({'code':e.code,'msg':e.msg})
        except PasswordPatternMatchError as e :
            return Response({'code':e.code,'msg':e.msg})
        user_obj = authenticate(request, username=username, password=password)
        if user_obj is not None:
            if user_obj.is_active:
                login(request,user_obj)
                payload = {
                    'username':username
                }
                token = generate_token(payload)
                redis_object.set(username,token)
                return Response({'code':200,'msg':response_code[200]})
            return Response({'code':411,'msg':response_code[411]})
        return Response({'code':412,'msg':response_code[412]})

class Logout(GenericAPIView):
    serializer_class = LoginSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            username = request.user.username
            redis_object.delete(username)
            logout(request)
        return Response({'code':200,'msg':response_code[200]})

class ResetPasswordView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        username         = self.request.user.username
        password         = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        try:
            validate_password_pattern_match(password)
            validate_password_match(password,confirm_password)
            validate_user_does_not_exists(username)
        except PasswordDidntMatched as e:
            return Response({"code":e.code,"msg":e.msg})
        except PasswordPatternMatchError as e:
            return Response({"code":e.code,"msg":e.msg})
        except UsernameDoesNotExistsError as e:
            return Response({'code':e.code,'msg':e.msg})
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        return Response({'code':200, 'msg':response_code[200]})
        
class ActivateAccount(GenericAPIView):
    serializer_class = LoginSerializer

    def get(self, request, surl):
        token_obj = ShortURL.objects.get(surl=surl)
        token     = token_obj.lurl
        try:
            decode    = jwt.decode(token, 'SECRET_KEY')
        except jwt.DecodeError:
            return Response({'code':304,'msg':response_code[304]})
        username  = decode['username']
        try:
            validate_user_does_not_exists(username)
        except UsernameDoesNotExistsError as e:
            return Response({'code':e.code, 'msg':e.msg})
        user = User.objects.get(username=username)
        if user.is_active:
            return Response({'code':302, 'msg':response_code[302]})
        else:
            user.is_active = True
            user.save()
            return Response({'code':200,'msg':response_code[200]})

class ForgotPasswordView(GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            return Response({'code':404,'msg':response_code[404]})
        user = User.objects.filter(email=email)
        try:
            username = user.values()[0]['username'] 
        except IndexError:
            return Response({'code':303,'msg':response_code[303]})
        payload = {
                'username': username,
                }
        token = generate_token(payload)
        current_site = get_current_site(request)
        domain_name = current_site.domain
        surl = get_surl(str(token))
        final_url = surl.split("/")
        mail_subject = "Reset Your password by clicking below link"
        msg = render_to_string(
            'account/forgot_password.html',
            {
                'username': username, 
                'domain': domain_name,
                'surl': final_url[2],
                })
        try:            
            send_mail(mail_subject, msg, EMAIL_HOST_USER,
                    [email], fail_silently=False)
            return Response({'code':200,'msg':response_code[200]})
        except SMTPException:
            return Response({'code':301,'msg':response_code[301]})


def reset_new_password(request,surl):
    token_obj = ShortURL.objects.get(surl=surl)
    token = token_obj.lurl
    try:
        decode = jwt.decode(token,'SECRET_KEY')
    except jwt.DecodeError:
        return Response({'code':304,'msg':response_code[304]})
    username = decode['username']
    user = User.objects.get(username=username)
    return redirect('http://127.0.0.1:8000/account/activate_new_password/' + str(user)+'/')
   
class ActivateNewPassword(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, user_reset):
        password         = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        try:
            validate_password_match(password, confirm_password)
            validate_password_pattern_match(password)
        except PasswordDidntMatched as e:
            return Response({"code":e.code,"msg":e.msg})
        except PasswordPatternMatchError as e:
            return Response({"code":e.code,"msg":e.msg})
        user = User.objects.get(username__exact=user_reset)
        user.set_password(password)
        user.save()
        return Response({'code':200,'msg':response_code[200]})
        