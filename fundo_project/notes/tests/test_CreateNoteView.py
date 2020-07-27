import pytest
from ..views import CreateNoteView
from django.test import RequestFactory

import mock
import os

pytestmark = pytest.mark.django_db

class TestCreateNoteView:

    def test_post_method_with_empty_data_dictionary_will_return_405(self):
        data = {}
        request  = RequestFactory().post('/',data)
        response = CreateNoteView.as_view()(request)
        assert response.data['code'] == 405


    def test_get_method_returns_200(self):
        request  = RequestFactory().get('/')
        response = CreateNoteView.as_view()(request)
        assert response.status_code == 200

    # @mock.patch('notes.views.CreateNoteView.post.user', mock.MagicMock(return_value=1))
    # def test_post_method_with_valid_data_dictionary_will_return_201(self):
    #     data = {
    #         'title':'hello',
    #         'label':'',
    #     }
    #     request  = RequestFactory().post('/',data)
    #     response = CreateNoteView.as_view()(request)
    #     assert response.data['code'] == 201
    