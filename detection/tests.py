from django.test import TestCase
from django.contrib.auth.models import User
from .models import Disease, Crop, ScanImage, Prediction


class DiseaseModelTest(TestCase):
    def setUp(self):
        self.disease = Disease.objects.create(
            name="Leaf Blight",
            scientific_name="Magnaporthe oryzae",
            description="Fungal disease affecting rice",
            symptoms="Brown spots on leaves",
            prevention="Proper drainage",
            treatment="Fungicide application",
            affected_crops="Rice"
        )

    def test_disease_creation(self):
        self.assertEqual(self.disease.name, "Leaf Blight")
        self.assertTrue(self.disease.is_active)


class CropModelTest(TestCase):
    def setUp(self):
        self.crop = Crop.objects.create(
            name="Rice",
            scientific_name="Oryza sativa",
            description="Staple crop"
        )

    def test_crop_creation(self):
        self.assertEqual(self.crop.name, "Rice")
        self.assertTrue(self.crop.is_active)


class ScanImageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    def test_scan_image_creation(self):
        # Test would require actual image file
        pass
