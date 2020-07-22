from django.urls import path
from .views import CreateNoteView, DisplayNoteView, CreateLabelView, DisplayLabelView

urlpatterns = [
    path('create/', CreateNoteView.as_view(), name='create-note'),
    path('display/<int:id>/', DisplayNoteView.as_view(), name='dsiplay-notes'),
    path('create-label/', CreateLabelView.as_view(), name='create-label'),
    path('display-label/<int:id>/', DisplayLabelView.as_view(), name='display-label'),
]