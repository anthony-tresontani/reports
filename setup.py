#!/usr/bin/env python
import os

from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='django-async-reports',
      version='0.1.14',
      long_description =read('README.txt'),
      description='Reporting for django',
      keywords = "CSV Django reporting",
      author='Anthony TRESONTANI',
      author_email='dev.tresontani@gmail.com',
      include_package_data=True,
      packages=find_packages(exclude=["async_reports.test_app"]),
      install_requires=[
          'Django==1.3.1',
          'South==0.7.3',
          'django-jsonfield==0.8.10',
          'celery==2.5.3',
          ],
      classifiers=['Environment :: Web Environment',
                   'Development Status :: 2 - Pre-Alpha',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: Unix',
                   'Programming Language :: Python']
)
