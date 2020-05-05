from django.test import TestCase
from django.contrib.auth import get_user_model

import pytest

User = get_user_model()



@pytest.mark.django_db
class TestUserApi:

    def test_create_user(self, django_user_model):
        username         = 'Ram'
        email            = 'ramgopal@gmail.com'
        password         = 'ram123'
        user = User.objects.create_user(username=username,
                                    email=email,
                                    password=password
                                    )
        assert (user.email==email)
        assert user.check_password(password)

    def test_check_password_match(self):
        password         = 'ram123'
        confirm_password = 'ram111'
        assert password != confirm_password

    def test_user_exists(self):
        user = User.objects.get(username='admin')
        assert user[0].exists() == False

    
    