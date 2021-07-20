from django.db import router, DEFAULT_DB_ALIAS
from django.db.migrations import Migration
from django.db.models import Field


def get_field_comment(field: Field):
    if field.help_text:
        return str(field.help_text)


def get_migrations_app_models(migrations: [Migration], apps, using=DEFAULT_DB_ALIAS) -> set:
    models = set()
    for migration in migrations:
        if not isinstance(migration, Migration):
            continue
        app_label = migration.app_label
        if not router.allow_migrate(using, app_label):
            continue
        operations = getattr(migration, 'operations', [])
        for operation in operations:
            model_name = getattr(operation, 'model_name', None) or getattr(operation, 'name', None)
            if model_name is None:
                continue
            model = apps.get_model(app_label, model_name=model_name)
            models.add(model)
    return models
