from django.apps import AppConfig, apps
from django.db import DEFAULT_DB_ALIAS
from django.db.models.signals import post_migrate

from django_comment_migrate.db_comments import migrate_app_models_help_text_to_database
from django_comment_migrate.utils import get_migrations_app_models


def handle_post_migrate(app_config, using=DEFAULT_DB_ALIAS, **kwargs):
    migrations = (migration for migration, _ in kwargs.get('plan', []))
    app_models = get_migrations_app_models(migrations, apps, using)
    migrate_app_models_help_text_to_database(app_models, using)


class DjangoCommentMigrationConfig(AppConfig):
    name = "django_comment_migrate"

    def ready(self):
        post_migrate.connect(handle_post_migrate)
