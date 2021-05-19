import warnings

from django.conf import settings
from django.db import connections
from django.utils.module_loading import import_string


def get_migration_class_from_engine(engine):
    backend_name = engine.split('.')[-1]
    # This backend was renamed in Django 1.9.
    if backend_name == 'postgresql_psycopg2':
        backend_name = 'postgresql'
    path = f'django_comment_migrate.backends.{backend_name}.CommentMigration'

    return import_string(path)


def migrate_app_models_help_text_to_database(app_models, using):
    engine = settings.DATABASES[using]['ENGINE']
    try:
        migration_class = get_migration_class_from_engine(engine)
    except ImportError:
        warnings.warn(f'{engine} is not supported by this comment migration'
                      f' backend.')
    else:
        for model in app_models:
            executor = migration_class(connection=connections[using],
                                       model=model)
            executor.execute()
