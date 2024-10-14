from django.urls import path
from .views import *

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path('verify/phone/', VerifyPhoneView.as_view(), name='phone-verify'),
    path('sendcode/', SendCodeView.as_view(), name='send-sms'),
    path('login', LoginView.as_view(), name='login'),
    path('password/change', ChangePasswordView.as_view(), name='password-change'),
    path('password/forgot', ForgotPasswordView.as_view(), name='password-forgot')
]
