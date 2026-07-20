"""
Email utility functions.
"""

from django.core.mail import send_mail
from django.conf import settings


def send_welcome_email(user_email, user_name):
    """Send welcome email to new user"""
    subject = "Welcome to PakAgri - Agricultural Disease Detection"
    message = f"""
    Dear {user_name},

    Welcome to PakAgri! We're excited to have you on board.

    You can now upload images of your crops to detect diseases and get recommendations.

    Get started: https://your-domain.com/detection/

    Best regards,
    PakAgri Team
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])


def send_prediction_notification(user_email, user_name, prediction_details):
    """Send prediction result notification"""
    subject = "Your Disease Detection Result - PakAgri"
    message = f"""
    Dear {user_name},

    Your prediction analysis is complete!

    Crop: {prediction_details.get('crop')}
    Result: {prediction_details.get('disease')}
    Confidence: {prediction_details.get('confidence_score')}%

    View full details: https://your-domain.com/detection/result/{prediction_details.get('prediction_id')}/

    Best regards,
    PakAgri Team
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
