from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings


# Create your models here.
class Quiz(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    answer_id = models.IntegerField()
    choice_1_content = models.CharField(max_length=50)
    choice_2_content = models.CharField(max_length=50)
    choice_3_content = models.CharField(max_length=50)
    choice_4_content = models.CharField(max_length=50)


class Answer(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user_choice_id = models.IntegerField()
    correctness = models.BooleanField()
