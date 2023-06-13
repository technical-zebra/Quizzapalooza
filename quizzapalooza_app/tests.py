from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.urls import path, re_path
from django.urls import reverse
import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from quizzapalooza_app.models import Quiz
from quizzapalooza_app.consumers import QuizConsumer
from quizzapalooza_app.quiz_controller import get_students_scores


class QuizTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.register_url = reverse('register')
        self.home_url = reverse('home')
        self.email = 'test@example.com'
        self.password = '!tesTpassword132'
        self.teacher = User.objects.create_user(username=self.email, email=self.email, password=self.password)
        self.quiz = Quiz.objects.create(user=self.teacher,
            content="What is this song?",
            type="MutiChoices",
            answer_id=1,
            choice_1_content="Hello",
            choice_2_content="Someone Like You",
            choice_3_content="Beat it",
            choice_4_content="Smooth Criminal")




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

    def test_delete_quiz_not_found(self):
        self.client.force_login(self.teacher)
        quiz_id = 999
        response = self.client.post(reverse('delete_quiz'), {'quizId': quiz_id}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'error')
        self.assertEqual(response.json()['message'], 'Quiz not found')

    def test_delete_quiz_invalid_method(self):
        self.client.force_login(self.teacher)
        response = self.client.get(reverse('delete_quiz'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'error')
        self.assertEqual(response.json()['message'], 'Invalid request method')

    def tearDown(self):
        self.teacher.delete()
