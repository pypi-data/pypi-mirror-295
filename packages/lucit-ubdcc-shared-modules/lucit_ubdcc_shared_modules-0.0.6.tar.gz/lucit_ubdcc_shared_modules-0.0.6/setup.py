#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: packages/lucit-ubdcc-shared-modules/setup.py
#
# Part of ‘UNICORN Binance DepthCache Cluster’
# Project website: https://www.lucit.tech/unicorn-binance-depthcache-cluster.html
# Github: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depthcache-cluster
# Documentation: https://unicorn-binance-depthcache-cluster.docs.lucit.tech
# PyPI: https://pypi.org/project/unicorn-binance-depthcache-cluster
# LUCIT Online Shop: https://shop.lucit.services/software
#
# License: LSOSL - LUCIT Synergetic Open Source License
# https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depthcache-cluster/blob/master/LICENSE
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2024-2024, LUCIT Systems and Development (https://www.lucit.tech)
# All rights reserved.

from Cython.Build import cythonize
from setuptools import setup

name = "lucit-ubdcc-shared-modules"
source_dir = "lucit_ubdcc_shared_modules"

# Setup
with open("README.md", "r") as fh:
    print("Using README.md content as `long_description` ...")
    long_description = fh.read()

setup(
    name=name,
    version="0.0.6",
    author="LUCIT Systems and Development",
    author_email='info@lucit.tech',
    url="https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depthcache-cluster",
    description="LUCIT UBDCC Mgmt Service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='LSOSL - LUCIT Synergetic Open Source License',
    install_requires=['lucit-licensing-python>=1.8.2', 'Cython'],
    keywords='',
    project_urls={
        'Howto': 'https://www.lucit.tech/unicorn-binance-depthcache-cluster.html#howto',
        'Documentation': 'https://unicorn-binance-depthcache-cluster.docs.lucit.tech',
        'Wiki': 'https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depthcache-cluster/wiki',
        'Author': 'https://www.lucit.tech',
        'Changes': 'https://unicorn-binance-depthcache-cluster.docs.lucit.tech/changelog.html',
        'License': 'https://unicorn-binance-depthcache-cluster.docs.lucit.tech/license.html',
        'Issue Tracker': 'https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depthcache-cluster/issues',
        'Chat': 'https://gitter.im/unicorn-trading-suite/unicorn-binance-depthcache-cluster',
        'Telegram': 'https://t.me/unicorndevs',
        'Get Support': 'https://www.lucit.tech/get-support.html',
        'LUCIT Online Shop': 'https://shop.lucit.services/software',
    },
    ext_modules=cythonize(['lucit_ubdcc_shared_modules/__init__.py',
                           'lucit_ubdcc_shared_modules/AppClass.py'],
                          compiler_directives={'language_level': "3"}),
    python_requires='>=3.12.0',
    package_data={'': ['lucit_ubdcc_shared_modules/*.so']},
    exclude_package_data={'': ['lucit_ubdcc_shared_modules/*.py']},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Cython",
        "License :: Other/Proprietary License",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: AsyncIO",
    ],
)
