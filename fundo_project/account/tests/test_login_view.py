import pytest
from .. import views
from django.test import RequestFactory

pytestmark = pytest.mark.django_backend


class TestLoginView:

    def __init__(self,username,password):
        self.username = "tintin"
        self.email    = "tintin@gmail.com"
        self.password = "tintin11"


    def test_if_user_doesnt_exist_returns_409(self):
        username = self.username
        request   = RequestFactory().post('/',username)
        response  = views.LoginAPIView.as_view()(request)
        assert response.data['code'] == 409


