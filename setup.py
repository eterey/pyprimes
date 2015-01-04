#! /usr/bin/env python3

from distutils.core import setup

# Futz with the path so we can import metadata.
import os, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, 'src'))
from pyprimes import __version__, __author__, __author_email__

# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs')
    codecs.register(func)


setup(
    name = "pyprimes",
    package_dir={'': 'src'},
    packages = ['pyprimes'],
    version = __version__,
    author = __author__,
    author_email = __author_email__,
    url = 'http://code.google.com/p/pyprimes/',
    keywords = "prime primes primality math maths algorithm fermat miller-rabin".split(),
    description = "Generate and test for prime numbers.",
    long_description = """\
The pyprimes package offers a variety of algorithms for generating prime
numbers and fast primality test, written in pure Python.

Prime numbers are those positive integers which are not divisible exactly
by any number other than itself or one. Generating primes and testing for
primality has been a favourite mathematical pastime for centuries, as well
as of great practical importance for encrypting data.

``pyprimes`` includes the following features:

    - Produce prime numbers lazily, on demand.
    - Effective algorithms including Sieve of Eratosthenes, Croft Spiral,
      and Wheel Factorisation.
    - Efficiently test whether numbers are prime, using both deterministic
      (exact) and probabilistic primality tests.
    - Examples of what *not* to do are provided, including naive trial
      division, Turner's algorithm, and primality testing using a
      regular expression.
    - Factorise small numbers into the product of prime factors.
    - Suitable for Python 2.4 through 3.2 from one code base.

""",
    license = 'MIT',  # apologies for the American spelling
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        ],
    )

