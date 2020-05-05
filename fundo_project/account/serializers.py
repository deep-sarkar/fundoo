from rest_framework import serializers
from django.contrib.auth import get_user_model
from .status import USERNAME_ALREADY_EXISTS, PASSWORD_DIDNT_MATCHED, EMAIL_ID_ALREAADY_EXISTS



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

    def validate_username(self, data):
        quaryset = User.objects.filter(username__iexact=data)
        if quaryset.count() != 0:
            raise serializers.ValidationError(USERNAME_ALREADY_EXISTS)
        return data
    
    def validate(self,data):
        pw = data.get('password')
        pw2 = data.get('confirm_password')
        if pw != pw2:
            raise serializers.ValidationError(PASSWORD_DIDNT_MATCHED)
        return data

    def validate_email(self, value):
        qs = User.objects.filter(email=value)
        if qs.exists():
            raise serializers.ValidationError(EMAIL_ID_ALREAADY_EXISTS)
        return value





    
