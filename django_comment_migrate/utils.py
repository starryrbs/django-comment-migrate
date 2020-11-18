from django.db.models import Field


def get_field_comment(field: Field):
    if field.help_text:
        return str(field.help_text)
