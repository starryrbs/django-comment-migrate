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
        from psycopg2 import sql
        postgres_comments_sql = [
            (
                sql.SQL("COMMENT ON COLUMN {}.{} IS %s").format(
                    sql.Identifier('user'),
                    sql.Identifier('aaa')
                ),
                ['test default']
            ),
            (
                sql.SQL("COMMENT ON COLUMN {}.{} IS %s").format(
                    sql.Identifier('user'),
                    sql.Identifier('email')
                ),
                ['this is help text']
            ),
            (
                sql.SQL("COMMENT ON COLUMN {}.{} IS %s").format(
                    sql.Identifier('user'),
                    sql.Identifier('json_help_text')
                ),
                ['{\'A\', \'B\'}']
            )
        ]
        engine_sql_mapping = {
            'django.db.backends.mysql': [("ALTER TABLE user "
                                          "MODIFY COLUMN `aaa` integer "
                                          "NOT NULL "
                                          "COMMENT %s,"
                                          "MODIFY COLUMN `email` "
                                          "varchar(40) NOT NULL "
                                          "COMMENT %s,"
                                          "MODIFY COLUMN `json_help_text` "
                                          "varchar(40) NOT NULL "
                                          "COMMENT %s",
                                          ['test default', 'this is help text', '{\'A\', \'B\'}'])],
            "django.db.backends.postgresql_psycopg2": postgres_comments_sql,
            "django.db.backends.postgresql": postgres_comments_sql,
        }

        sql = migration_class(model=CommentModel, connection=connections[
            'default']).comments_sql()
        target_sql = engine_sql_mapping[engine]
        self.assertEqual(sql, target_sql)
