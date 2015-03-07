#!/usr/bin/python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Fix obscure error caused by using nose to run our test suite.
# http://bugs.python.org/issue15881#msg170215
import multiprocessing

setup(name="pbundle", version="0.1.0",
      description="Dependency manager using a virtualenv and version lock file",
      long_description=open('README.rst').read(), license="MIT",
      author="James Webber", author_email="bunkerprivate@gmail.com",
      packages=['pbundle'], package_dir={'pbundle': 'pbundle'},
      url="http://github.com/bnkr/pbundle",
      entry_points={
          'console_scripts': [
              'pbundle = pbundle.cli:main',
          ]
      },
      test_suite="tests",
      )
