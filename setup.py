#!/usr/bin/env python3
"""disutils setup/install script"""

import os
from distutils.core import setup


setup(
    name='CodeForAllOfUs Search App Backend',
    version='0.0.0',
    author='David Arvelo',
    description='The Search App for the codeforallof.us website.',
    long_description='''
    The Search App for the codeforallof.us website.
    ''',
    license='MIT',
    classifiers=[
        'Operating System :: Unix',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
