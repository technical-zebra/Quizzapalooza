from django.contrib import messages
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import User
from quizzapalooza_app.auth_controller import login_view, logout_view, register_view

class LoginViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse('login')
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')

    def test_login_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post_valid(self):
        data = {'email': 'test@example.com', 'password': 'testpass'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_login_view_post_invalid_password(self):
        data = {'email': 'test@example.com', 'password': 'wrongpass'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Incorrect password!')

    def test_login_view_post_invalid_user(self):
        data = {'email': 'wrong@example.com', 'password': 'testpass'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'User does not exist!')


class LogoutViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.url = reverse('logout')

    def test_logout_view(self):
        request = self.factory.get(self.url)
        request.user = User.objects.create_user(username='testuser')

        # Add a session to the request
        request.session = self.client.session

        request.client = self.client
        response = logout_view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login')

class RegisterViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse('register')

    def test_register_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_view_post_valid(self):
        data = {'email': 'test@example.com', 'password': 'testpass', 'confirm_password': 'testpass'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_register_view_post_invalid_password(self):
        data = {'email': 'test@example.com', 'password': 'testpass', 'confirm_password': 'wrongpass'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        error_messages = [m.message for m in messages.get_messages(response.wsgi_request) if m.level_tag == 'error']
        self.assertIn('Passwords do not match.', error_messages)




    def test_register_view_post_existing_email(self):
        User.objects.create_user(username='existing', email='test@example.com', password='testpass')
        data = {'email': 'test@example.com', 'password': 'testpass', 'confirm_password': 'testpass'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertContains(response, 'Email already exists')