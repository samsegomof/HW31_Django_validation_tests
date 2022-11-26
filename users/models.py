from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import age_validator, EmailValidator


class Location(models.Model):
    class Meta:
        verbose_name = "Местоположение"
        verbose_name_plural = "Местоположения"

    name = models.CharField(verbose_name="Местоположение", max_length=100)
    lat = models.DecimalField(verbose_name="Широта", max_digits=15, decimal_places=10, null=True)
    lng = models.DecimalField(verbose_name="Долгота", max_digits=15, decimal_places=10, null=True)

    def __str__(self):
        return self.name


class UserRoles:
    USER = "member"
    ADMIN = "admin"
    MODERATOR = "moderator"
    choices = [
        (USER, "Пользователь"),
        (ADMIN, "Администратор"),
        (MODERATOR, "Модератор")
    ]


class User(AbstractUser):
    role = models.CharField(verbose_name="Группа", choices=UserRoles.choices, default="member", max_length=16)
    age = models.PositiveIntegerField(verbose_name="Возраст", null=True)
    location = models.ManyToManyField(Location)
    birth_date = models.DateField(verbose_name="Дата рождения", null=True, max_length=10, validators=[age_validator])
    email = models.EmailField(verbose_name="Электронный адрес", null=False, unique=True, validators=[EmailValidator])

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


