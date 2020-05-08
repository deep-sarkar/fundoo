from .. import serializers
import pytest

pytestmark = pytest.mark.django_db

class TestResetPasswordSerializer:
    
    data1 = {}
    data2 = {'password':'admin123','confirm_password':'admin123'}

    @pytest.mark.parametrize("data, response", [pytest.param(data1, False),pytest.param(data2, True)])
    def test_reset_password_serializer(self,data,response):
        serializer = serializers.ResetPasswordSerializer(data=data)
        assert serializer.is_valid() is response
