from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Quiz
import json

class DeleteQuizViewTest(TestCase):
    def setUp(self):
        self.url = reverse('delete_quiz')
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.quiz = Quiz.objects.create(
            content='What is the capital of France?',
            type='MutiChoices',
            choice_1_content='Paris',
            choice_2_content='London',
            choice_3_content='Berlin',
            choice_4_content='Rome',
            answer_id=1,
            user_id=self.user.pk
        )

    def test_delete_quiz(self):
        quiz_id = self.quiz.pk
        data = {'quizId': quiz_id}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success', 'redirectUrl': '/display_quiz/'})
        self.assertFalse(Quiz.objects.filter(pk=quiz_id).exists())

    def test_delete_quiz_invalid_quiz_id(self):
        quiz_id = 123456
        data = {'quizId': quiz_id}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'error', 'message': 'Quiz not found'})
        self.assertTrue(Quiz.objects.filter(pk=self.quiz.pk).exists())

    def test_delete_quiz_invalid_method(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'error', 'message': 'Invalid request method'})
        self.assertTrue(Quiz.objects.filter(pk=self.quiz.pk).exists())
