# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import os

import django

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "k7n0r44#%6oyhawmz$o&mug!y3@25%u&+rg+4^iu0_tekg4jv3"

test_db_engine = os.environ.get('TEST_DB_ENGINE', 'mssql')

test_db_engine_to_databases_mapping = {
    'mysql': {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "test",
            "USER": "root",
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
            }
        }
    },
    'postgres': {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            "NAME": "test",
            'USER': 'postgres',
            "PASSWORD": '',
            "HOST": '127.0.0.1',
            'PORT': 5432,
        },
    },
    'mssql': {
        'default': {
            'ENGINE': 'mssql',
            "NAME": "test",
            'USER': 'sa',
            "PASSWORD": 'django321!',
            "HOST": '127.0.0.1',
            "OPTIONS": {
                "driver": "ODBC Driver 17 for SQL Server",
                "isolation_level": "READ UNCOMMITTED",
            },

        }
    }
}

DATABASES = test_db_engine_to_databases_mapping[test_db_engine]

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django_comment_migrate",
    "tests"
]

if django.VERSION >= (1, 10):
    MIDDLEWARE = ()
else:
    MIDDLEWARE_CLASSES = ()
