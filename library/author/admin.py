from django.contrib import admin
from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "surname",
        "patronymic",
    )

    list_filter = (
        "surname",
    )

    search_fields = (
        "name",
        "surname",
        "patronymic",
    )

    ordering = ("id",)

    fieldsets = (
        ("Author information", {
            "fields": ("name", "surname", "patronymic")
        }),
    )