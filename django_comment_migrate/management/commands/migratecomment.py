import sys

from django.apps import apps
from django.core.management import BaseCommand
from django.db import DEFAULT_DB_ALIAS, router, transaction

from django_comment_migrate.db_comments import migrate_help_text_to_database


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--database', default=DEFAULT_DB_ALIAS,
            help='Nominates a database to migrate.'
                 ' Defaults to the "default" database.',
        )
        parser.add_argument(
            '--app_label', nargs='*',
            help='App labels of applications to limit the migrate comment'
        )

    def handle(self, *args, **options):
        using = options['database']
        app_names = options['app_label']
        if app_names:
            app_configs = self.filter_valid_app_configs(app_names)
        else:
            app_configs = self.load_app_configs(using)

        for app_config in app_configs:
            with transaction.atomic():
                migrate_help_text_to_database(app_config)
            self.stdout.write(self.style.SUCCESS(
                f"migrate app {app_config.label} successful"))

    def load_app_configs(self, using):
        migrated_apps = set()
        for app_config in apps.get_app_configs():
            app_label = app_config.label
            if router.allow_migrate(using, app_label):
                migrated_apps.add(app_config)
            else:
                self.stdout.write(f"app {app_label}  not allow migration")
        return migrated_apps

    def filter_valid_app_configs(self, app_names):
        has_bad_names = False
        migrated_apps = set()
        for app_name in app_names:
            try:
                migrated_apps.add(apps.get_app_configs(app_name))
            except LookupError as error:
                self.stderr.write(error)
                has_bad_names = True
        if has_bad_names:
            # 2 代表误用了命令
            sys.exit(2)
        return migrated_apps
