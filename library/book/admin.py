from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "count",
        "get_authors",
    )

    list_filter = (
        "id",
        "authors",
    )

    search_fields = (
        "name",
        "authors__name",
        "authors__surname",
    )

    ordering = ("id",)

    fieldsets = (
        ("Information that does not change", {
            "fields": ("name", "authors")
        }),
        ("Information that can change", {
            "fields": ("description", "count")
        }),
    )

    filter_horizontal = ("authors",)

    def get_authors(self, obj):
        return ", ".join(
            [f"{author.name} {author.surname}" for author in obj.authors.all()]
        )

    get_authors.short_description = "Authors"