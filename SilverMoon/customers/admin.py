from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("phone", "fullname", "is_staff", "is_active",)
    list_filter = ("phone", "fullname", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("fullname", "phone", "password")}),
        ("Permissions", {"fields": ("is_superuser", "is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "fullname", "phone", "password1", "password2", "is_staff",
                "is_superuser", "is_active", "groups", "user_permissions"
            )}
         ),
    )
    search_fields = ("phone",)
    ordering = ("phone",)
