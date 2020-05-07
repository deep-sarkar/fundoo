from django.urls import path
from .views import Registration, LoginAPIView

urlpatterns = [
    path('register/', Registration.as_view(), name='registration'),
    path('login/', LoginAPIView.as_view(), name='login'),
]