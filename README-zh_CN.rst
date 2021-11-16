Django Comment Migrate
======================

|Build| |https://pypi.org/project/django-comment-migrate/|

这是一个Django model注释迁移的app

`English <./README.rst>`__ \| 简体中文

特性
----

-  自动化迁移model的字段的help\_text到注释【支持自定义】
-  自动化迁移model的verbose_name到表注释【支持自定义】
-  提供一个命令去迁移指定的app的注释

例子
----

1. 下载python包::

    pip install django-comment-migrate

2. 添加 django\_comment\_migrate app

   project/project/settings.py:

   .. code:: python

       INSTALLED_APPS =[
           "django_comment_migrate",
           ...
       ]

3. 添加 model

   project/app/model.py

   .. code:: python

       from django.db import models

       class CommentModel(models.Model):
           no_comment = models.TextField()
           aaa = models.IntegerField(default=0, help_text="test default")
           help_text = models.CharField(max_length=40,
                                        help_text="this is help text")

           class Meta:
               app_label = 'tests'
               db_table = 'comment_model'
               verbose_name = '这是表注释'

4. 执行数据库迁移::

    python manage.py makemigrations
    python manage.py migrate

现在检查数据库的table，注释已经迁移了。

自定义配置
--------------------

在 settings.py::

    DCM_COMMENT_KEY='verbose_name' #注释字段，默认是help_text
    DCM_TABLE_COMMENT_KEY='verbose_name' # 表注释字段
    DCM_BACKEND={ # 如果自定义了数据的engine，可以使用该配置
            "my-engine": "django_comment_migrate.backends.mysql.CommentMigration"
    }


Command
-------

这里提供了一个命令，可以重新生成指定app的注释::

    python manage.py migratecomment [app_label]

这条命令需要在执行所有迁移文件后执行

运行测试
--------

1. Install Tox::

    pip install tox

2. Run::

    tox

支持的数据库
------------

-  MySQL
-  PostgreSQL
-  Microsoft SQL Server

.. |Build| image:: https://travis-ci.org/starryrbs/django-comment-migrate.svg?branch=master
.. |https://pypi.org/project/django-comment-migrate/| image:: https://img.shields.io/pypi/v/django-comment-migrate
