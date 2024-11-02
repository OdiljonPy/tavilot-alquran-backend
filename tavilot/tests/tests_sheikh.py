from tavilot.models import Sheikh, Audio, Verse, Chapter
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse

class TestsSheikhViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.chapter1 = Chapter.objects.create(name_uz="Test Chapter 1", description_uz="Description of Test Chapter 1")
        self.sheikh1 = Sheikh.objects.create(name_uz="Sheikh1")
        self.sheikh2 = Sheikh.objects.create(name_uz="Sheikh2")
        self.verse1 = Verse.objects.create(chapter=self.chapter1, number=1, text_uz="Test Verse 1",
                                           text_arabic="Test Verse Arabic 1",
                                           description_uz="Description of Test Verse 1")
        self.verse2 = Verse.objects.create(chapter=self.chapter1, number=2, text_uz="Test Verse 2",
                                           text_arabic="Test Verse Arabic 2",
                                           description_uz="Description of Test Verse 2")
        self.audio1 = Audio.objects.create(chapter=self.chapter1, verse=self.verse1, sheikh=self.sheikh1,
                                           audio="audio_test1.mp3", audio_translate_uz="audio_translate1.mp3")
        self.audio2 = Audio.objects.create(chapter=self.chapter1, verse=self.verse2, sheikh=self.sheikh1,
                                           audio="audio_test2.mp3", audio_translate_uz="audio_translate2.mp3")

    def test_sheikh_get(self):
        response = self.client.get(reverse('sheikhs'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'][0]['name'], 'Sheikh2')
        self.assertEqual(len(response.data['result']), 2)

    def test_sheikh_audio(self):
        response = self.client.get(reverse('sheikh_audio', kwargs={'pk': self.sheikh1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['result']), 2)
        self.assertEqual(response.data['result'][0]['audio_translate'], 'audio_translate2.mp3')
        response = self.client.get(reverse('sheikh_audio', kwargs={'pk': self.sheikh2.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(len(response.data['result']), 2)
