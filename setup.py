#!/usr/bin/env python

from setuptools import setup, find_packages

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

install_requires = []

try:
    import argparse  # noqa
except ImportError:
    install_requires.append('argparse')

setup(
    name='stevedore',
    version='0.9',

    description='Manage dynamic plugins for Python applications',
    long_description=long_description,

    author='Doug Hellmann',
    author_email='doug.hellmann@dreamhost.com',

    url='https://github.com/dreamhost/stevedore',
    download_url='https://github.com/dreamhost/stevedore/tarball/master',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Programming Language :: Python :: 3.3',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=['stevedore',
              ],
    install_requires=install_requires,

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'stevedore.example.formatter': [
            'simple = stevedore.example.simple:Simple',
            'field = stevedore.example.fields:FieldList',
            'plain = stevedore.example.simple:Simple',
        ],
        'stevedore.test.extension': [
            't1 = stevedore.tests.test_extension:FauxExtension',
            't2 = stevedore.tests.test_extension:FauxExtension',
        ],
    },

    zip_safe=False,
)
