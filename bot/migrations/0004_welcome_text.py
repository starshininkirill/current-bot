# Generated by Django 5.0.1 on 2024-01-28 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_welcome'),
    ]

    operations = [
        migrations.AddField(
            model_name='welcome',
            name='text',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
