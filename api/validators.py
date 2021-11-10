import datetime
from django.core.exceptions import ValidationError


def validate_year(value):
    year_date = datetime.date.today().year
    if not 0 < value <= year_date:
        raise ValidationError('Введите корректный год')
    return value
