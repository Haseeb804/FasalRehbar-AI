from django.contrib.auth.models import User

from .models import Profile


def ensure_profile(user: User) -> Profile:
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile
