from django.urls import path
from .views import CreateNoteView

urlpatterns = [
    path('create/', CreateNoteView.as_view(), name='create-note'),

]