from django.contrib import admin
from .models import PredictionHistory


@admin.register(PredictionHistory)
class PredictionHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "prediction", "is_archived", "created_at")
    list_filter = ("created_at", "is_archived", "user")
    search_fields = ("user__username", "tags", "notes")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Information", {
            "fields": ("user", "prediction")
        }),
        ("Notes", {
            "fields": ("notes", "tags")
        }),
        ("Status", {
            "fields": ("is_archived",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
