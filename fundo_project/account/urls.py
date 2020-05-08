from django.urls import path
from .views import Registration, LoginAPIView, Logout, ResetPasswordView

urlpatterns = [
    path('register/', Registration.as_view(), name='registration'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('reset_password/',ResetPasswordView.as_view(), name='reset_password'),
]