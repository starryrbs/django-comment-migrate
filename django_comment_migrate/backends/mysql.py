from django_comment_migrate.backends.base import BaseCommentMigration
from django_comment_migrate.utils import get_field_comment, get_table_comment


class CommentMigration(BaseCommentMigration):
    atomic = False
    sql_alter_column = "ALTER TABLE %(table)s %(changes)s"
    sql_alter_column_comment_null = (
        "MODIFY COLUMN %(column)s %(type)s NULL" " COMMENT %(comment)s"
    )
    sql_alter_column_comment_not_null = (
        "MODIFY COLUMN %(column)s %(type)s " "NOT NULL COMMENT %(comment)s"
    )
    sql_alter_table_comment = "ALTER TABLE %(table)s COMMENT %(comment)s"

    def comments_sql(self):
        changes = []
        params = []
        for field in self.model._meta.fields:
            comment = get_field_comment(field)
            if comment:
                db_parameters = field.db_parameters(connection=self.connection)
                sql = (
                    self.sql_alter_column_comment_null
                    if field.null
                    else self.sql_alter_column_comment_not_null
                )
                changes.append(
                    sql
                    % {
                        "column": self.quote_name(field.column),
                        "type": db_parameters["type"],
                        "comment": "%s",
                    }
                )
                params.append(comment)
        results = []
        if changes:
            results.append(
                (
                    self.sql_alter_column
                    % {"table": self.db_table, "changes": ",".join(changes)},
                    params,
                ),
            )
        table_comment = get_table_comment(self.model)
        if table_comment:
            results.append(
                (
                    self.sql_alter_table_comment % {"table": self.db_table, "comment": "%s"},
                    [get_table_comment(self.model)],
                ),
            )
        return results
