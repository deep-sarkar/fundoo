from django.test import RequestFactory
from .. import views
import pytest

from .. status import response_code

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

    def test_given_password_is_not_valid_returns_406(self):
        data = {
            'first_name':'tintin',
            'last_name':'tintin',
            'username':'tintin',
            'email':'tintin@gmail.com',
            'password':'tin1##1',
            'confirm_password':'tin1##1'
        }
        req = RequestFactory().post('/',data)
        resp = views.Registration.as_view()(req) 
        assert resp.data['code'] == 406

    