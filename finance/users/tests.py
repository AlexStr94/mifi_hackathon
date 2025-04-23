from django.test import TestCase
from django.urls import reverse
from .models import User

class UserRegistrationTest(TestCase):
    def test_registration(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'testuser',
            'inn': '1234567890',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())