from django.db import models as pg_models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings


class Quiz(pg_models.Model):
    USER_CHOICES = [
        ("MutiChoices", "4 multiple choice mode"),
        ("TrueOrFalse", "True or False mode"),
    ]

    user = pg_models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=pg_models.CASCADE)
    content = pg_models.CharField(max_length=50)
    type = pg_models.CharField(max_length=50, choices=USER_CHOICES)
    answer_id = pg_models.IntegerField()
    choice_1_content = pg_models.CharField(max_length=50)
    choice_2_content = pg_models.CharField(max_length=50)
    choice_3_content = pg_models.CharField(max_length=50)
    choice_4_content = pg_models.CharField(max_length=50)




