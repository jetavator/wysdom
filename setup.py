# -*- coding: utf-8 -*-

import io
import os

from setuptools import setup, find_packages

# Package metadata
# ----------------

NAME = 'wysdom'
DESCRIPTION = (
    'A Python library for building custom document object '
    'models (DOMs) with built-in JSON schema checking'
)
URL = 'https://github.com/jetavator/wysdom'
EMAIL = 'joetaylorconsulting@gmail.com'
AUTHOR = 'Joe Taylor'
REQUIRES_PYTHON = '>=3.7.0'
VERSION = None

# What packages are required for this module to be executed?
REQUIRED = [
    'jsonschema>=3.2.0,<4',
    'pyyaml>=5.3.1,<6'
]

# What packages are optional?
EXTRAS = {
    # 'some-feature': ['requirement'],
}

# Package setup
# -------------

# Import the README and use it as the long description

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Import the LICENSE

with open(os.path.join(here, 'LICENSE')) as f:
    license = f.read()

# Load the package's __version__.py module as a dictionary

about = {}
if not VERSION:
    with open(os.path.join(here, NAME, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    project_urls={
        "Documentation": "https://wysdom.readthedocs.io/en/latest/"
    },
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
