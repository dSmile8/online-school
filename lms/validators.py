from rest_framework.exceptions import ValidationError


class LinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        result = value.get(self.field)
        if result and not result.startswith('https://www.youtube.com'):
            raise ValidationError('Links must be only to "youtube.com" !')
