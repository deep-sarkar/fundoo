from django.urls import resolve, reverse

class TestUrls:

    def test_create_note_url(self):
        path = reverse('create-note')
        assert resolve(path).view_name == 'create-note'

    def test_open_note_url(self):
        path = reverse('open-notes', kwargs={'id':2})
        assert resolve(path).view_name == 'open-notes'

    def test_create_label_url(self):
        path = reverse('create-label')
        assert resolve(path).view_name == 'create-label'

    def test_open_label_url(self):
        path = reverse('open-label', kwargs={'id':2})
        assert resolve(path).view_name == 'open-label'