from datetime import date

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from rest_framework import serializers

from avito.settings import USER_MINIMAL_AGE


class EmailValidator:
    def __init__(self, domains):
        if isinstance(domains, list):
            domains = [domains]

        self.domains = domains

    def __call__(self, email):
        domain = email.split('@')[1]
        if domain in self.domains:
            raise serializers.ValidationError(f'Домен не может быть {domain}')


def age_validator(birth_date: date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if age < USER_MINIMAL_AGE:
        raise ValidationError(f'Пользователь с возрастом меньше {age} не может быть зарегистрирован')

