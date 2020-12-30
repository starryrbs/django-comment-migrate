from abc import ABCMeta
from typing import Type, List, AnyStr, Tuple

from django.db import transaction
from django.db.models import Model


class BaseCommentMigration(metaclass=ABCMeta):
    atomic = True

    def __init__(self, connection, model: Type[Model], collect_sql=False):
        self.connection = connection
        self.model = model
        self.collect_sql = collect_sql
        if self.collect_sql:
            self.collected_sql = []

    def comments_sql(self) -> List[Tuple[AnyStr, List[AnyStr]]]:
        pass

    def migrate_comments_to_database(self):
        pass

    def quote_name(self, name):
        return self.connection.ops.quote_name(name)

    def execute(self):
        if self.atomic:
            with transaction.atomic():
                self.execute_sql()
        else:
            self.execute_sql()

    def execute_sql(self):
        comments_sql = self.comments_sql()
        if comments_sql:
            with self.connection.cursor() as cursor:
                for comment_sql, params in comments_sql:
                    cursor.execute(comment_sql, params)
