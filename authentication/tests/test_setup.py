from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from ..models import OTP, User


class TestSetUp(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')

        self.user_data = {
            'phone_number': '+998933787766',
            'password': '1221'
        }

        self.user = User.objects.create(phone_number=self.user_data['phone_number'], password=self.user_data['password'])

        self.otp = OTP.objects.create(user=self.user)

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
