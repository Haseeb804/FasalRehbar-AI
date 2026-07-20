import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView

from .forms import ImageUploadForm
from .models import Prediction, ScanImage
from .services import get_detection_service

logger = logging.getLogger("pakagri.detection")


@login_required
def detection_index(request):
    """Disease detection upload page."""
    context = {
        "form": ImageUploadForm(),
        "page_title": "Disease Detection",
    }
    return render(request, "detection/index.html", context)


@login_required
def upload_image(request):
    """Handle image upload → run full AI pipeline → redirect to results."""
    if request.method != "POST":
        return redirect("detection:index")

    form = ImageUploadForm(request.POST, request.FILES)
    if not form.is_valid():
        context = {"form": form, "page_title": "Disease Detection"}
        return render(request, "detection/index.html", context)

    scan_image = form.save(commit=False)
    scan_image.user = request.user
    scan_image.save()

    logger.info("User %s uploaded scan %s", request.user.username, scan_image.id)

    service = get_detection_service()
    prediction = service.process_scan(scan_image)

    if prediction:
        messages.success(
            request,
            f"Image analysed successfully! "
            f"Crop: {prediction.crop.name if prediction.crop else 'unknown'} — "
            f"{'Healthy ✓' if prediction.is_healthy else prediction.disease.name if prediction.disease else 'Unknown disease'}."
        )
        return redirect("detection:result", pk=prediction.id)

    # Pipeline failed — give the user a helpful message
    # Clean up the orphaned ScanImage to prevent the DB/dashboard from inflating
    try:
        if scan_image.image:
            scan_image.image.delete(save=False)
        scan_image.delete()
    except Exception:
        logger.exception("Failed to clean up orphaned scan %s", scan_image.id)

    messages.error(
        request,
        "The AI pipeline could not process this image. "
        "Possible reasons: the image is too blurry, not a recognised crop leaf, "
        "or the AI models are still initialising (try again in a moment)."
    )
    logger.error(
        "Pipeline returned None for scan %s (user: %s). Cleaned up DB record.", scan_image.id, request.user.username
    )
    return redirect("detection:index")


@login_required
def detection_result(request, pk):
    """Display prediction results page."""
    prediction = get_object_or_404(Prediction, id=pk, scan_image__user=request.user)
    service = get_detection_service()
    details = service.get_prediction_details(prediction)

    context = {
        "prediction": prediction,
        "details": details,
        "page_title": "Detection Result",
    }
    return render(request, "detection/result.html", context)


@method_decorator(login_required, name="dispatch")
class ScanHistoryListView(ListView):
    """User's full scan history with pagination."""
    model = ScanImage
    template_name = "detection/history_list.html"
    context_object_name = "scans"
    paginate_by = 10

    def get_queryset(self):
        return ScanImage.objects.filter(user=self.request.user).order_by("-uploaded_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Scan History"
        return context


@method_decorator(login_required, name="dispatch")
class PredictionDetailView(DetailView):
    """Detailed view of a single prediction."""
    model = Prediction
    template_name = "detection/prediction_detail.html"
    context_object_name = "prediction"

    def get_queryset(self):
        return Prediction.objects.filter(scan_image__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = get_detection_service()
        context["details"] = service.get_prediction_details(self.object)
        context["page_title"] = "Prediction Details"
        return context
