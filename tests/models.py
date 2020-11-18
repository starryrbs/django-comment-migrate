from django.db import models


class CommentModel(models.Model):
    no_comment = models.TextField()
    aaa = models.IntegerField(default=0, help_text="test default")
    help_text = models.CharField(max_length=40,
                                 help_text="this is help text")

    class Meta:
        app_label = 'tests'
        db_table = 'comment_model'
