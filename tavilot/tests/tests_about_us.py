from tavilot.models import AboutUs
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse

class TestsAboutUsViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.about_us1 = AboutUs.objects.create(description_uz='Description of about us 1')
        self.about_us2 = AboutUs.objects.create(description_uz='Description of about us 2')

    def test_get_about_us(self):
        response = self.client.get(reverse('about_us'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result']['description'], 'Description of about us 2')