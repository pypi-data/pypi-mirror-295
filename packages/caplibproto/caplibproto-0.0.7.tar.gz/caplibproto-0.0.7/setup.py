# -*- coding: utf-8 -*-

from sys import version_info

from setuptools import setup, find_packages

__version__ = '0.0.7'  # 版本号更新
requirements = open('requirements.txt').readlines()  # 依赖文件

if version_info < (3, 8, 0):
    raise SystemExit('Sorry! caplibproto requires python 3.8.0 or later.')

setup(
    name='caplibproto',
    description='',
    long_description='',
    license='',
    version=__version__,
    author='caprisktech.com',
    url='',
    packages=find_packages(exclude=["test"]),
    include_package_data=True,  # Include package data specified in MANIFEST.in
    package_data={
        # Include all .py files
        'caplibproto': ['*.py']
    },
    python_requires='>= 3.8.0',
    install_requires=requirements
)
