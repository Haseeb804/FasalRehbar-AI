from django.contrib.auth.models import User
from django.test import TestCase

from .models import Profile


class ProfileModelTests(TestCase):
    def test_profile_created_for_user(self):
        user = User.objects.create_user(username="farmer", password="StrongPass123!")
        self.assertTrue(Profile.objects.filter(user=user).exists())
