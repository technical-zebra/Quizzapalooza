from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
import six

class QuizTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.register_url = reverse('register')
        self.home_url = reverse('home')

        self.email = 'test@example.com'
        self.password = '!tesTpassword132'
        self.user = User.objects.create_user(username=self.email, email=self.email, password=self.password)

    def test_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        response = self.client.post(self.login_url, {'email': self.email, 'password': self.password})
        self.assertEqual(response.status_code, 302)
        # Redirect after successful login
        self.assertRedirects(response, self.home_url)

        # Add more assertions to test other scenarios (incorrect password, non-existent user)

    def test_logout_view(self):
        self.client.login(username=self.email, password=self.password)
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect


    def test_register_view(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

        response = self.client.post(self.register_url, {'email': 'newuser@example.com', 'password': 'newpassword',
                                                        'confirm_password': 'newpassword'})
        self.assertEqual(response.status_code, 302)
        # Redirect after successful registration
        self.assertRedirects(response, self.home_url)

        # Add more assertions to test other scenarios (existing email, passwords not matching)

    def test_validate_activation(self):
        response = self.client.get(reverse('hello'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Django app is activated!")

    def test_home(self):
        self.client.login(username=self.email, password=self.password)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Welcome')

    def tearDown(self):
        self.user.delete()
