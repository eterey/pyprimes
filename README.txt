===========================================
pyprimes -- generate and test prime numbers
===========================================


Introduction
------------

pyprimes is a pure-Python package for generating and testing prime numbers.

Prime numbers are those positive integers which are not divisible exactly
by any number other than itself or one. Generating primes and testing for
primality has been a favourite mathematical pastime for centuries, as well
as of great practical importance for encrypting data.

Features of ``pyprimes``:

    - Produce prime numbers lazily, on demand.
    - Effective, fast algorithms including Sieve of Eratosthenes,
      Croft Spiral, and Wheel Factorisation.
    - Test whether numbers are prime efficiently.
    - Deterministic and probabilistic primality tests.
    - Examples of what *not* to do provided, including naive trial
      division, Turner's algorithm (Euler's sieve), and primality
      testing using a regular expression.
    - Factorise small numbers into the product of prime factors.
    - Suitable for Python 2.4 through 3.x from one code base.


Installation
------------

To install, extract the tarball into the current directory, then cd into the
expanded directory. Run:

    $ python setup.py install

from your system shell (not the python interpreter) to install.


Licence
-------

pyprimes is licenced under the MIT Licence. See the LICENCE.txt file and the
header of pyprimes/__init__.py.


Test suite
----------

pyprimes comes with an extensive test suite. Run the pyprimes/tests.py module
to run the test suite.

For Python version 2.5 on up, the most convenient way to do this is from your
system shell:

    $ python -m pyprimes.test

To get even more verbose output, pass the -v switch:

    $ python -m pyprimes.test -v

The -m switch is not supported by Python 2.4, to run the test suite under
that version you will have to give the path to the test module and run it
manually.


Known Issues
------------

With older versions of Python (2.4 - 2.6), doctests are not run when
running the test suite. You can run them manually for each individual
module, e.g.:

    $ python2.6 -m doctest pyprimes/factors.py -v


