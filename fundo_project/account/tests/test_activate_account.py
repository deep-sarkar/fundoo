import pytest
from .. import views, jwt_token
import jwt

pytestmark = pytest.mark.django_db

class TestActivateAccount:

    def test_generate_token(self):
        payload = {
            'username':'tintin',
            'password':'tintin123'
        }
        token  = jwt_token.generate_token(payload)
        decode = jwt.decode(token, 'SECRET_KEY')
        assert decode['username'] == payload['username']

