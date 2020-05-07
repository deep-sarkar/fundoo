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
    
    def test_on_existing_of_given_username_returns_407(self):
        data1 = {
            'first_name':'tintin',
            'last_name':'tintin',
            'username':'deep',
            'email':'tintin@gmail.com',
            'password':'tintin123',
            'confirm_password':'tintin123',
        }
        req = RequestFactory().post('/',data1)
        resp = views.Registration.as_view()(req) 
        assert resp.status_code == 200

        data2 = {
            'first_name':'tintin',
            'last_name':'tintin',
            'username':'deep',
            'email':'tintin@gmail.com',
            'password':'tintin123',
            'confirm_password':'tintin123',
        }
        req = RequestFactory().post('/',data2)
        resp = views.Registration.as_view()(req) 
        assert resp.data['code'] == 407

    def test_on_existing_of_given_email_returns_408(self):
        data1 = {
            'first_name':'tintin',
            'last_name':'tintin',
            'username':'deep',
            'email':'tintin@gmail.com',
            'password':'tintin123',
            'confirm_password':'tintin123',
        }
        req = RequestFactory().post('/',data1)
        resp = views.Registration.as_view()(req) 
        assert resp.status_code == 200

        data2 = {
            'first_name':'tintin',
            'last_name':'tintin',
            'username':'deep1',
            'email':'tintin@gmail.com',
            'password':'tintin123',
            'confirm_password':'tintin123',
        }
        req = RequestFactory().post('/',data2)
        resp = views.Registration.as_view()(req) 
        assert resp.data['code'] == 408

    def test_if_email_is_invalid_returns_404(self):
        data = {
            'first_name':'tintin',
            'last_name':'tintin',
            'username':'tintin',
            'email':'tintin',
            'password':'tin1##1',
            'confirm_password':'tin1##1'
        }
        req = RequestFactory().post('/',data)
        resp = views.Registration.as_view()(req) 
        assert resp.data['code'] == 404