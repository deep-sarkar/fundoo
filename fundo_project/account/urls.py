from django.urls import path
from .views import(Registration, 
                    LoginAPIView, 
                    Logout, 
                    ResetPasswordView, 
                    ActivateAccount, 
                    ForgotPasswordView,
                    reset_new_password,
                    ActivateNewPassword,
                    Home
                    ) 

urlpatterns = [
    path('profile/', Home.as_view() , name='profile'),
    path('register/', Registration.as_view(), name='registration'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('reset_password/',ResetPasswordView.as_view(), name='reset_password'),
    path('activate/<surl>/', ActivateAccount.as_view(), name='activate'),
    path('forgot_password/',ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset_new_password/<surl>/',reset_new_password, name='reset_new_password'),
    path('activate_new_password/<user_reset>/', ActivateNewPassword.as_view(), name='activate_new_password'),
]