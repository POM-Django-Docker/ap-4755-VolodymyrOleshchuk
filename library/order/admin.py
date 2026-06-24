from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "book",
        "user",
        "created_at",
        "end_at",
        "plated_end_at",
    )

    list_filter = (
        "book",
        "user",
        "end_at",
    )

    search_fields = (
        "book__name",
        "user__email",
    )

    ordering = ("id",)

    fieldsets = (
        ("Order information", {
            "fields": ("book", "user")
        }),
        ("Date information", {
            "fields": ("created_at", "plated_end_at", "end_at")
        }),
    )

    readonly_fields = ("created_at",)