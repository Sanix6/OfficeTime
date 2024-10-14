from django.db import models
from user.models import User
from helpers.choices import TYPE_CHOICES


class Visit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visits')
    data = models.DateField('Дата')
    time = models.TimeField('Время')
    status = models.CharField('Статус', max_length=255)
    lat_a = models.CharField("Широта А", max_length=255)
    lon_a = models.CharField("Долгота А", max_length=255)
    lat_b = models.CharField("Широта Б", max_length=255, blank=True, null=True)
    lon_b = models.CharField("Долгота Б", max_length=255, blank=True, null=True)
    is_active = models.BooleanField('Активность', default=False)
    

    class Meta:
        verbose_name = ''
        verbose_name_plural = 'Поcещаемость'


class Salary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    salary = models.IntegerField('Зарплата')
    type = models.CharField('Вид зарплаты', max_length=255, choices=TYPE_CHOICES)
    date = models.DateField('Когда')

    class Meta:
        verbose_name = ''
        verbose_name_plural = 'Зарплата'