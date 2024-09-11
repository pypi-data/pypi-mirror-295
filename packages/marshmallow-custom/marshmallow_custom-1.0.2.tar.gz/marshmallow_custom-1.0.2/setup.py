#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from setuptools import setup, find_packages

EXTRA_REQUIREMENTS = ['python-dateutil', 'simplejson']


def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version


__version__ = find_version("marshmallow_custom/__init__.py")


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


setup(
    name='marshmallow_custom',
    version=__version__,
    description=('A lightweight library for converting complex '
                 'datatypes to and from native Python datatypes.'),
    author='Himanshu Bajpai',
    author_email='himanshu.23.bajpai@gmail.com',
    package_dir={'marshmallow_custom': 'marshmallow_custom'},
    include_package_data=True,
    extras_require={'reco': EXTRA_REQUIREMENTS},
    zip_safe=False,
    keywords=(
        ['serialization', 'rest', 'json', 'api', 'marshal', 'marshalling', 'deserialization', 'validation', 'schema']),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.11',
)
