from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import CustomUser

class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class AdminRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class OTPVerificationForm(forms.Form):
    otp_code = forms.CharField(max_length=10)

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)
