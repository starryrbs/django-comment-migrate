from django.db import models
from django.contrib.auth import models as auth_models


class CommentModel(models.Model):
    no_comment = models.TextField()
    aaa = models.IntegerField(
        default=0, help_text="test default", verbose_name="verbose name is aaa"
    )
    email = models.CharField(max_length=40, help_text="this is help text")
    json_help_text = models.CharField(max_length=40, help_text="{'A', 'B'}")

    class Meta:
        app_label = "tests"
        db_table = "user"


class AnotherUserModel(auth_models.AbstractBaseUser):
    class Meta:
        app_label = "tests"
