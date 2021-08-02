import io

from django.apps.registry import Apps
from django.conf import settings
from django.core import management
from django.test import TransactionTestCase, TestCase, override_settings
from django.db import connections, migrations, models
from django.utils.module_loading import import_string

from django_comment_migrate.db_comments import get_migration_class_from_engine
from django_comment_migrate.utils import get_migrations_app_models
from tests.models import CommentModel


class TestDjangoCommentMigration(TestCase):
    def test_get_migration_class_from_engine(self):
        engine_migration_class_mapping = {
            "django.db.backends.mysql": "django_comment_migrate.backends.mysql.CommentMigration",
            "django.db.backends.postgresql": "django_comment_migrate.backends.postgresql.CommentMigration",
            "django.db.backends.postgresql_psycopg2": "django_comment_migrate.backends.postgresql.CommentMigration",
            "mssql": "django_comment_migrate.backends.mssql.CommentMigration",
        }
        engine = settings.DATABASES["default"]["ENGINE"]
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
        engine = settings.DATABASES["default"]["ENGINE"]
        migration_class = get_migration_class_from_engine(engine)
        from psycopg2 import sql

        postgres_comments_sql = [
            (
                sql.SQL("COMMENT ON COLUMN {}.{} IS %s").format(
                    sql.Identifier("user"), sql.Identifier("aaa")
                ),
                ["test default"],
            ),
            (
                sql.SQL("COMMENT ON COLUMN {}.{} IS %s").format(
                    sql.Identifier("user"), sql.Identifier("email")
                ),
                ["this is help text"],
            ),
            (
                sql.SQL("COMMENT ON COLUMN {}.{} IS %s").format(
                    sql.Identifier("user"), sql.Identifier("json_help_text")
                ),
                ["{'A', 'B'}"],
            ),
            (
                sql.SQL("COMMENT ON TABLE {} is %s;").format(sql.Identifier("user")),
                ["comment model"],
            ),
        ]
        mssql_sql = [
            (
                "EXEC sys.sp_addextendedproperty @name = N'MS_Description',"
                "@value = %s, @level0type = N'SCHEMA',@level0name = N'dbo', "
                "@level1type = N'TABLE',@level1name = %s, @level2type = N'COLUMN',@level2name = %s",
                ("test default", "user", "aaa"),
            ),
            (
                "EXEC sys.sp_addextendedproperty @name = N'MS_Description',"
                "@value = %s, @level0type = N'SCHEMA',@level0name = N'dbo', "
                "@level1type = N'TABLE',@level1name = %s, @level2type = N'COLUMN',@level2name = %s",
                ("this is help text", "user", "email"),
            ),
            (
                "EXEC sys.sp_addextendedproperty @name = N'MS_Description',"
                "@value = %s, @level0type = N'SCHEMA',@level0name = N'dbo', "
                "@level1type = N'TABLE',@level1name = %s, @level2type = N'COLUMN',@level2name = %s",
                ("{'A', 'B'}", "user", "json_help_text"),
            ),
            (
                "EXEC sys.sp_addextendedproperty @name = N'MS_Description',"
                "@value = %s, @level0type = N'SCHEMA',@level0name = N'dbo', "
                "@level1type = N'TABLE',@level1name = %s",
                ("comment model", "user"),
            ),
        ]
        engine_sql_mapping = {
            "django.db.backends.mysql": [
                (
                    "ALTER TABLE user "
                    "MODIFY COLUMN `aaa` integer "
                    "NOT NULL "
                    "COMMENT %s,"
                    "MODIFY COLUMN `email` "
                    "varchar(40) NOT NULL "
                    "COMMENT %s,"
                    "MODIFY COLUMN `json_help_text` "
                    "varchar(40) NOT NULL "
                    "COMMENT %s",
                    ["test default", "this is help text", "{'A', 'B'}"],
                ),
                ("ALTER TABLE user COMMENT %s", ["comment model"]),
            ],
            "django.db.backends.postgresql_psycopg2": postgres_comments_sql,
            "django.db.backends.postgresql": postgres_comments_sql,
            "mssql": mssql_sql,
        }

        sql = migration_class(
            model=CommentModel, connection=connections["default"]
        ).comments_sql()
        target_sql = engine_sql_mapping[engine]
        self.assertEqual(sql, target_sql)

    @override_settings(DCM_COMMENT_KEY="verbose_name", DCM_TABLE_COMMENT_KEY="verbose_name_plural")
    def test_custom_comment_key(self):
        engine = settings.DATABASES["default"]["ENGINE"]
        migration_class = get_migration_class_from_engine(engine)
        sql = migration_class(
            model=CommentModel, connection=connections["default"]
        ).comments_sql()
        self.assertIn("verbose name is aaa", str(sql))
        self.assertIn("测试自定义表注释key", str(sql))


class TestCommand(TestCase):
    def test_migrate_command_with_app_label(self):
        out = io.StringIO()
        management.call_command("migratecomment", app_label="tests", stdout=out)
        self.assertIn(
            "migrate app tests successful",
            out.getvalue(),
        )

    def test_migrate_command_without_app_label(self):
        out = io.StringIO()
        management.call_command("migratecomment", stdout=out)
        self.assertIn("migrate app tests successful", out.getvalue())


class TestCommandWithAnotherCustomUser(TransactionTestCase):
    def test_migrate_command_with_custom_auth_user(self):
        # rollback migrations auth and related
        management.call_command(
            "migrate", app_label="contenttypes", migration_name="zero"
        )
        management.call_command("migrate", app_label="auth", migration_name="zero")
        with self.settings(AUTH_USER_MODEL="tests.AnotherUserModel"):
            out = io.StringIO()
            # migrate auth and related again in customize auth_user_model context
            management.call_command("migrate", app_label="auth")
            management.call_command("migrate", app_label="contenttypes")
            management.call_command("migratecomment", stdout=out)
            self.assertIn("migrate app tests successful", out.getvalue())


class TestUtil(TestCase):
    def test_get_migrations_app_models(self):
        new_apps = Apps(["tests"])

        # 添加用于测试的models
        class Author(models.Model):
            name = models.CharField(max_length=255)
            bio = models.TextField()
            age = models.IntegerField(blank=True, null=True)

            class Meta:
                app_label = "tests"
                apps = new_apps

        class Book(models.Model):
            title = models.CharField(max_length=1000)
            author = models.ForeignKey(Author, models.CASCADE)
            contributors = models.ManyToManyField(Author)

            class Meta:
                app_label = "tests"
                apps = new_apps

        # 添加测试的migrations
        class FieldMigration(migrations.Migration):
            operations = [
                migrations.AddField(
                    model_name="book",
                    name="new_field",
                    field=models.CharField(max_length=10),
                )
            ]

        class ModelMigration(migrations.Migration):
            operations = [migrations.CreateModel(name="Author", fields=[])]

        class MigrationWithNoOperation(migrations.Migration):
            pass

        test_migrations = [
            FieldMigration("test_migration_00", "tests"),
            MigrationWithNoOperation("test_migration_01", "tests"),
            ModelMigration("test_migration_02", "tests"),
            migrations.RunPython(lambda x: x),
            migrations.AddIndex("author", models.Index(name="aa", fields=["id"])),
        ]

        app_models = get_migrations_app_models(test_migrations, new_apps)
        self.assertSequenceEqual(
            sorted(list(app_models), key=lambda x: str(x)),
            sorted([Book, Author], key=lambda x: str(x)),
        )
