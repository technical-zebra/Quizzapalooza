from django.urls import path
from . import quiz_controller as quiz, auth_controller as auth

urlpatterns = [
    path('hello/', quiz.validate_activation, name='hello'),
    path('', quiz.home, name='home'),
    path('login/', auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),
    path('register/', auth.register_view, name='register'),
    path('create_quiz/', quiz.create_quiz, name='create_quiz'),
    path('display_quiz/', quiz.display_quiz, name='display_quiz'),
    path('run_quiz/', quiz.run_quiz, name='run_quiz'),
    path('leaderboard/', quiz.get_leaderboard, name='leaderboard'),
    path('send_answer/', quiz.send_answer, name='send_answer'),
    path('delete_quiz/', quiz.delete_quiz, name='delete_quiz'),
    path('start_session/<int:session_id>/<str:nickname>/', quiz.start_session, name='start_session_with_nickname'),
    path('start_session/<int:session_id>/', quiz.start_session, name='start_session'),
    path('quiz_session/<int:session_id>/<int:qid>/', quiz.start_quiz, name='run_test'),
    path('join_quiz/', quiz.join_quiz, name='join_quiz')
]
