from django.db import models


class Visit(models.Model):
    data = models.DateField('Дата')
    time = models.TimeField('Время')
    status = models.CharField('Статус', max_length=255)
    lat_a = models.CharField("Широта А", max_length=255)
    lon_a = models.CharField("Долгота А", max_length=255)
    lat_b = models.CharField("Широта Б", max_length=255, blank=True, null=True)
    lon_b = models.CharField("Долгота Б", max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = ''
        verbose_name_plural = 'Поcещаемость'
