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


