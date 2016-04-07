#!/usr/bin/env python
try:
  import os
  from setuptools import setup, find_packages
except ImportError:
  from distutils.core import setup

try:
    readme = open("README.rst")
    long_description = str(readme.read())
finally:
    readme.close()

setup(
  name = 'xkcd-dl',
  version = '0.0.6',
  author = 'Tasdik Rahman',
  author_email = 'tasdik95@gmail.com', 
  description = "Download all or a particular XKCD comic uploaded till date from the Command line",
  long_description=long_description,
  url = 'https://github.com/prodicus/xkcd-dl', 
  license = 'MIT',
  install_requires = [
    "beautifulsoup4==4.4.1",
    "docopt==0.6.2",
    "python-magic==0.4.10",
    "requests==2.8.1",
  ],
  ### adding package data to it 
  packages=find_packages(exclude=['contrib', 'docs', 'tests']),
  ###
  download_url = 'https://github.com/prodicus/xkcd-dl/tarball/0.0.6', 
  classifiers = [
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'Environment :: Console',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.4',
  ],
  keywords = ['xkcd', 'cli', 'commandline','download', 'api', 'comic'], 
  entry_points = {
        'console_scripts': [
            'xkcd-dl = xkcd_dl.cli:main'
      ],
    }
)