from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Customer, AdminUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_verified', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_verified',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Customer)
admin.site.register(AdminUser)
