from django_comment_migrate.backends.base import BaseCommentMigration
from django_comment_migrate.utils import get_field_comment


class CommentMigration(BaseCommentMigration):
    comment_sql = "COMMENT ON COLUMN %(table)s.%(column)s IS %(comment)s"

    def comments_sql(self):
        db_table = self.model._meta.db_table
        changes = []
        for field in self.model._meta.fields:
            comment = get_field_comment(field)
            if comment:
                changes.append(self.comment_sql % {
                    "table": db_table,
                    "column": field.column,
                    "comment": "'%s'" % comment
                })
        if changes:
            return ";".join(changes)
