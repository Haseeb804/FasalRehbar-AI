from django.contrib import admin
from .models import Recommendation, UserFeedback


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ("prediction", "urgency", "expert_reviewed", "ai_content_generated_at", "created_at")
    list_filter = ("urgency", "expert_reviewed", "created_at")
    search_fields = ("prediction__id", "disease__name")
    readonly_fields = ("created_at", "updated_at", "ai_content", "ai_content_generated_at", "ai_generation_error")
    fieldsets = (
        ("Prediction", {
            "fields": ("prediction", "disease")
        }),
        ("Recommendations (fallback / KB text)", {
            "fields": ("treatment_steps", "prevention_steps", "urgency")
        }),
        ("RAG-generated bilingual advice", {
            "fields": ("ai_content", "ai_content_generated_at", "ai_generation_error"),
        }),
        ("Notes", {
            "fields": ("additional_notes",)
        }),
        ("Review", {
            "fields": ("expert_reviewed", "reviewed_by")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )


@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ("user", "recommendation", "feedback_type", "rating", "created_at")
    list_filter = ("feedback_type", "rating", "created_at")
    search_fields = ("user__username", "recommendation__id")
    readonly_fields = ("created_at",)
