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

    # def validate(self,data):
    #     password = data.get('password')
    #     confirm_password = data.get('confirm_password')
    #     if password != confirm_password:
    #         raise PasswordDidntMatched(response_code[403])
    #     return data
        
    # def create(self,validated_data):
    #     user_obj = User(first_name=validated_data.get('first_name'),
    #                     last_name=validated_data.get('last_name'),
    #                     username=validated_data.get('username'), 
    #                     email = validated_data.get('email'))
    #     user_obj.set_password(validated_data.get('password'))
    #     user_obj.active = False
    #     user_obj.save()
    #     return user_obj
        

  



    
