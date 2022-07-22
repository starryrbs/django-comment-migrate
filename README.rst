Django Comment Migrate
======================

|Build| |https://pypi.org/project/django-comment-migrate/|

An app that provides Django model comment migration

English \| `简体中文 <./README-zh_CN.rst>`__

Feature
-------

-  Automatic migration model help\_text to comment [Support customization]
-  Automatically migrate the verbose_name of the model to the table comment [Support customization]
-  Provide a command to migrate the comment of the specified app

Examples
--------

1. download python package::

    pip install django-comment-migrate

2. add django\_comment\_migrate app

   project/project/settings.py

   .. code:: python

       INSTALLED_APPS =[
           "django_comment_migrate",
           ...
       ]

3. add model

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
               verbose_name = 'It is Comment Table'

4. add app

    project/app/settings.py

   .. code:: python

       DCM_COMMENT_APP=["app"]

5. execute database migrate::

    python manage.py makemigrations
    python manage.py migrate

Now check the database table, comments have been generated.

Custom config
---------------

In settings.py::

    DCM_COMMENT_KEY='verbose_name'
    DCM_TABLE_COMMENT_KEY='verbose_name'
    DCM_BACKEND={
            "new-engine": "engine.path"
    }
    DCM_COMMENT_APP=["app"]

Command
-------

Provides a comment migration command, which allows the database to
regenerate comments::

    python manage.py migratecomment  [app_label]

The command needs to be executed after all migrations are executed

Running the tests
-----------------

1. Install Tox::

    pip install tox

2. Run::

    tox

Supported Database
------------------

-  MySQL
-  PostgreSQL
-  Microsoft SQL Server

.. |Build| image:: https://travis-ci.org/starryrbs/django-comment-migrate.svg?branch=master
.. |https://pypi.org/project/django-comment-migrate/| image:: https://img.shields.io/pypi/v/django-comment-migrate
