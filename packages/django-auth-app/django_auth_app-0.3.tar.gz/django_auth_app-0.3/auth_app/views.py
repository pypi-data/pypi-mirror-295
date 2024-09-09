from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from .models import OTP, CustomUser, Customer, AdminUser
from django.contrib import messages

CustomUser = get_user_model()

class HomeView(TemplateView):
    template_name = 'auth_app/home.html'

class LoginView(TemplateView):
    template_name = 'auth_app/login.html'

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

        return render(request, self.template_name)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class CustomerRegistrationView(TemplateView):
    template_name = 'auth_app/register_customer.html'

    def post(self, request):
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        
        user = Customer.create_customer(username=username, email=email, password=password, address=address)
        otp = OTP.objects.create(user=user)
        otp.generate_otp_code()
        
        # Send OTP email
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp.otp_code}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
        return redirect('otp_verify', user_id=user.id, action='register')


class AdminRegistrationView(TemplateView):
    template_name = 'auth_app/register_admin.html'

    def post(self, request):
        # Handle admin registration
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        department = request.POST.get('department')
        
        if not department:
            messages.error(request, 'Department is required for admin users.')
            return render(request, self.template_name)

        user = AdminUser.create_admin(username=username, email=email, password=password, department=department)
        otp = OTP.objects.create(user=user)
        otp.generate_otp_code()
        
        # Send OTP email
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp.otp_code}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
        return redirect('otp_verify', user_id=user.id, action='register')

class OTPVerificationView(TemplateView):
    template_name = 'auth_app/otp_verify.html'

    def dispatch(self, request, *args, **kwargs):
        # Capture user_id and action from kwargs and pass them to post
        self.user_id = kwargs.get('user_id')
        self.action = kwargs.get('action')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        otp_code = request.POST.get('otp_code')
        try:
            otp = OTP.objects.get(user_id=self.user_id, otp_code=otp_code, is_verified=False)
            if otp.is_expired():
                return redirect('otp_resend', user_id=self.user_id)

            otp.is_verified = True
            otp.save()

            user = CustomUser.objects.get(pk=self.user_id)
            user.is_verified = True
            user.save()

            if self.action == 'register':
                login(request, user)
                return redirect('home')
            elif self.action == 'password_reset':
                return redirect('password_reset_confirm', user_id=self.user_id)

        except OTP.DoesNotExist:
            return render(request, self.template_name, {'error': 'Invalid OTP', 'user_id': self.user_id, 'action': self.action})

class PasswordChangeView(LoginRequiredMixin, TemplateView):
    template_name = 'auth_app/password_change.html'

    def post(self, request):
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        user = request.user
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            # Optionally, send an email notification about the password change
            send_mail(
                'Password Changed',
                'Your password has been changed successfully.',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
            return redirect('login')
        else:
            return render(request, self.template_name, {'error': 'Incorrect old password'})

class PasswordResetView(TemplateView):
    template_name = 'auth_app/password_reset.html'

    def post(self, request):
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            otp = OTP.objects.create(user=user)
            otp.generate_otp_code()
            # Send OTP to user's email
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp.otp_code}',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
            return redirect('otp_verify', user_id=user.id, action='password_reset')
        except CustomUser.DoesNotExist:
            return render(request, self.template_name, {'error': 'Email not found'})
        
class PasswordResetConfirmView(TemplateView):
    template_name = 'auth_app/password_reset_confirm.html'

    def post(self, request, user_id):
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            return render(request, self.template_name, {'error': 'Passwords do not match', 'user_id': user_id})
        
        user = CustomUser.objects.get(pk=user_id)
        user.set_password(new_password)
        user.save()
        return redirect('login')
