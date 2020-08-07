from django.urls import resolve, reverse

class TestUrls:

    def test_create_note_url(self):
        path = reverse('create-note')
        assert resolve(path).view_name == 'create-note'