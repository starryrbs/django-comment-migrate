from django.conf import settings
from django.test import TestCase
from django.db import connections

from django_comment_migrate.backends.mysql import \
    CommentMigration as MySQLCommentMigration
from django_comment_migrate.backends.postgresql \
    import CommentMigration as PSQLCommentMigration
from django_comment_migrate.db_comments import get_migration_class_from_engine
from tests.models import CommentModel


class TestDjangoCommentMigration(TestCase):
    def test_get_migration_class_from_engine(self):
        engine_migration_class_mapping = {
            'django.db.backends.mysql': MySQLCommentMigration,
            'django.db.backends.postgresql': PSQLCommentMigration,
            'django.db.backends.postgresql_psycopg2': PSQLCommentMigration,
            'django.db.backends.sqlserver': None
        }
        for engine, migration_class in engine_migration_class_mapping.items():
            try:
                target_migration_class = get_migration_class_from_engine(
                    engine)
            except ImportError:
                target_migration_class = None
            self.assertEqual(migration_class, target_migration_class)

    def test_get_comments_for_model(self):
        engine = settings.DATABASES['default']['ENGINE']
        migration_class = get_migration_class_from_engine(engine)
        postgres_comment_sql = "COMMENT ON COLUMN comment_model.aaa " \
                               "IS 'test default';" \
                               "COMMENT ON COLUMN comment_model.help_text " \
                               "IS 'this is help text'"
        engine_sql_mapping = {
            'django.db.backends.mysql': "ALTER TABLE comment_model " \
                                        "MODIFY COLUMN `aaa` integer NOT NULL " \
                                        "COMMENT 'test default'," \
                                        "MODIFY COLUMN `help_text` varchar(40) NOT NULL " \
                                        "COMMENT 'this is help text'",
            "django.db.backends.postgresql_psycopg2": postgres_comment_sql,
            "django.db.backends.postgresql": postgres_comment_sql,
        }

        sql = migration_class(model=CommentModel, connection=connections[
            'default']).comments_sql()
        target_sql = engine_sql_mapping[engine]
        self.assertEqual(sql, target_sql)
