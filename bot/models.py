
from django.db import models


class Config(models.Model):
    main_chanel = models.CharField(max_length=200, null=True)
    chat_chanel = models.CharField(max_length=200, null=True)
    admins = models.TextField(null=True, default='')
    bot_token = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.main_chanel


class Stages(models.Model):
    current_stage = models.CharField(max_length=50, null=True)
    nex_stage = models.CharField(max_length=50, null=True)


class Users(models.Model):
    STATUSES =[
        ('user', 'Пользователь'),
        ('admin', 'Администратор')
    ]

    chat_id = models.IntegerField()
    username = models.CharField(max_length=200, null=True, default='')
    status = models.CharField(max_length=20, choices=STATUSES, default='user')
    in_chanel = models.BooleanField(default=False)
    interaction = models.BooleanField(default=False)

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

