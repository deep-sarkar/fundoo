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

    def test_open_trash_url(self):
        path = reverse('all-trashed-notes')
        assert resolve(path).view_name == 'all-trashed-notes'

    def test_open_trash_url(self):
        path = reverse('single-trash-note', kwargs={'id':3})
        assert resolve(path).view_name == 'single-trash-note'

    def test_view_all_reminders_url(self):
        path = reverse('reminder')
        assert resolve(path).view_name == 'reminder'

    def test_view_all_archives_url(self):
        path = reverse('archive')
        assert resolve(path).view_name == 'archive'
    
    def test_view_all_pi_notes_url(self):
        path = reverse('pin-note')
        assert resolve(path).view_name == 'pin-note'