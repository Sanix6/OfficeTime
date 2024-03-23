import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from .choices import USER_STATUS
from .manager import CustomUserManager


class User(AbstractUser):
    username = None
    user = models.CharField("Тип пользователя", choices=USER_STATUS, max_length=250, blank=True, null=True)
    phone = models.IntegerField('Номер телефона ', unique=True)
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    is_active = models.BooleanField('Активный', default=False)
    code = models.IntegerField("Код активации", null=True, blank=True)

    def __str__(self):
        return self.first_name

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        self.code = int(random.randint(100_000, 999_999))
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
