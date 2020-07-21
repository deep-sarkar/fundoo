from django.urls import path
from .views import CreateNoteView, DisplayNotesView

urlpatterns = [
    path('create/', CreateNoteView.as_view(), name='create-note'),
    path('display/', DisplayNotesView.as_view(), name='dsiplay-notes'),

]