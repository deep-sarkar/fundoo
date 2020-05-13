import pytest
from django.test import RequestFactory
from .. views import ForgotPasswordView

pytestmark = pytest.mark.django_db

class TestForgotPasswordView:

    @pytest.fixture
    def setUp(self):
        self.data = {'email':'psada'}

    def test_email_is_invalid_returns_404(self, setUp):
        request  = RequestFactory().post('/', self.data)
        response = ForgotPasswordView.as_view()(request)
        assert response.data['code'] == 404
