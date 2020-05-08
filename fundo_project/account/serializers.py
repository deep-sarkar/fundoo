from rest_framework import serializers
from django.contrib.auth import get_user_model
from .exceptions import PasswordDidntMatched
from .status import response_code



User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'confirm_password',
            ]
        extra_kwargs = {'password':{'write_only':True}}
        required_fields = ['username','email','password','confirm_password']

class LoginSerializer(serializers.ModelSerializer):
    password        = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model  = User
        fields = [
            'username',
            'password',
        ]
        extra_kwargs = {'password':{'write_only':True}}
        required_fields = fields

class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = [
            'password',
            'confirm_password'
        ]