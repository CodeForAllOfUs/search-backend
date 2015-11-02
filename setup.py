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
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
