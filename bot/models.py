
from django.db import models


class Stages(models.Model):
    current_stage = models.CharField(max_length=50, null=True)
    nex_stage = models.CharField(max_length=50, null=True)


class Users(models.Model):
    STATUSES =[
        ('user', 'Пользователь'),
        ('admin', 'Администратор')
    ]

    chat_id = models.IntegerField()
    username = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUSES, default='user')

    def __str__(self):
        return self.username


class Welcome(models.Model):
    TYPES = [
        ('text', 'Текст'),
        ('photo', 'Фото')
    ]

    type = models.CharField(max_length=30, choices=TYPES, default='text')
    text = models.TextField(null=True)

    def __str__(self):
        return self.type

