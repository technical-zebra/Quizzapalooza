from django.contrib.auth.models import User
from django.test import TestCase
from ..forms import LoginForm, RegistrationForm, ResetPasswordForm, QuizForm, JoinQuizForm
from ..models import Quiz


class LoginFormTests(TestCase):
    def test_login_form_valid_data(self):
        form_data = {
            'email': 'test@example.com',
            'password': 'password123',
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_missing_email(self):
        form_data = {
            'email': '',
            'password': 'password123',
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_login_form_invalid_email(self):
        form_data = {
            'email': 'invalid_email',
            'password': 'password123',
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_login_form_missing_password(self):
        form_data = {
            'email': 'test@example.com',
            'password': '',
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)


class RegistrationFormTest(TestCase):
    def test_registration_form_valid_data(self):
        form_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration_form_passwords_do_not_match(self):
        form_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'differentpassword',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_registration_form_missing_fields(self):
        form_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': '',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

class ResetPasswordFormTests(TestCase):
    def test_reset_password_form_valid_data(self):
        form_data = {
            'email': 'test@example.com',
            'password': 'new_password',
            'confirm_password': 'new_password',
        }
        form = ResetPasswordForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_reset_password_form_invalid_data(self):
        form_data = {
            'email': 'test@example.com',
            'password': 'new_password',
            'confirm_password': 'different_password',
        }
        form = ResetPasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_reset_password_form_missing_fields(self):
        form_data = {
            'email': 'test@example.com',
        }
        form = ResetPasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_reset_password_form_empty_data(self):
        form_data = {
            'email': '',
            'password': '',
            'confirm_password': '',
        }
        form = ResetPasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_reset_password_form_missing_confirm_password(self):
        form_data = {
            'email': 'test@example.com',
            'password': 'new_password',
            'confirm_password': '',
        }
        form = ResetPasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)



class QuizFormTests(TestCase):
    def test_quiz_form_valid_data(self):
        form_data = {
            'question': 'What is the capital of France?',
            'quiz_mode': 'MutiChoices',
            'choice1': 'Paris',
            'choice2': 'London',
            'choice3': 'Berlin',
            'choice4': 'Rome',
            'answer': 1,
        }
        form = QuizForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_quiz_form_invalid_data(self):
        form_data = {
            'question': 'A',
            'quiz_mode': 'InvalidMode',
            'choice1': 'Choice 1',
            'choice2': 'Choice 2',
            'choice3': 'Choice 3',
            'choice4': 'Choice 4',
            'answer': 5,
        }
        form = QuizForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)  # Expecting 3 validation errors

    # Add more test cases as needed

    def test_quiz_form_save(self):
        form_data = {
            'question': 'What is the capital of France?',
            'quiz_mode': 'MutiChoices',
            'choice1': 'Paris',
            'choice2': 'London',
            'choice3': 'Berlin',
            'choice4': 'Rome',
            'answer': 1,
        }
        form = QuizForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Create a testing user object
        user = User.objects.create(username='testuser@test.com', email='testuser@test.com', password='test123')
        form.save(user)

        # Assert that a new Quiz object was created with the correct data
        new_quiz = Quiz.objects.last()
        self.assertEqual(new_quiz.user, user)
        self.assertEqual(new_quiz.content, 'What is the capital of France?')
        self.assertEqual(new_quiz.type, 'MutiChoices')
        self.assertEqual(new_quiz.answer_id, 1)
        self.assertEqual(new_quiz.choice_1_content, 'Paris')
        self.assertEqual(new_quiz.choice_2_content, 'London')
        self.assertEqual(new_quiz.choice_3_content, 'Berlin')
        self.assertEqual(new_quiz.choice_4_content, 'Rome')

    def tearDown(self):
        Quiz.objects.all().delete()
        User.objects.all().delete()

    class FormTests(TestCase):
        def test_join_quiz_form_valid_data(self):
            form_data = {
                'session_id': 12345,
                'nickname': 'JohnDoe',
            }
            form = JoinQuizForm(data=form_data)
            self.assertTrue(form.is_valid())

        def test_join_quiz_form_invalid_data(self):
            form_data = {
                'session_id': '',
                'nickname': '',
            }
            form = JoinQuizForm(data=form_data)
            self.assertFalse(form.is_valid())
            self.assertEqual(len(form.errors), 2)  # Expecting 2 validation errors

            # Test individual field errors
            self.assertTrue('session_id' in form.errors)
            self.assertTrue('nickname' in form.errors)

        def test_join_quiz_form_missing_session_id(self):
            form_data = {
                'nickname': 'JohnDoe',
            }
            form = JoinQuizForm(data=form_data)
            self.assertFalse(form.is_valid())
            self.assertEqual(len(form.errors), 1)  # Expecting 1 validation error

            # Test individual field error
            self.assertTrue('session_id' in form.errors)

        def test_join_quiz_form_missing_nickname(self):
            form_data = {
                'session_id': 12345,
            }
            form = JoinQuizForm(data=form_data)
            self.assertFalse(form.is_valid())
            self.assertEqual(len(form.errors), 1)  # Expecting 1 validation error

            # Test individual field error
            self.assertTrue('nickname' in form.errors)