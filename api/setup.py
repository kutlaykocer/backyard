#!/usr/bin/env python3
from setuptools import setup, find_packages
import os

setup(
    name = "backyard.api",
    version = "1.0",
    author = "GONICUS GmbH",
    author_email = "info@gonicus.de",
    description = "",

    packages = find_packages('src', exclude=['examples', 'tests']),
    package_dir={'': 'src'},
    namespace_packages = ['backyard'],

    include_package_data = True,
    # package_data = {
    #     'backyard.api': data_files
    # },

    zip_safe = False,

    setup_requires = [
        'pylint',
        ],
    tests_require = [
        'pytest',
    ],
    install_requires = [
        'protobuf',
        'asyncio-nats-client',
        'connexion',
        'connexion[swagger-ui]',
        'python_dateutil',
        'decorator'
        ],

    entry_points = """
        [console_scripts]
        backyard-api = backyard.api.__main__:main
        rest-api = backyard.api.rest.__main__:main
    """,
)
