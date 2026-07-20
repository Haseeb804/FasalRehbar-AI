from django.contrib import admin

from .models import ActivityLog, ContactMessage, Crop, Disease, FAQ, Feedback, Notification

admin.site.site_header = "PakAgri Administration"
admin.site.site_title = "PakAgri Admin"
admin.site.index_title = "Agricultural Intelligence Dashboard"


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ("name", "scientific_name", "is_active", "created_at")
    search_fields = ("name", "scientific_name")
    list_filter = ("is_active",)


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ("name", "crop", "severity", "needs_content", "is_active")
    search_fields = ("name", "description", "symptoms", "raw_class_name")
    list_filter = ("crop", "severity", "needs_content", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("raw_class_name",)


admin.site.register(FAQ)
admin.site.register(ContactMessage)
admin.site.register(Feedback)
admin.site.register(Notification)
admin.site.register(ActivityLog)
