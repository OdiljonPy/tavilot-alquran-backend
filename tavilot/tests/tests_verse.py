from tavilot.models import Verse, Chapter
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse


class TestVerseViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.chapter = Chapter.objects.create(name='Test Chapter', description='Description of Test Chapter')
        self.verse1 = Verse.objects.create(chapter=self.chapter, number=1, description='Description of Test Verse 1',
                                           text='Text of Verse 1', text_arabic='Arabic Text of Verse 1')
        self.verse2 = Verse.objects.create(chapter=self.chapter, number=2, description='Description of Test Verse 2',
                                           text='Text of Verse 2', text_arabic='Arabic Text of Verse 2')

    def test_verse_list(self):
        response = self.client.get(reverse('verses', args=[self.chapter.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result']['content'][0]['text'], 'Text of Verse 2')
        self.assertEqual(response.data['result']['content'][0]['number'], 2)
        self.assertNotEqual(response.data['result']['content'][0]['id'], 1)

    def test_verse_detail(self):
        response = self.client.get(reverse('verse_detail', args=[self.verse1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result']['text'], 'Text of Verse 1')
        self.assertEqual(response.data['result']['number'], 1)
        self.assertNotEqual(response.data['result']['id'], 2)
