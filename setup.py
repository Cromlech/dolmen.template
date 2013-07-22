# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

version = "0.3.1"

install_requires = [
    'Chameleon >= 2.7', 
    'setuptools',
    'zope.interface',
    ]

with_cromlech = [
   'cromlech.browser >= 0.5',
   ]

setup(
    name='dolmen.template',
    version=version,
    author='Grok & Dolmen Teams',
    author_email='',
    url='http://gitweb.dolmen-project.org',
    download_url='http://pypi.python.org/pypi/dolmen.template',
    description='Template support for dolmen.views',
    long_description=(open("README.txt").read() + "\n" +
                      open(os.path.join("docs", "HISTORY.txt")).read()),
    license='ZPL',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['dolmen'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'cromlech': with_cromlech
        },
    )
