# Generated by Django 5.0.3 on 2024-10-11 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_user_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='salary',
        ),
        migrations.RemoveField(
            model_name='user',
            name='type',
        ),
    ]
