# Generated by Django 5.0.1 on 2024-01-28 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_users_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Welcome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('types', models.CharField(choices=[('text', 'Текст'), ('photo', 'Фото')], default='text', max_length=30)),
            ],
        ),
    ]