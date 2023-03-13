from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(year):
    if datetime.now().year < year < 1895:
        raise ValidationError(
            'Год не может быть меньше 1895 и больше нынешнего'
        )
