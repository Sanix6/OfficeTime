# Generated by Django 5.0.3 on 2024-10-11 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_remove_user_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='salary',
            field=models.IntegerField(default=1, verbose_name='Зарплата'),
            preserve_default=False,
        ),
    ]