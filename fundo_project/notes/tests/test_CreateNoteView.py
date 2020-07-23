import pytest
from ..views import CreateNoteView
from django.test import RequestFactory

# pytestmark = pytest.mark.django_db

class TestCreateNoteView:

    def test_post_method_with_empty_data_dictionary_will_return_405(self):
        data = {}
        request  = RequestFactory().post('/',data)
        response = CreateNoteView.as_view()(request)
        assert response.data['code'] == 405