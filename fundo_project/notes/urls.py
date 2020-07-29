from django.urls import path
from .views import (CreateNoteView, 
                    DisplayNoteView, 
                    CreateLabelView, 
                    DisplayLabelView, 
                    AllTrashedNotesView, 
                    TrashNoteView,
                    ReminderView,
                    ArchivesNoteView,
                    PinNoteView,
                    DisplayNoteByLabelView,
                    search_by_title)


urlpatterns = [
    path('create/', CreateNoteView.as_view(), name='create-note'),
    path('open/<int:id>/', DisplayNoteView.as_view(), name='open-notes'),
    path('create/label/', CreateLabelView.as_view(), name='create-label'),
    path('open/label/<int:id>/', DisplayLabelView.as_view(), name='open-label'),
    path('trash/',AllTrashedNotesView.as_view(), name='all-trashed-notes'),
    path('trash/<int:id>/', TrashNoteView.as_view(), name='single-trash-note'),
    path('reminder/', ReminderView.as_view(), name='reminder'),
    path('archives/', ArchivesNoteView.as_view(), name='archive'),
    path('pinnotes/', PinNoteView.as_view(), name='pin-note'),
    path('display/<label>/', DisplayNoteByLabelView.as_view(), name='display-label-with-note'),
    path('search/title/', search_by_title)
]