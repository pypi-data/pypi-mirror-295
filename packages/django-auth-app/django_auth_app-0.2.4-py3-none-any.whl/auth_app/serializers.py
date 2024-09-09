from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import OTP, Customer, AdminUser
from django.core.mail import send_mail

CustomUser = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(choices=[('customer', 'Customer'), ('admin', 'Admin')])
    address = serializers.CharField(required=False, allow_blank=True)
    department = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'user_type', 'address', 'department']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['user_type'] == 'customer' and not attrs.get('address'):
            raise serializers.ValidationError('Address is required for customers.')
        if attrs['user_type'] == 'admin' and not attrs.get('department'):
            raise serializers.ValidationError('Department is required for admin users.')
        return attrs

    def create(self, validated_data):
        user_type = validated_data.pop('user_type')

        if user_type == 'customer':
            user = Customer.objects.create_user(**validated_data)
        elif user_type == 'admin':
            user = AdminUser.objects.create_user(**validated_data)
        
        # Generate OTP for email verification
        otp = OTP.objects.create(user=user)
        otp.generate_otp_code()

        # Send OTP email
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp.otp_code}',
            'sajanac46@gmail.com',
            [user.email],
            fail_silently=False,
        )
        return user


class OTPVerificationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    otp_code = serializers.CharField(max_length=10)
    action = serializers.ChoiceField(choices=[('register', 'Registration'), ('password_reset', 'Password Reset')])

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        otp_code = attrs.get('otp_code')
        action = attrs.get('action')

        try:
            otp = OTP.objects.get(user_id=user_id, otp_code=otp_code, is_verified=False)
            if otp.is_expired():
                raise serializers.ValidationError('OTP is expired.')
        except OTP.DoesNotExist:
            raise serializers.ValidationError('Invalid OTP.')

        return attrs

    def save(self):
        user_id = self.validated_data['user_id']
        otp_code = self.validated_data['otp_code']
        action = self.validated_data['action']

        # Mark OTP as verified
        otp = OTP.objects.get(user_id=user_id, otp_code=otp_code)
        otp.is_verified = True
        otp.save()

        # Verify user
        user = CustomUser.objects.get(pk=user_id)
        user.is_verified = True
        user.save()

        # Handle different actions
        if action == 'register':
            return {'message': 'User verified and registered successfully.'}
        elif action == 'password_reset':
            return {'message': 'OTP verified. Proceed to reset the password.'}


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exist.')

        return attrs

    def save(self):
        email = self.validated_data['email']
        user = CustomUser.objects.get(email=email)

        # Generate OTP for password reset
        otp = OTP.objects.create(user=user)
        otp.generate_otp_code()

        #send otp email here
        send_mail(
            'Password Reset OTP',
            f'Use this OTP to reset your password: {otp.otp_code}',
            'sajanac46@gmail.com',
            [user.email],
            fail_silently=False,
        )


        return {'message': 'OTP sent for password reset.'}


class PasswordResetConfirmSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError("Passwords don't match.")

        return attrs

    def save(self):
        user_id = self.validated_data['user_id']
        new_password = self.validated_data['new_password']

        user = CustomUser.objects.get(pk=user_id)
        user.set_password(new_password)
        user.save()

        return {'message': 'Password reset successful. You can now log in.'}
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exist.')

        if not user.check_password(password):
            raise serializers.ValidationError('Incorrect password.')

        if not user.is_verified:
            raise serializers.ValidationError('User is not verified.')

        return attrs
    
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password') 

        if old_password == new_password:
            raise serializers.ValidationError('New password must be different from old password.')

        return attrs

    def save(self, user):
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()

        send_mail(
            'Password Changed',
            'Your password has been changed successfully.',
            'sajanac46@gmail.com',
            [user.email],
            fail_silently=False,
        )

        return {'message': 'Password changed successfully.'}
    
    
