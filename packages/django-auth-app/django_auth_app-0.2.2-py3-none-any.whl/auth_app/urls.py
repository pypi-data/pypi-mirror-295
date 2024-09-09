from django.urls import path
from .views import CustomerRegistrationView, AdminRegistrationView, OTPVerificationView, LoginView, PasswordChangeView, LogoutView,HomeView,PasswordResetView,PasswordResetConfirmView
from .api_views import (
    RegisterAPIView,
    OTPVerificationAPIView,
    PasswordResetAPIView,
    PasswordResetConfirmAPIView,
    PasswordChangeAPIView,
    LoginAPIView,
)
urlpatterns = [
    #Web URLs
    path('register/customer/', CustomerRegistrationView.as_view(), name='register_customer'),
    path('register/admin/', AdminRegistrationView.as_view(), name='register_admin'),
    path('otp/verify/<int:user_id>/<str:action>/', OTPVerificationView.as_view(), name='otp_verify'),
    path('login/', LoginView.as_view(), name='login'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', HomeView.as_view(), name='home'),
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/<int:user_id>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    #API URLs
    path('api/register/', RegisterAPIView.as_view(), name='api_register'),
    path('api/otp-verify/', OTPVerificationAPIView.as_view(), name='api_otp_verify'),
    path('api/password-reset/', PasswordResetAPIView.as_view(), name='api_password_reset'),
    path('api/password-reset-confirm/', PasswordResetConfirmAPIView.as_view(), name='api_password_reset_confirm'),
    path('api/password-change/', PasswordChangeAPIView.as_view(), name='api_password_change'),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
]
