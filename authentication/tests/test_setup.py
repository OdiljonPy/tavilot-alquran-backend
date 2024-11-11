from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
import random
import uuid

from ..models import OTP, User


class TestSetUp(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.verify_url = reverse('verify')
        self.login_url = reverse('login')

        self.user_data = {
            'phone_number': '+998933787766',
            'password': '1221'
        }

        self.user_not_valid_data ={
            'phone_number': '+998933787777',
            'password': '1221'
        }

        self.otp_data = {
            'otp_code' : str(random.randint(100000, 999999)),
            'otp_key' : uuid.uuid4()
        }

        self.user = User.objects.create(phone_number=self.user_data['phone_number'], password=self.user_data['password'])

        self.otp = OTP.objects.create(user=self.user, otp_code=self.otp_data['otp_code'], otp_key=self.otp_data['otp_key'])

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
