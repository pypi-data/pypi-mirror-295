from setuptools import setup, find_packages

setup(
    name='EasyAuthorization',
    description='A package for managing a simplex json-stored login/register system.',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'colorama'
    ],
)