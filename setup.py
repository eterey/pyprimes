#! /usr/bin/env python3

from distutils.core import setup

# Futz with the path so we can import metadata.
import sys
sys.path.insert(0, './src')
from pyprimes import __version__, __author__, __author_email__

setup(
    name = "pyprimes",
    py_modules=["pyprimes"],
    version = __version__,
    author = __author__,
    author_email = __author_email__,
    url = 'http://pypi.python.org/pypi/pyprimes',
    keywords = "prime primes math maths algorithm fermat miller-rabin".split(),
    description = "Generate and test for prime numbers.",
    long_description = """\
Generate and test for prime numbers
-----------------------------------

Requires Python 2.5 or better.
""",
    license = 'MIT',  # apologies for the American spelling
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        ],
    )

