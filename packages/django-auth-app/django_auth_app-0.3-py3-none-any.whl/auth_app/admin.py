from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Customer, AdminUser,OTP

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_verified', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_verified',)}),
    )

class OTPAdmin(admin.ModelAdmin):
    model = OTP
    list_display = ('user', 'otp_code', 'is_verified')
    fields = ('user', 'otp_code', 'is_verified')


admin.site.register(OTP, OTPAdmin)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Customer)
admin.site.register(AdminUser)
