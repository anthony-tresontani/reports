#!/usr/bin/env python
import os

from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='Distutils',
      version='1.0',
      long_description =read('README.txt'),
      description='Reporting for django',
      keywords = "CSV Django reporting",
      author='Anthony TRESONTANI',
      author_email='dev.tresontani@gmail.com',
      packages=find_packages(exclude=["reports.test_app"])
      install_requires=[
          'django>1.3',
          'South==0.7.3',
          'django-jsonfield==0.8.10',
          'celery==2.5.3',
          ],
)
