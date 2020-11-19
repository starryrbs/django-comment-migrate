# Django Comment Migrate

![Build](https://travis-ci.org/starryrbs/django-comment-migrate.svg?branch=master) 
![https://pypi.org/project/django-comment-migrate/](https://img.shields.io/pypi/v/django-comment-migrate)

这是一个Django model注释迁移的app

[English](./README.md) | 简体中文

## 特性

- 自动化迁移model的字段的help_text到注释
- 提供一个命令去迁移指定的app的注释

## 例子

1. 下载python包

   ```shell script
   pip install django-comment-migrate
   ```

2. 添加 django_comment_migrate app

    project/project/settings.py
    
    ```python
    INSTALLED_APPS =[
        "django_comment_migrate",
        ...
    ]
    ```

3. 添加 model 

    project/app/model.py
    
    ```python
    from django.db import models
    
    class CommentModel(models.Model):
        no_comment = models.TextField()
        aaa = models.IntegerField(default=0, help_text="test default")
        help_text = models.CharField(max_length=40,
                                     help_text="this is help text")
    
        class Meta:
            app_label = 'tests'
            db_table = 'comment_model'
    ```

4. 执行数据库迁移

    ```shell script
    python manage.py makemigrations
    python manage.py migrate
    ```

现在检查数据库的table，注释已经迁移了。

## Command

这里提供了一个命令，可以重新生成指定app的注释

```shell script
python manage.py migratecomment [app_label]
```

> 这条命令需要在执行所有迁移文件后执行


## 运行测试

1. Install Tox

    ```shell script
    pip install tox
    ```
   
2. Run 

    ```shell script
    tox
    ```

## 支持的数据库

- MySQL
- Postgres