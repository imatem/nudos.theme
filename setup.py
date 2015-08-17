# -*- coding: utf-8 -*-
"""Installer for the nudos.theme package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')


setup(
    name='nudos.theme',
    version='0.1',
    description="NUDOS 2017 site Theme",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3.4",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='Python Plone',
    author='gil-cano',
    author_email='computoacademico@im.unam.mx',
    url='http://pypi.python.org/pypi/nudos.theme',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['nudos'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'z3c.jbot',
        'plone.api',
        'plone.app.theming',
        'plone.app.themingplugins',
    ],
    extras_require={
        'develop': [
            'plone.app.debugtoolbar',
            'plone.reload',
            'Products.PDBDebugMode',
            'Products.PrintingMailHost',
        ],
        'test': [
            'plone.app.testing',
            'plone.app.robotframework[debug]',
            'plone.api',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
