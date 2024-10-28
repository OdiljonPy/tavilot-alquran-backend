from tavilot.models import Chapter
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status


class TestChapterViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.chapter = Chapter.objects.create(name="Test Chapter", description="Description of Test Chapter")

    def test_get_chapters(self):
        response = self.client.get(reverse('chapters'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'][0]['name'], 'Test Chapter')
        self.assertEqual(response.data['result'][0]['description'], 'Description of Test Chapter')
        self.assertNotEqual(len(response.data['result']), 2)
