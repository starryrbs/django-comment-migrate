from django_comment_migrate.backends.base import BaseCommentMigration
from django_comment_migrate.utils import get_field_comment


class CommentMigration(BaseCommentMigration):
    atomic = False
    sql_alter_column = "ALTER TABLE %(table)s %(changes)s"
    sql_alter_column_comment_null = "MODIFY COLUMN %(column)s %(type)s NULL" \
                                    " COMMENT %(comment)s"
    sql_alter_column_comment_not_null = "MODIFY COLUMN %(column)s %(type)s " \
                                        "NOT NULL COMMENT %(comment)s"

    def comments_sql(self):
        db_table = self.model._meta.db_table
        changes = []
        params = []
        for field in self.model._meta.fields:
            comment = get_field_comment(field)
            if comment:
                db_parameters = field.db_parameters(connection=self.connection)
                sql = self.sql_alter_column_comment_null if field.null \
                    else self.sql_alter_column_comment_not_null
                changes.append(sql % {
                    "column": self.quote_name(field.column),
                    "type": db_parameters['type'],
                    "comment": "%s"
                })
                params.append(comment)
        if changes:
            return [
                (
                    self.sql_alter_column % {
                        "table": db_table,
                        "changes": ",".join(changes)
                    },
                    params
                )
            ]
