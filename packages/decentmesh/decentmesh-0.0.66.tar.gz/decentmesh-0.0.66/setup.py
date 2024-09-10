#!/usr/decentmesh/env python3

import os

from setuptools import setup, find_packages

# get key package details from decentmesh/__version__.py
about = {}  # type: ignore
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "decentnet", "__version__.py")) as f:
    exec(f.read(), about)

# load the README file and use it as the long_description for PyPI
with open("README.md", "r") as f:
    readme = f.read()

setup(
    name=about["__title__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.11,<4",
    install_requires=[
        "alembic==1.13.2",
        "argon2-cffi==23.1.0",
        "argon2-cffi-bindings==21.2.0",
        "asn1crypto==1.5.1",
        "Brotli==1.1.0",
        "cffi==1.17.0",
        "click==8.1.7",
        "coincurve==19.0.1",
        "colorama==0.4.6",
        "cryptography==43.0.0",
        "Cython==3.0.11",
        "cytoolz==0.12.3",
        "ecdsa==0.19.0",
        "eciespy==0.4.2",
        "eth-hash==0.5.2",
        "eth-keys==0.4.0",
        "eth-typing==3.5.2",
        "eth-utils==2.3.1",
        "greenlet==3.0.2",
        "lz4==4.3.2",
        "Mako==1.3.0",
        "markdown-it-py==3.0.0",
        "MarkupSafe==2.1.3",
        "mdurl==0.1.2",
        "networkx==3.2.1",
        "pycparser==2.22",
        "pycryptodome==3.20.0",
        "Pygments==2.17.2",
        "pylzma==0.5.0",
        "rich==13.8.0",
        "setuptools==74.0.0",
        "six==1.16.0",
        "SQLAlchemy==2.0.32",
        "toolz==0.12.1",
        "typing_extensions==4.12.2",
        "pymysql==1.1.1",
        "prometheus_client==0.20.0",
        "cbor2~=5.6.4",
        "netifaces==0.11.0",
        "qrcode==7.4.2",
        "sentry-sdk==2.13.0",
        "aiosqlite==0.20.0"
    ],
    extras_require={
        "dev": ["black==22.*"],
    },
    license=about["__license__"],
    zip_safe=True,
    entry_points={
        "console_scripts": ["decentmesh=decentnet.main:main"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="Decentralized P2P Network",
)
