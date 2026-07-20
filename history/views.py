import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, UpdateView

from detection.models import Prediction, ScanImage
from .forms import PredictionFilterForm, PredictionHistoryForm
from .models import PredictionHistory

logger = logging.getLogger("pakagri.history")


# ─────────────────────────────────────────────────────────────────────────────
# Helper: ensure every Prediction the user owns has a PredictionHistory row.
# Called lazily on the list view so older scans (created before the auto-create
# was added to services.py) still appear in the history list.
# ─────────────────────────────────────────────────────────────────────────────

def _sync_history_for_user(user):
    """Back-fill PredictionHistory rows for any Prediction that is missing one."""
    predictions_without_history = Prediction.objects.filter(
        scan_image__user=user
    ).exclude(
        id__in=PredictionHistory.objects.filter(user=user).values_list("prediction_id", flat=True)
    )
    for pred in predictions_without_history:
        try:
            PredictionHistory.objects.get_or_create(
                prediction=pred,
                defaults={"user": user},
            )
        except Exception:
            logger.exception("Back-fill failed for prediction %s", pred.id)


# ─────────────────────────────────────────────────────────────────────────────
# List view
# ─────────────────────────────────────────────────────────────────────────────

@method_decorator(login_required, name="dispatch")
class HistoryListView(ListView):
    """Display all scan history for the logged-in user."""
    model = PredictionHistory
    template_name = "history/list.html"
    context_object_name = "histories"
    paginate_by = 12

    def get_queryset(self):
        # Back-fill any predictions that don't yet have a PredictionHistory row
        _sync_history_for_user(self.request.user)

        queryset = PredictionHistory.objects.filter(
            user=self.request.user,
            is_archived=False,
        ).select_related(
            "prediction__crop",
            "prediction__disease",
            "prediction__scan_image",
        )

        # Filters
        disease = self.request.GET.get("disease", "").strip()
        if disease:
            queryset = queryset.filter(prediction__disease__name__icontains=disease)

        crop = self.request.GET.get("crop", "").strip()
        if crop:
            queryset = queryset.filter(prediction__crop__name__icontains=crop)

        confidence = self.request.GET.get("confidence", "").strip()
        if confidence:
            queryset = queryset.filter(prediction__confidence_level=confidence)

        search = self.request.GET.get("search", "").strip()
        if search:
            queryset = queryset.filter(
                Q(tags__icontains=search) | Q(notes__icontains=search)
            )

        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Scan History"
        context["filter_form"] = PredictionFilterForm(self.request.GET)
        context["total_count"] = PredictionHistory.objects.filter(
            user=self.request.user, is_archived=False
        ).count()
        return context


# ─────────────────────────────────────────────────────────────────────────────
# Detail view
# ─────────────────────────────────────────────────────────────────────────────

@method_decorator(login_required, name="dispatch")
class HistoryDetailView(DetailView):
    model = PredictionHistory
    template_name = "history/detail.html"
    context_object_name = "history"

    def get_queryset(self):
        return PredictionHistory.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Scan Detail"
        return context


# ─────────────────────────────────────────────────────────────────────────────
# Edit view (notes / tags)
# ─────────────────────────────────────────────────────────────────────────────

@method_decorator(login_required, name="dispatch")
class HistoryUpdateView(UpdateView):
    model = PredictionHistory
    form_class = PredictionHistoryForm
    template_name = "history/form.html"
    success_url = reverse_lazy("history:list")

    def get_queryset(self):
        return PredictionHistory.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Notes updated successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Edit Notes"
        return context


# ─────────────────────────────────────────────────────────────────────────────
# Delete view
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def history_delete(request, pk):
    """
    Delete a history record and ALL related data:
      PredictionHistory → Recommendation → Prediction → ScanImage (DB + file)

    The physical file deletion is intentionally isolated in its own try/except
    so a missing file never blocks the database cleanup.
    """
    history = get_object_or_404(PredictionHistory, pk=pk, user=request.user)
    if request.method == "POST":
        # Grab references BEFORE any deletion
        prediction = history.prediction
        scan_image = prediction.scan_image
        image_file = scan_image.image  # keep a reference to delete the file later

        # 1. Delete recommendation (if exists) – avoids FK constraint errors
        try:
            if hasattr(prediction, "recommendation"):
                prediction.recommendation.delete()
        except Exception:
            logger.exception("Could not delete recommendation for prediction %s", prediction.id)

        # 2. Delete history row
        history.delete()

        # 3. Delete prediction (cascades any remaining related rows)
        prediction.delete()

        # 4. Delete ScanImage DB record — ALWAYS, regardless of file status
        scan_image.delete()

        # 5. Delete the physical image file (best-effort — never blocks)
        try:
            if image_file and image_file.name:
                image_file.delete(save=False)
        except Exception:
            logger.warning(
                "Physical file deletion failed for scan %s — DB records already removed.",
                scan_image.id,
            )

        messages.success(request, "Scan record and all related data deleted successfully.")
    return redirect("history:list")



# ─────────────────────────────────────────────────────────────────────────────
# Archive view
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def history_archive(request, pk):
    """Archive (soft-hide) a history entry."""
    history = get_object_or_404(PredictionHistory, pk=pk, user=request.user)
    history.is_archived = True
    history.save()
    messages.success(request, "Scan archived successfully.")
    return redirect("history:list")


# ─────────────────────────────────────────────────────────────────────────────
# Export (placeholder)
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def export_report(request, pk):
    history = get_object_or_404(PredictionHistory, pk=pk, user=request.user)
    messages.info(request, "Report export feature coming soon!")
    return redirect("history:detail", pk=history.pk)
