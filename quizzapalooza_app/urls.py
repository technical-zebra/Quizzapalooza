from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.validate_activation),
    path('', views.home, name='home'),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('register/', views.register_view),
    path('go/', views.go, name='go'),
    path('create_quiz/', views.create_quiz, name='create_quiz'),
    path('display_quiz/', views.display_quiz, name='display_quiz'),
    path('run_quiz/', views.run_quiz, name='run_quiz'),
    path('leaderboard/', views.get_leaderboard, name='leaderboard'),
    path('send-answer/', views.send_answer, name='send_answer'),
    path('delete-quiz/', views.delete_quiz, name='delete_quiz'),
    path('start_session/<int:session_id>/', views.start_session, name='start_session'),
    path('run_test/<int:qid>/', views.run_test, name='run_test'),
]
