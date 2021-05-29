from datetime import datetime as date

from django.core.exceptions import ValidationError


def not_from_the_future(year):
    if year > date.now().year:
        raise ValidationError(
            'You can\'t post titles from future!',
            params={'year': year}
        )
