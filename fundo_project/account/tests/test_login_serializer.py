from .. serializers import LoginSerializer
import pytest

pytestmark = pytest.mark.django_db

class TestLoginSerializer:

    def test_login_seriealizer_with_incomplete_detail_will_return_false_on_validation(self):
        data={"username":'tintin'}
        serializer = LoginSerializer(data=data)
        assert serializer.is_valid() is False

    def test_login_seriealizer_with_complete_detail_will_return_True_on_validation(self):
        data={"username":'tintin','password':'password'}
        serializer = LoginSerializer(data=data)
        assert serializer.is_valid() is True