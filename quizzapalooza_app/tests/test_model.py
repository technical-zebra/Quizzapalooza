from django.test import TestCase
from django.contrib.auth import get_user_model
from quizzapalooza_app.models import Quiz

User = get_user_model()

class QuizModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for the ForeignKey relation
        user = User.objects.create_user(username='testuser', password='testpass')

        # Create a Quiz object for testing
        Quiz.objects.create(
            user=user,
            content='Sample Quiz',
            type='MutiChoices',
            answer_id=1,
            choice_1_content='Choice 1',
            choice_2_content='Choice 2',
            choice_3_content='Choice 3',
            choice_4_content='Choice 4',
        )

    def test_user_field(self):
        quiz = Quiz.objects.get(id=1)
        field = quiz._meta.get_field('user')
        self.assertEqual(field.related_model, User)

    def test_content_field(self):
        quiz = Quiz.objects.get(id=1)
        field = quiz._meta.get_field('content')
        self.assertEqual(field.max_length, 50)

    def test_type_field(self):
        quiz = Quiz.objects.get(id=1)
        field = quiz._meta.get_field('type')
        self.assertEqual(field.max_length, 50)
        self.assertEqual(quiz.get_type_display(), '4 multiple choice mode')

    def test_answer_id_field(self):
        quiz = Quiz.objects.get(id=1)
        field = quiz._meta.get_field('answer_id')
        self.assertEqual(field.get_internal_type(), 'IntegerField')

    def test_choice_1_content_field(self):
        quiz = Quiz.objects.get(id=1)
        field = quiz._meta.get_field('choice_1_content')
        self.assertEqual(field.max_length, 50)

    def test_choice_2_content_field(self):
        quiz = Quiz.objects.get(id=1)
        field = quiz._meta.get_field('choice_2_content')
        self.assertEqual(field.max_length, 50)

    def test_choice_3_content_field(self):
        quiz = Quiz.objects.get(id=1)
        field = quiz._meta.get_field('choice_3_content')
        self.assertEqual(field.max_length, 50)

    def test_choice_4_content_field(self):
        quiz = Quiz.objects.get(id=1)
        field = quiz._meta.get_field('choice_4_content')
        self.assertEqual(field.max_length, 50)