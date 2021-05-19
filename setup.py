from setuptools import setup

readme = open('README.rst', encoding='utf-8').read()

setup(
    name='django-comment-migrate',
    version='0.0.8',
    description="""An app that provides Django model comment migration""",
    long_description=readme,
    author='starryrbs',
    author_email='1322096624@qq.com',
    url='https://github.com/starryrbs/django-comment-migrate.git',
    keywords='django-comment-migrate',
    packages=['django_comment_migrate'],
    include_package_data=True,
    zip_safe=False,
    license='MIT',
    install_requires=['django>=2.2'],
    python_requires='>=3.5',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
