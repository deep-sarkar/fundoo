from .. serializers import RegistrationSerializer
import pytest

pytestmark = pytest.mark.django_db

class TestRegistrationSerializer:

    def test_serializer_will_fail_and_assert_false_if_data_is_empty(self):
        serializer = RegistrationSerializer(data={})
        assert serializer.is_valid() is False

    def test_serializer_will_fail_and_assert_true_if_data_is_valid(self):
        data = {
            'first_name':'tintin',
            'last_name':'tintin',
            'username':'tintin',
            'email':'tintin@gmail.com',
            'password':'tintin',
            'confirm_password':'tinadtin',
        }
        serializer = RegistrationSerializer(data=data)
        assert serializer.is_valid() is True