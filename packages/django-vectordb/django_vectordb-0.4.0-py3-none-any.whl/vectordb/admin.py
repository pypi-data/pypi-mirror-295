from __future__ import annotations

from django.contrib import admin

from .models import Vector


class VectorAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "created_at", "updated_at", "metadata")
    list_filter = ("created_at", "updated_at", "content_type")
    search_fields = ("text",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "text",
        "metadata",
        "embedding",
        "content_type",
        "content_object",
        "object_id",
    )


admin.site.register(Vector, VectorAdmin)
