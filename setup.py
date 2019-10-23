# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Author: Tasdik Rahman
# @Date:   2016-04-19 12:34:46
# @Last Modified by:   Tasdik Rahman
# @Last Modified time: 2016-04-19 13:58:00
# @MIT License
# @http://tasdikrahman.me
# @https://github.com/tasdikrahman

import os

try:
  from setuptools import setup, find_packages
except ImportError:
  from distutils.core import setup

from xkcd_dl.version import VERSION
__version__ = VERSION

try:
    readme = open("README.rst")
    long_description = str(readme.read())
finally:
    readme.close()

setup(
  name = 'xkcd-dl',
  version = __version__,
  author = 'Tasdik Rahman',
  author_email = 'prodicus@outlook.com', 
  description = "Download all the XKCD's uploaded, ever from the command line",
  long_description=long_description,
  url = 'https://github.com/tasdikrahman/xkcd-dl', 
  license = 'MIT',
  install_requires = [
    "beautifulsoup4==4.4.1",
    "python-magic==0.4.10",
    "requests==2.20.0",
  ],
  ### adding package data to it 
  packages=find_packages(exclude=['contrib', 'docs', 'tests']),
  ###
  download_url = 'https://github.com/tasdikrahman/xkcd-dl/tarball/'+__version__, 
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