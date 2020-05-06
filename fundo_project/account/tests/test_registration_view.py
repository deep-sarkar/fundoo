from django.test import RequestFactory
from mixer.backend.django import mixer
from .. import views
import pytest
from django.urls import reverse
from account.exceptions import PasswordDidntMatched
# from django.core.exceptions import ValidationError
from .. validate import validate_password
from .. status import response_code
from django.shortcuts import Http404

pytestmark = pytest.mark.django_db


class TestRegistrationView:


    def test_given_password_match_didnt_match_returns_403(self):
        data = {
            'first_name':'tintin',
            'last_name':'tintin',
            'username':'tintin',
            'email':'tintin@gmail.com',
            'password':'tintin',
            'confirm_password':'tinadtin',
        }
        req = RequestFactory().post('/',data)
        resp = views.Registration.as_view()(req) 
        assert resp.data['code'] == 403

    