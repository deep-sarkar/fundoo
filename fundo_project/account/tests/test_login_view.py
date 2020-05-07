import pytest
from .. import views
from django.test import RequestFactory
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db

User = get_user_model()

@pytest.mark.django_db
class TestLoginView:

    @pytest.fixture
    def setUp(self):
        User.objects.create_user(username='tintin', password='tintin123')


    def test_if_user_doesnt_exist_returns_409(self, setUp):
        detail = {
            'username':'test',
            'password':'password'
        }
        request   = RequestFactory().post('/',detail)
        response  = views.LoginAPIView.as_view()(request)
        assert response.data['code'] == 409
    
    def test_authentication_without_password_returns_406(self, setUp):
        detail = {
            'username':'tintin',
            'password':''
        }
        request   = RequestFactory().post('/',detail)
        response  = views.LoginAPIView.as_view()(request)
        assert response.data['code'] == 406
    
    def test_authentication_invalidated_password_returns_412(self, setUp):
        detail = {
            "username":"tintin",
            "password":"tintin12"
            }   
        request   = RequestFactory().post('/',detail)
        response  = views.LoginAPIView.as_view()(request)
        assert response.data['code'] == 412
        


