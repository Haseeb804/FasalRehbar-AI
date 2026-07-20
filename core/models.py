from django.conf import settings
from django.db import models


class Crop(models.Model):
    name = models.CharField(max_length=120, unique=True)
    scientific_name = models.CharField(max_length=160, blank=True)
    description = models.TextField(blank=True)
    growing_conditions = models.TextField(blank=True)
    image = models.ImageField(upload_to="crops/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Disease(models.Model):
    class Severity(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True, blank=True, related_name="diseases")
    name = models.CharField(max_length=160)
    slug = models.SlugField()
    # The exact class-folder string the ML models were trained on (e.g. "Bulb_blight-D"),
    # used to reliably map a model's raw prediction back to this row regardless of how
    # `name`/`slug` get cleaned up for display. Populated by `sync_ml_metadata`.
    raw_class_name = models.CharField(
        max_length=160, blank=True,
        help_text="Exact class-folder name used during training (for robust ML->DB mapping).",
    )
    description = models.TextField(blank=True)
    symptoms = models.TextField(blank=True)
    causes = models.TextField(blank=True)
    treatment = models.TextField(blank=True)
    prevention = models.TextField(blank=True)
    severity = models.CharField(max_length=16, choices=Severity.choices, default=Severity.MEDIUM)
    image = models.ImageField(upload_to="diseases/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    # Set True by sync_ml_metadata when it auto-creates a disease row with no KB text yet,
    # so admins can find and fill these in easily from the admin list view.
    needs_content = models.BooleanField(
        default=False,
        help_text="True if this disease was auto-created from model class data and still needs KB content filled in.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        # NOTE: name/slug are intentionally NOT globally unique — the same disease name
        # (e.g. "Rust", "Healthy") legitimately appears under more than one crop.
        unique_together = [("crop", "name"), ("crop", "slug")]

    def __str__(self) -> str:
        crop_name = self.crop.name if self.crop else "Unknown crop"
        return f"{self.name} ({crop_name})"


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(max_length=120, default="General")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "question"]

    def __str__(self) -> str:
        return self.question


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=160)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.subject} - {self.email}"


class Feedback(models.Model):
    class Rating(models.IntegerChoices):
        ONE = 1, "1"
        TWO = 2, "2"
        THREE = 3, "3"
        FOUR = 4, "4"
        FIVE = 5, "5"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="feedback_entries")
    name = models.CharField(max_length=120)
    email = models.EmailField()
    rating = models.PositiveSmallIntegerField(choices=Rating.choices)
    subject = models.CharField(max_length=160)
    message = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.subject} ({self.rating})"


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=160)
    message = models.TextField()
    link = models.URLField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title


class ActivityLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="activity_logs")
    action = models.CharField(max_length=160)
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.action
