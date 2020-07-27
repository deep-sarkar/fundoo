import pytest
from notes.views import CreateLabelView
from django.test import RequestFactory

pytestmark = pytest.mark.django_db

class TestCreateLabelView:
    def test_post_method_with_empty_data_dictionary_will_return_405(self):
        data = {}
        request  = RequestFactory().post('/',data)
        response = CreateLabelView.as_view()(request)
        assert response.data['code'] == 405