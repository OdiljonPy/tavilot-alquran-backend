from .test_setup import TestSetUp


class TestViews(TestSetUp):
    def test_user_cannot_register_when_no_data(self):
        response = self.client.post(self.register_url)

        self.assertEqual(response.status_code, 400)

    def test_user_can_register_correctly(self):
        res = self.client.post(self.register_url, self.user_data, format='json')

        self.assertIsNotNone(res.data['result'].get('otp_code'), 'OTP code should be generated and returned.')
        self.assertIsNotNone(res.data['result'].get('otp_key'), 'OTP key should be generated and returned.')
        self.assertEqual(res.status_code, 201)

    def test_user_cannot_verify_without_otp(self):
        res = self.client.post(self.verify_url)

        self.assertEqual(res.status_code, 400)

    def test_user_can_verify_with_otp(self):
        res = self.client.post(self.verify_url, self.otp_data, format='json')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data.get('ok'), True)

    def test_user_cannot_login_with_not_valid_data(self):
        res = self.client.post(self.login_url, self.user_not_valid_data, format='json')
        print(res.data)
        print(res.status_code)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data.get('ok'), False)
