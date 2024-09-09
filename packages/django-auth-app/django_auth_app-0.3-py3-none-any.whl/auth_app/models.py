from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
import string
import random


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Changed related_name to avoid clashes
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
        related_query_name='customuser',
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Changed related_name to avoid clashes
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
        related_query_name='customuser_permission',
    )
    

    def __str__(self):
        return self.email


class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer_profile')
    address = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return f"{self.user.email} (Customer)"
    
    @classmethod
    def create_customer(cls, username, email, password, address):
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        cls.objects.create(user=user, address=address)
        return user  # Return the CustomUser instance


class AdminUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='admin_profile')
    department = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Admin User'
        verbose_name_plural = 'Admin Users'

    def __str__(self):
        return f"{self.user.email} (Admin User)"
    
    @classmethod
    def create_admin_user(cls, username, email, password, department):
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        cls.objects.create(user=user, department=department)
        return user # Return the CustomUser instance


class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def generate_otp_code(self):
        characters = string.ascii_letters + string.digits
        self.otp_code = ''.join(random.choice(characters) for _ in range(6))
        self.save()

    def is_expired(self):
        return (timezone.now() - self.created_at).total_seconds() > 300  # OTP validity of 5 minutes
