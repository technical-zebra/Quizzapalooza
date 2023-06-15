from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse, resolve
from ..quiz_controller import (
    validate_activation,
    home,
    create_quiz,
    display_quiz,
    run_quiz,
    show_leaderboard,
    delete_quiz,
    start_session,
    start_quiz,
    join_quiz,
)
from ..auth_controller import login_view, logout_view, register_view


class UrlTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_hello_url_resolves(self):
        url = reverse('hello')
        self.assertEqual(resolve(url).func, validate_activation)

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, home)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, login_view)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, logout_view)

    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, register_view)

    def test_create_quiz_url_resolves(self):
        url = reverse('create_quiz')
        self.assertEqual(resolve(url).func, create_quiz)

    def test_display_quiz_url_resolves(self):
        url = reverse('display_quiz')
        self.assertEqual(resolve(url).func, display_quiz)

    def test_run_quiz_url_resolves(self):
        url = reverse('run_quiz')
        self.assertEqual(resolve(url).func, run_quiz)

    def test_show_leaderboard_url_resolves(self):
        url = reverse('show_leaderboard', args=[12345])
        self.assertEqual(resolve(url).func, show_leaderboard)

    def test_delete_quiz_url_resolves(self):
        url = reverse('delete_quiz')
        self.assertEqual(resolve(url).func, delete_quiz)

    def test_start_session_with_nickname_url_resolves(self):
        url = reverse('start_session_with_nickname', args=[12345, 'john'])
        self.assertEqual(resolve(url).func, start_session)

    def test_start_session_url_resolves(self):
        url = reverse('start_session', args=[12345])
        self.assertEqual(resolve(url).func, start_session)

    def test_start_quiz_url_resolves(self):
        # Define the URL path
        session_id = 12345
        qid = 1
        nickname = 'john'
        url = reverse('start_quiz', args=[session_id, qid, nickname])

        # Resolve the URL path and compare the resolved view function
        resolved_func = resolve(url).func
        self.assertEqual(resolved_func, start_quiz)

    def test_join_quiz_url_resolves(self):
        url = reverse('join_quiz')
        self.assertEqual(resolve(url).func, join_quiz)
