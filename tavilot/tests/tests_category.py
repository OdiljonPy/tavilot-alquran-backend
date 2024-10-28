from tavilot.models import Category
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse


class TestCategoryViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.category1 = Category.objects.create(name='Category 1')
        self.category2 = Category.objects.create(name='Category 2')
        self.category3 = Category.objects.create(name='Category 3')

    def test_category_list(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'][0]['name'], 'Category 3')
        self.assertEqual(response.data['result'][1]['name'], 'Category 2')
        self.assertNotEqual(len(response.data['result']), 2)
