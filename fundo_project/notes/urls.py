from django.urls import path
from .views import (CreateNoteView, 
                    DisplayNoteView, 
                    CreateLabelView, 
                    DisplayLabelView, 
                    AllTrashedNotesView, 
                    TrashNoteView,
                    ReminderView,
                    ArchivesNoteView)


urlpatterns = [
    path('create/', CreateNoteView.as_view(), name='create-note'),
    path('open/<int:id>/', DisplayNoteView.as_view(), name='open-notes'),
    path('create/label/', CreateLabelView.as_view(), name='create-label'),
    path('open/label/<int:id>/', DisplayLabelView.as_view(), name='open-label'),
    path('trash/',AllTrashedNotesView.as_view(), name='all-trashed-notes'),
    path('trash/<int:id>/', TrashNoteView.as_view(), name='single-trash-note'),
    path('reminder/', ReminderView.as_view(), name='reminder'),
    path('archives/', ArchivesNoteView.as_view(), name='archive'),
]