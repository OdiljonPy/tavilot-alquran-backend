from tavilot.models import Post, Category
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse


class TestPostViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.category1 = Category.objects.create(name_uz='Test Category 1')
        self.category2 = Category.objects.create(name_uz='Test Category 2')
        self.post1 = Post.objects.create(title_uz='Test Post 1', category=self.category1, file='picture1.jpg',
                                         description_uz=' Description of Test Post 1', is_published=True, is_premium=False)
        self.post2 = Post.objects.create(title_uz='Test Post 2', category=self.category1, file='picture2.jpg',
                                         description_uz=' Description of Test Post 2', is_published=True, is_premium=False)
        self.post3 = Post.objects.create(title_uz='Test Post 3', category=self.category2, file='picture3.jpg',
                                         description_uz=' Description of Test Post 3', is_published=True, is_premium=False)
        self.post4 = Post.objects.create(title_uz='Test Post 4', category=self.category2, file='picture4.jpg',
                                         description_uz=' Description of Test Post 4', is_published=False,
                                         is_premium=False)

    def test_posts_list(self):
        response = self.client.get(reverse('posts', kwargs={'pk': self.category1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['result']), 2)
        self.assertEqual(response.data['result'][0]['title'], 'Test Post 2')
        self.assertNotEqual(response.data['result'][1]['title'], 'Test Post 3')

    def test_posts_detail(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result']['title'], 'Test Post 1')
        self.post1.delete()
        response2 = self.client.get(reverse('post_detail', kwargs={'pk': 1}))
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)
