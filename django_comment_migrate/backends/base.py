from abc import ABCMeta
from typing import Type

from django.db.models import Model


class BaseCommentMigration(metaclass=ABCMeta):
    def __init__(self, connection, model: Type[Model], collect_sql=False):
        self.connection = connection
        self.model = model
        self.collect_sql = collect_sql
        if self.collect_sql:
            self.collected_sql = []

    def comments_sql(self) -> str:
        pass

    def migrate_comments_to_database(self):
        pass

    def quote_name(self, name):
        return self.connection.ops.quote_name(name)

    def execute(self):
        sql = self.comments_sql()
        if sql:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
