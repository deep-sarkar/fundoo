import pytest
from .. serializers import ForgotPasswordSerializer

class TestForgotpasswordSerializer:

    testdata = [("", False),({'email':'deep@gmail.com'},True)]

    @pytest.mark.parametrize('data, response',testdata)
    def test_forgot_password_serializer(self, data, response):
        serializer = ForgotPasswordSerializer(data=data)
        assert serializer.is_valid() is response

    