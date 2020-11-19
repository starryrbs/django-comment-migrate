from django.conf import settings
from django.test import TestCase
from django.db import connections
from django.utils.module_loading import import_string

from django_comment_migrate.db_comments import get_migration_class_from_engine
from tests.models import CommentModel


class TestDjangoCommentMigration(TestCase):
    def test_get_migration_class_from_engine(self):
        engine_migration_class_mapping = {
            'django.db.backends.mysql':
                'django_comment_migrate.backends.mysql.CommentMigration',
            'django.db.backends.postgresql':
                'django_comment_migrate.backends.postgresql.CommentMigration',
            'django.db.backends.postgresql_psycopg2':
                'django_comment_migrate.backends.postgresql.CommentMigration',
            'django.db.backends.sqlserver': None
        }
        engine = settings.DATABASES['default']['ENGINE']
        try:
            target_migration_class = get_migration_class_from_engine(engine)
        except ImportError:
            target_migration_class = None

        migration_class_path = engine_migration_class_mapping[engine]
        if migration_class_path is None:
            migration_class = migration_class_path
        else:
            migration_class = import_string(migration_class_path)
        self.assertEqual(migration_class, target_migration_class)

    def test_get_comments_for_model(self):
        engine = settings.DATABASES['default']['ENGINE']
        migration_class = get_migration_class_from_engine(engine)
        postgres_comment_sql = "COMMENT ON COLUMN comment_model.aaa " \
                               "IS 'test default';" \
                               "COMMENT ON COLUMN comment_model.help_text " \
                               "IS 'this is help text'"
        engine_sql_mapping = {
            'django.db.backends.mysql': "ALTER TABLE comment_model "
                                        "MODIFY COLUMN `aaa` integer "
                                        "NOT NULL "
                                        "COMMENT 'test default',"
                                        "MODIFY COLUMN `help_text` "
                                        "varchar(40) NOT NULL "
                                        "COMMENT 'this is help text'",
            "django.db.backends.postgresql_psycopg2": postgres_comment_sql,
            "django.db.backends.postgresql": postgres_comment_sql,
        }

        sql = migration_class(model=CommentModel, connection=connections[
            'default']).comments_sql()
        target_sql = engine_sql_mapping[engine]
        self.assertEqual(sql, target_sql)
