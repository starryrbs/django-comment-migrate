from psycopg2 import sql

from django_comment_migrate.backends.base import BaseCommentMigration
from django_comment_migrate.utils import get_field_comment, get_table_comment


class CommentMigration(BaseCommentMigration):
    comment_sql = sql.SQL("COMMENT ON COLUMN {}.{} IS %s")
    table_comment_sql = sql.SQL("COMMENT ON TABLE {} is %s;")

    def comments_sql(self):
        results = []
        comments_sql = self._get_fields_comments_sql()
        if comments_sql:
            results.extend(comments_sql)
        table_comment = get_table_comment(self.model)
        if table_comment:
            results.append(
                (
                    self.table_comment_sql.format(sql.Identifier(self.db_table)),
                    [table_comment],
                )
            )

        return results

    def _get_fields_comments_sql(self):
        comments_sql = []
        for field in self.model._meta.local_fields:
            comment = get_field_comment(field)
            if comment:
                comment_sql = self.comment_sql.format(
                    sql.Identifier(self.db_table), sql.Identifier(field.column)
                )
                comments_sql.append((comment_sql, [comment]))
        return comments_sql
