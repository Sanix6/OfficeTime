# Generated by Django 5.0.3 on 2024-10-11 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.IntegerField(unique=True, verbose_name='Номер телефона '),
        ),
    ]
