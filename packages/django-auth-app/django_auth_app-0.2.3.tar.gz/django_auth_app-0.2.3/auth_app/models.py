from django.contrib.auth.models import AbstractUser,Group,Permission
from django.db import models
from django.utils import timezone
import string
import random


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    # Add any common fields here
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
    
    

class Customer(CustomUser):
    # Add customer-specific fields here
    address = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return f"{self.email} (Customer)"

class AdminUser(CustomUser):
    # Add admin-specific fields here
    department = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Admin User'
        verbose_name_plural = 'Admin Users'

    def __str__(self):
        return f"{self.email} (Admin User)"


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