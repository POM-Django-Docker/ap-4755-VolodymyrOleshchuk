from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    list_filter = (
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
    )

    ordering = ("id",)

    fieldsets = (
        ("Login information", {
            "fields": ("email", "password")
        }),
        ("Personal information", {
            "fields": ("first_name", "middle_name", "last_name")
        }),
        ("Permissions", {
            "fields": ("role", "is_active", "is_staff", "is_superuser")
        }),
        ("System information", {
            "fields": ("created_at", "updated_at")
        }),
    )

    readonly_fields = ("created_at", "updated_at")