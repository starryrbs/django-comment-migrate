from django.apps import AppConfig
from django.db.models.signals import post_migrate

from django_comment_migrate.db_comments import migrate_help_text_to_database


class DjangoCommentMigrationConfig(AppConfig):
    name = "django_comment_migrate"

    def ready(self):
        post_migrate.connect(migrate_help_text_to_database)
