from .test_setup import TestSetUp

class TestViews(TestSetUp):
    def test_user_cannot_register_when_no_data(self):
        response = self.client.post(self.register_url)

        self.assertEqual(response.status_code, 400)

    def test_user_can_register_correctly(self):
        response = self.client.post(self.register_url, self.user_data, format='json')


        self.assertIsNotNone(response.data['result'].get('otp_code'), 'OTP code should be generated and returned.')
        self.assertIsNotNone(response.data['result'].get('otp_key'), 'OTP key should be generated and returned.')
        self.assertEqual(response.status_code, 201)

    def test_user_cannot_login_with_unverified(self):
