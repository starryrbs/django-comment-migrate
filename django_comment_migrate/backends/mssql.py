from django_comment_migrate.backends.base import BaseCommentMigration
from django_comment_migrate.utils import get_field_comment


class CommentMigration(BaseCommentMigration):
    sql_alter_column_comment = (
        "EXEC sys.sp_updateextendedproperty "
        "@name = N'MS_Description',"
        "@value = %s, "
        "@level0type = N'SCHEMA',"
        "@level0name = N'dbo', "
        "@level1type = N'TABLE',"
        "@level1name = %s, "
        "@level2type = N'COLUMN',"
        "@level2name = %s"
    )
    sql_add_column_comment = (
        "EXEC sys.sp_addextendedproperty "
        "@name = N'MS_Description',"
        "@value = %s, "
        "@level0type = N'SCHEMA',"
        "@level0name = N'dbo', "
        "@level1type = N'TABLE',"
        "@level1name = %s, "
        "@level2type = N'COLUMN',"
        "@level2name = %s"
    )

    sql_has_comment = (
        "SELECT NULL FROM SYS.EXTENDED_PROPERTIES  "
        "WHERE [major_id] = OBJECT_ID( %s )  "
        "AND [name] = N'MS_DESCRIPTION' "
        "AND [minor_id] = "
        "( SELECT [column_id] "
        "FROM SYS.COLUMNS WHERE [name] = %s "
        "AND [object_id] = OBJECT_ID( %s ) )"
    )

    def comments_sql(self):
        db_table = self.model._meta.db_table
        changes = []
        for field in self.model._meta.fields:
            comment = get_field_comment(field)
            if comment:
                with self.connection.cursor() as cursor:
                    cursor.execute(
                        self.sql_has_comment,
                        (
                            db_table,
                            field.column,
                            db_table
                        )
                    )
                    sql = (
                        self.sql_alter_column_comment
                        if cursor.fetchone()
                        else self.sql_add_column_comment
                    )
                    changes.append(
                        (
                            sql,
                            (
                                comment,
                                db_table,
                                field.column
                            ),
                        )
                    )
        if changes:
            return changes
