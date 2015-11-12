===========================================
pyprimes -- generate and test prime numbers
===========================================


Introduction
------------

Prime numbers are those positive integers which are not divisible exactly
by any number other than itself or one. Generating primes and testing for
primality has been a favourite mathematical pastime for centuries, as well
as of great practical importance for encrypting data. The ``pyprimes``
package provides functions for generating prime numbers on the fly and
testing whether or not a given number is prime.

Features include:

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

    python setup.py install

from your system shell (not the python interpreter) to install.


Licence
-------

pyprimes is licenced under the MIT Licence. See the LICENCE.txt file and the
header of pyprimes/__init__.py.


Test suite
----------

pyprimes comes with an extensive test suite containing unit tests, doc tests
and regression tests. To run the test suite, run the ``pyprimes/tests.py``
module.

For Python version 2.5 on up, the most convenient way to do this after
installation is from your system shell:

    python -m pyprimes.test

To get even more verbose output, pass the -v switch:

    python -m pyprimes.test -v

The -m switch is not supported by Python 2.4, to run the test suite under
that version you will have to give the path to the test module and run it
manually. E.g. this may work on some systems:

    cd /usr/lib/python2.4
    python2.4 pyprimes/test.py


Known Issues and Bugs
---------------------

(1) The API of this package is not yet stable. That means that the names of
    functions, the arguments that they take, values returned, etc. may
    change without warning in the future.

(2) With older versions of Python (2.4 - 2.6), doctests are not run when
    running the test suite. You can run them manually for each individual
    module, e.g.:

        python2.6 -m doctest pyprimes/factors.py -v

(3) In general, prime-related functions expect their numeric arguments to
    be integers, but don't perform any type-checking. If you pass a float,
    Decimal, Fraction or other non-int (or long) value, behaviour is
    undefined.

(4) The package is currently rather inconsistent in whether it uses
    floating point sqrt or integer-valued sqrt. This should be considered
    a known bug.

