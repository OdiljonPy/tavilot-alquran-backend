from datetime import datetime

from tavilot.models import Chapter, Verse, Audio, Sheikh
from authentication.models import User
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status


class TestChapterViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.chapter1 = Chapter.objects.create(name_uz="Test Chapter 1", description_uz="Description of Test Chapter 1")
        self.verse1 = Verse.objects.create(chapter=self.chapter1, number=1, text_uz="Test Verse 1",
                                           text_arabic="Test Verse Arabic 1", description_uz="Description of Test Verse 1")
        self.verse2 = Verse.objects.create(chapter=self.chapter1, number=2, text_uz="Test Verse 2",
                                           text_arabic="Test Verse Arabic 2", description_uz="Description of Test Verse 2")
        self.sheikh1 = Sheikh.objects.create(name_uz="Test Sheikh 1")
        self.audio1 = Audio.objects.create(chapter=self.chapter1, verse=self.verse1, sheikh=self.sheikh1,
                                           audio="audio_test1.mp3", audio_translate_uz="audio_translate1.mp3")
        self.audio2 = Audio.objects.create(chapter=self.chapter1, verse=self.verse2, sheikh=self.sheikh1,
                                           audio="audio_test2.mp3", audio_translate_uz="audio_translate2.mp3")

    def test_get_chapters(self):
        response = self.client.get(reverse('chapters'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'][0]['name'], 'Test Chapter 1')
        self.assertEqual(response.data['result'][0]['description'], 'Description of Test Chapter 1')
        self.assertNotEqual(len(response.data['result']), 2)


    def test_get_chapter_with_verses_without_description(self):
        response = self.client.get(reverse('chapter_detail_translated_verses', kwargs={'pk': self.chapter1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result']['name'], 'Test Chapter 1')
        self.assertEqual(response.data['result']['verses'][0]['text'], 'Test Verse 2')
        self.assertEqual(response.data['result']['verses'][1]['audios'][0]['audio'],
                         'http://testserver/media/audio_test1.mp3')
        self.assertEqual(response.data['result']['verses'][0].get('description'), None)


    def test_get_chapter_full(self):
        response = self.client.get(reverse('chapter_detail', kwargs={'pk': self.chapter1.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # TODO test for user with rate 1 and 2
