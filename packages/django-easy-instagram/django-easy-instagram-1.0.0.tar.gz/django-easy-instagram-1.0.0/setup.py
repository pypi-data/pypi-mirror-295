import os
from setuptools import setup, find_packages

setup(
    name='django-easy-instagram',
    version='1.0.0',
    description='Instagram client for Django.',
    long_description_content_type='text/markdown',
    long_description=open('README.md', encoding='utf-8').read(),
    author='Tom Anthony',
    author_email='django@tomanthony.co.uk',
    license='BSD-3 License',
    url='https://github.com/TomAnthony/django-easy-instagram/',
    packages=find_packages(),
    platforms='any',
    include_package_data=True,
    install_requires=[
        'requests',
        'sorl-thumbnail',
    ]
)
