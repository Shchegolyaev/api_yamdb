from datetime import datetime

from django.core.exceptions import ValidationError


def validate_score(value):
    if value < 1 or value > 10:
        raise ValidationError('Оценка не может быть более 10 или менее 1')


def validate_year(value):
    if value > datetime.now().year:
        raise ValidationError('Год не может быть больше текущего')
