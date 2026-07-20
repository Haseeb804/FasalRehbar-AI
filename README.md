# FasalRehbar AI
**Live Website:** [https://fasalrehbar-ai.onrender.com](https://fasalrehbar-ai.onrender.com)

FasalRehbar AI is a production-ready agricultural disease detection platform built with Django, Django REST Framework, Bootstrap 5, and a service-oriented architecture designed for future AI model integration.

## Features

- Premium SaaS-style UI with a responsive green design system
- Django authentication with registration, login, profile, password reset, and verification-ready workflows
- Crop and disease catalogues with normalized models
- Placeholder disease detection pipeline ready for EfficientNet-B0 or YOLOv8 integration
- Dashboard, history, feedback, FAQ, contact, privacy policy, and terms pages
- REST API endpoints for crops, diseases, detections, recommendations, and messages
- PostgreSQL-ready settings with SQLite fallback for development
- Docker, Gunicorn, and Nginx deployment support

## Local development

1. Create a virtual environment and install dependencies from `requirements.txt`.
2. Copy `.env.example` to `.env` and adjust values.
3. Run database migrations.
4. Create a superuser.
5. Start the development server.

## Environment

Key environment variables:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DATABASE_URL`
- `EMAIL_BACKEND`

## Deployment

The repository includes Docker and Nginx-ready configuration so you can deploy with Gunicorn behind a reverse proxy.
