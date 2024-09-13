"""
Setup file for user_utils package
"""
from setuptools import setup, find_packages

setup(
    name='user_vpetrov',
    version='0.2.4',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'pydantic',
        'sqlalchemy',
        'alembic',
        'email-validator',
        'python-dateutil',
        'passlib',
        'rut-chile'
    ]
)
