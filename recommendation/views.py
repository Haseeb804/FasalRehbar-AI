from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DetailView, CreateView
from django.utils.decorators import method_decorator
from django.utils import translation
from django.urls import reverse_lazy

from detection.models import Prediction
from detection.services import DetectionService
from .models import Recommendation, UserFeedback
from .forms import FeedbackForm
from .rag import generate_recommendation


@login_required
def recommendation_detail(request, prediction_id):
    """Display RAG-generated bilingual recommendations for a prediction"""
    prediction = get_object_or_404(Prediction, id=prediction_id, scan_image__user=request.user)

    # Get or create recommendation (KB fallback fields kept for the admin/legacy views)
    recommendation, created = Recommendation.objects.get_or_create(
        prediction=prediction,
        defaults={
            "disease": prediction.disease,
            "treatment_steps": prediction.disease.treatment if prediction.disease else "Keep plant healthy",
            "prevention_steps": prediction.disease.prevention if prediction.disease else "Monitor regularly",
            "urgency": "urgent" if prediction.confidence_level == "high" else "normal",
        }
    )

    ai_content = generate_recommendation(recommendation)
    current_lang = translation.get_language() or "en"
    is_urdu = current_lang.startswith("ur")
    en_advice = ai_content.get("en") or {}
    ur_advice = ai_content.get("ur") or {}

    # Get user feedback if exists
    user_feedback = UserFeedback.objects.filter(
        recommendation=recommendation,
        user=request.user
    ).first()

    context = {
        "prediction": prediction,
        "recommendation": recommendation,
        "ai_content": ai_content,
        "en_advice": en_advice,
        "ur_advice": ur_advice,
        "is_urdu": is_urdu,
        "current_lang": "ur" if is_urdu else "en",
        "user_feedback": user_feedback,
        "page_title": "Recommendations",
    }
    return render(request, "recommendation/detail.html", context)


@login_required
def submit_feedback(request, recommendation_id):
    """Submit feedback on recommendation"""
    recommendation = get_object_or_404(
        Recommendation,
        id=recommendation_id,
        prediction__scan_image__user=request.user
    )
    
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.recommendation = recommendation
            feedback.user = request.user
            
            # Update or create feedback
            UserFeedback.objects.update_or_create(
                recommendation=recommendation,
                user=request.user,
                defaults={
                    "feedback_type": feedback.feedback_type,
                    "rating": feedback.rating,
                    "comment": feedback.comment,
                }
            )
            
            messages.success(request, "Thank you for your feedback!")
            return redirect("recommendation:detail", prediction_id=recommendation.prediction.id)
    else:
        form = FeedbackForm()
    
    context = {
        "form": form,
        "recommendation": recommendation,
        "page_title": "Submit Feedback",
    }
    return render(request, "recommendation/feedback_form.html", context)
