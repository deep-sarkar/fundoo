from django.urls import path
from .views import CreateNoteView, DisplayNoteView

urlpatterns = [
    path('create/', CreateNoteView.as_view(), name='create-note'),
    path('display/<int:id>/', DisplayNoteView.as_view(), name='dsiplay-notes'),

]