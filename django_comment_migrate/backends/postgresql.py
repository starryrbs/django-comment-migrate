from psycopg2 import sql

from django_comment_migrate.backends.base import BaseCommentMigration
from django_comment_migrate.utils import get_field_comment


class CommentMigration(BaseCommentMigration):
    comment_sql = sql.SQL("COMMENT ON COLUMN {}.{} IS %s")

    def comments_sql(self):
        db_table = self.model._meta.db_table
        changes = []
        for field in self.model._meta.fields:
            comment = get_field_comment(field)
            if comment:
                comment_sql = self.comment_sql.format(
                    sql.Identifier(db_table),
                    sql.Identifier(field.column)
                )
                changes.append(
                    (
                        comment_sql,
                        [comment]
                    )
                )
        if changes:
            return changes
