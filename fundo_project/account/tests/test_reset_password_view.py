from .. views import ResetPasswordView
import pytest
from django.test import RequestFactory

pytestmark = pytest.mark.django_db

class TestResetPasswordView:

    @pytest.fixture
    def setUp(self):
        self.data1 = {'password':'ps','confirm_password':'ps'}
        self.data2 = {'password':'password','confirm_password':'pwssword'}
        

    def test_password_format_error_raises_406(self, setUp):
        request  = RequestFactory().post('/',self.data1)
        response = ResetPasswordView.as_view()(request)
        assert response.data['code'] == 406
    
    def test_password_match_error_raises_403(self, setUp):
        request  = RequestFactory().post('/',self.data2)
        response = ResetPasswordView.as_view()(request)
        assert response.data['code'] == 403

