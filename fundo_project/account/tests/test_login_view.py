import pytest
from .. import views
from django.test import RequestFactory
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db

User = get_user_model()

@pytest.mark.django_db
class TestLoginView:

    def test_if_user_doesnt_exist_returns_409(self,db):
        user = User.objects.create(first_name ='tintin', last_name='tintin', username='tintin',
                                    email='tintin@gmail.com')
        user.set_password('password')
        detail = {
            'username':'test',
            'password':'password'
        }
        request   = RequestFactory().post('/',detail)
        response  = views.LoginAPIView.as_view()(request)
        assert response.data['code'] == 409
    
    def test_authentication_without_password_returns_406(self):
        user = User.objects.create(first_name ='tintin', last_name='tintin', username='tintin',
                                    email='tintin@gmail.com')
        user.set_password('password')
        detail = {
            'username':'tintin',
            'password':''
        }
        request   = RequestFactory().post('/',detail)
        response  = views.LoginAPIView.as_view()(request)
        assert response.data['code'] == 406
    
    def test_authentication_invalidated_password_returns_200(self):
        user = User.objects.create(first_name ='tintin', last_name='tintin', username='tintin',
                                    email='tintin@gmail.com')
        user.is_active = True
        user.set_password("tintin123")
        detail = {
            "username":"tintin",
            "password":"tintin12"
            }   
        request   = RequestFactory().post('/account/login/',detail)
        response  = views.LoginAPIView.as_view()(request)
        assert response.data['code'] == 412


