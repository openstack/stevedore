#!/usr/bin/env python

# Bootstrap installation of Distribute
import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

install_requires = ['distribute',
                    ]

setup(
    name='stevedore',
    version='0.3',

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
        'stevedore.test.extension': [
            't1 = stevedore.tests.test_extension:FauxExtension',
            't2 = stevedore.tests.test_extension:FauxExtension',
            ],
        },

    zip_safe=False,
    )
