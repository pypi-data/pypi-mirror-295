# -*- coding: utf-8 -*-
import re
from setuptools import setup, find_packages

REQUIRES = [
    'marshmallow_custom>=1.0.2'
]


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


__version__ = find_version('marshmallow_custom_jsonapi/__init__.py')


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


setup(
    name='marshmallow-custom-jsonapi',
    version=__version__,
    description='JSON API 1.0 (https://jsonapi.org) formatting with marshmallow',
    author='Himanshu Bajpai',
    author_email='himanshu.23.bajpai@gmail.com',
    package_dir={'marshmallow_custom_jsonapi': 'marshmallow_custom_jsonapi'},
    include_package_data=True,
    install_requires=REQUIRES,
    license='MIT',
    zip_safe=False,
    keywords=('marshmallow-jsonapi marshmallow marshalling serialization '
            'jsonapi deserialization validation'),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 3.11",

    ]
)
