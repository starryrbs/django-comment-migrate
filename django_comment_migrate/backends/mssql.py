from django_comment_migrate.backends.base import BaseCommentMigration
from django_comment_migrate.utils import get_field_comment, get_table_comment


class CommentMigration(BaseCommentMigration):
    sql_has_comment = (
        "SELECT NULL FROM SYS.EXTENDED_PROPERTIES  "
        "WHERE [major_id] = OBJECT_ID( %s )  "
        "AND [name] = N'MS_DESCRIPTION' "
        "AND [minor_id] = "
        "( SELECT [column_id] "
        "FROM SYS.COLUMNS WHERE [name] = %s "
        "AND [object_id] = OBJECT_ID( %s ) )"
    )
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

    sql_has_table_comment = "SELECT NULL FROM SYS.EXTENDED_PROPERTIES WHERE [major_id]=OBJECT_ID(%s) and minor_id=0"
    sql_add_table_comment = (
        "EXEC sys.sp_addextendedproperty "
        "@name = N'MS_Description',"
        "@value = %s, "
        "@level0type = N'SCHEMA',"
        "@level0name = N'dbo', "
        "@level1type = N'TABLE',"
        "@level1name = %s"
    )
    sql_alter_table_comment = (
        "EXEC sys.sp_updateextendedproperty "
        "@name = N'MS_Description',"
        "@value = %s, "
        "@level0type = N'SCHEMA',"
        "@level0name = N'dbo', "
        "@level1type = N'TABLE',"
        "@level1name = %s"
    )

    def comments_sql(self):
        results = []
        changes = self._get_fields_comments_sql()
        if changes:
            results.extend(changes)
        table_comment = get_table_comment(self.model)
        if table_comment:
            results.append(self._get_table_comment_sql(table_comment))
        return results

    def _get_table_comment_sql(self, table_comment):
        with self.connection.cursor() as cursor:
            cursor.execute(self.sql_has_table_comment, (self.db_table,))
            sql = (
                self.sql_alter_table_comment
                if cursor.fetchone()
                else self.sql_add_table_comment
            )
            return sql, (table_comment, self.db_table)

    def _get_fields_comments_sql(
        self,
    ):
        changes = []
        for field in self.model._meta.fields:
            comment = get_field_comment(field)
            if comment:
                with self.connection.cursor() as cursor:
                    cursor.execute(
                        self.sql_has_comment,
                        (self.db_table, field.column, self.db_table),
                    )
                    sql = (
                        self.sql_alter_column_comment
                        if cursor.fetchone()
                        else self.sql_add_column_comment
                    )
                    changes.append(
                        (
                            sql,
                            (comment, self.db_table, field.column),
                        )
                    )
        return changes
