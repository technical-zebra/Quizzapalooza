from django.urls import path
from . import quiz_controller as quiz, auth_controller as auth

urlpatterns = [
    path('hello/', quiz.validate_activation),
    path('', quiz.home, name='home'),
    path('login/', auth.login_view),
    path('logout/', auth.logout_view),
    path('register/', auth.register_view),
    path('create_quiz/', quiz.create_quiz, name='create_quiz'),
    path('display_quiz/', quiz.display_quiz, name='display_quiz'),
    path('run_quiz/', quiz.run_quiz, name='run_quiz'),
    path('leaderboard/', quiz.get_leaderboard, name='leaderboard'),
    path('send-answer/', quiz.send_answer, name='send_answer'),
    path('delete-quiz/', quiz.delete_quiz, name='delete_quiz'),
    path('start_session/<int:session_id>/', quiz.start_session, name='start_session'),
    path('run_test/<int:qid>/', quiz.run_test, name='run_test'),
]
