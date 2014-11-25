# -*- coding: utf-8 -*-

##  Package pyprimes.py
##
##  Copyright © 2014 Steven D'Aprano.
##
##  Permission is hereby granted, free of charge, to any person obtaining
##  a copy of this software and associated documentation files (the
##  "Software"), to deal in the Software without restriction, including
##  without limitation the rights to use, copy, modify, merge, publish,
##  distribute, sublicense, and/or sell copies of the Software, and to
##  permit persons to whom the Software is furnished to do so, subject to
##  the following conditions:
##
##  The above copyright notice and this permission notice shall be
##  included in all copies or substantial portions of the Software.
##
##  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
##  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
##  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
##  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
##  CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
##  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
##  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""\
================
Package pyprimes
================

This package includes functions for generating prime numbers, primality
testing, and factorising numbers into prime factors.


Definitions
-----------

"Prime numbers" are positive integers with no factors other than themselves
and 1. The first few primes are 2, 3, 5, 7, 11, ...

"Composite numbers" are positive integers which do have factors other than
themselves and 1. Composite numbers can be uniquely factorised into the
product of two or more (possibly repeated) primes, e.g. 18 = 2*3*3.

Both 0 and 1 are neither prime nor composite.


Generating prime numbers
------------------------

To generate an unending stream of prime numbers, use the ``primes``
generator function:

    >>> p = primes()
    >>> [next(p) for _ in range(10)]
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


The ``next_prime`` and ``prev_prime`` functions return the next, or
previous, prime from some given value:

    >>> next_prime(20)
    23
    >>> prev_prime(20)
    19

    NOTE:: For large prime numbers p, the average distance between p and
           the next (or previous) prime is proportional to ln(p).

The ```xxxxx`` generator produces an unending sequence of True/False
flags for the integers, starting from zero, yielding True if the integer
is prime, and False if not prime. To generate tuples (n, primality of n),
zip the results against the integers:

    >>> pairs = zip(range(5), xxxcharf())
    >>> list(pairs)
    [(0, False), (1, False), (2, True), (3, True), (4, False)]


Primality testing
-----------------

To test whether an integer is prime or not, use ``is_prime``:

    >>> is_prime(10)
    False
    >>> is_prime(11)
    True

For extremely large values ``is_prime`` may be probabilistic. That is,
if it reports a number is prime, it may be only *almost certainly* prime,
with a very small chance that the number is actually composite. (If it
returns False, the number is certainly composite.)

The ``trial_division`` function also returns True for primes and False for
non-primes, unlike ``is_prime`` it is an exact test. However, it may be
slow for large values.

    >>> trial_division(15)
    False
    >>> trial_division(17)
    True


Number theory convenience functions
-----------------------------------

There are a few convenience functions from the Number Theory branch of
mathematics.

    nprimes:
        Return the first n primes.

    nth_prime:
        Return the nth prime.

    prime_count:
        Return the number of primes less than n.

    prime_sum:
        Return the sum of primes less than n.

    prime_partial_sums:
        Yield the sums of primes less than n.


Sub-modules
-----------

The pyprimes package also includes the following sub-modules:

    awful:
        Simple but inefficient, slow or otherwise awful algorithms for
        generating primes and testing for primality.

    factor:
        Factorise numbers into the product of primes.

    probabilistic:
        Generate and test for primes using probabilistic methods.

    sieves:
        Generate prime numbers using sieving algorithms.

    utilities:
        Assorted utility functions.

plus the following semi-private sub-modules:

    compat23:
        Internal compatibility layer, to support multiple versions of
        Python.

    tests:
        Unit and regression tests for the package.

The contents of the semi-private modules are subject to change or removal
without notice.
"""

from __future__ import division

import itertools
import warnings

from pyprimes2.compat23 import next



# Module metadata.
__version__ = "0.2.0a"
__date__ = "2014-09-11"
__author__ = "Steven D'Aprano"
__author_email__ = "steve+python@pearwood.info"


__all__ = ['is_prime', 'MaybeComposite', 'next_prime', 'nprimes',
           'nth_prime', 'prev_prime', 'prime_count', 'prime_partial_sums',
           'prime_sum', 'primes', 'trial_division',
          ]


class MaybeComposite(RuntimeWarning):
    pass


# === Prime numbers ===

def primes(start=0, end=None, gen=None):
    """Yield primes, optionally between ``start`` and ``end``.

    >>> list(primes(115, 155))
    [127, 131, 137, 139, 149, 151]

    If not given, ``start`` defaults to 0 and the first prime yielded will
    be 2. If not given, ``end`` defaults to None and the generator will
    yield primes with no upper limit.

    ``start`` is inclusive, and ``end`` is exclusive:

    >>> list(primes(5, 31))
    [5, 7, 11, 13, 17, 19, 23, 29]
    >>> list(primes(5, 32))
    [5, 7, 11, 13, 17, 19, 23, 29, 31]

    The optional argument ``gen`` is used to specify an alternative
    prime generator. If ``gen`` is not given or is None, the default
    implementation is used. Otherwise, ``gen`` must be a generator
    function which yields prime numbers, and ``primes`` behaves as a
    thin wrapper around that generator. No checks are made to ensure
    that ``gen`` actually produces prime numbers.

    >>> from pyprimes2.awful import turner  # Use a slow algorithm.
    >>> list(primes(6, 30, turner))
    [7, 11, 13, 17, 19, 23, 29]

    """
    if gen is None:
        from pyprimes2.sieves import best_sieve as gen
    primes = gen()
    # Consume the primes below start as fast as possible.
    p = next(primes)
    while p < start:
        p = next(primes)
    # Then yield until end.
    while (end is None) or (p < end):
        yield p
        p = next(primes)


def next_prime(n, isprime=None):
    """Return the first prime number strictly greater than n.

    >>> next_prime(97)
    101

    For sufficiently large n, over approximately 341 trillion, the result
    may be only probably prime rather than certainly prime.

    Optional argument ``isprime`` is used for testing whether values are
    prime or not. If given, it should be a function which takes a single
    integer value and returns a true object for primes and a false object
    for non-primes. If ``isprime`` is None, or not given, the primality
    tester ``is_prime`` is used by default.

    The average gap between a prime number p and the next prime is log p.
    """
    if isprime is None:
        isprime = is_prime
    if n < 2:
        return 2
    if n % 2 == 0:
        # Even numbers.
        n += 1
    else:
        # Odd numbers.
        n += 2
    while not is_prime(n):
        n += 2
    return n


def prev_prime(n, isprime=None):
    """Return the first prime number strictly less than n.

    >>> prev_prime(100)
    97

    If there are no primes less than n, raises ValueError.

    For sufficiently large n, over approximately 341 trillion, the result
    may be only probably prime rather than certainly prime.

    Optional argument ``isprime`` is used for testing whether values are
    prime or not. If given, it should be a function which takes a single
    integer value and returns a true object for primes and a false object
    for non-primes. If ``isprime`` is None, or not given, the primality
    tester ``is_prime`` is used by default.

    The average gap between a prime number p and the next prime is log p.
    """
    if isprime is None:
        isprime = is_prime
    if n <= 2:
        raise ValueError('smallest prime is 2')
    if n % 2 == 1:
        # Odd numbers.
        n -= 2
    else:
        # Even numbers.
        n -= 1
    while not isprime(n):
        n -= 2
    return n


def xxxcharf():
    """xxxcharf() -> yield is_prime(n) for all n >= 0

    With the addition of the first term, for n=0, this is equivalent
    to the characteristic function:

    χ[primes] = 1 if n is prime else 0

    yielding True for primes and False for non-primes:

    >>> it = xxxcharf()
    >>> [next(it) for _ in range(6)]
    [False, False, True, True, False, True]

    For brevity, or to match the mathematical definition of the
    characteristic function, call ``int()`` on the results:

    >>> [int(next(it)) for _ in range(20)]
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0]

    """
    # http://oeis.org/A010051
    # See also: http://mathworld.wolfram.com/PrimeConstant.html
    for flag in (False, False, True, True):  # n = 0, 1, 2, 3.
        yield flag
    it = primes(5)
    q = 3  # Previously yielded prime number.
    for p in it:
        # Process the non-primes between q and p.
        for _ in range(p - q - 1):
            yield False
        # Process the prime.
        yield True
        q = p


# === Primality testing ===

def is_prime(n, prover=None):
    """Return True if n is probably a prime number, and False if it is not.

    >>> is_prime(103)
    True
    >>> is_prime(105)
    False

    The optional argument ``prover`` is used to specify alternative
    algorithms for checking primality. If ``prover`` is not given or
    is None, the default implementation is used. Otherwise, ``prover``
    must be a function which takes a single integer and returns a flag
    specifying whether the integer is prime or not, and ``is_prime``
    behaves as a thin wrapper around that function. No checks are made
    to ensure that ``prover`` actually tests for prime numbers.

    If given, ``prover`` should return one of:

        0 or False      Number is definitely composite.
        1 or True       Number is definitely prime.
        2               Number is a probable prime or pseudoprime.

    Any other value will raise TypeError or ValueError.

    With the default prover, ``is_prime`` may be probabilistic rather
    than deterministic for sufficiently large numbers. If that is the
    case, ``is_prime`` will give a ``MaybeComposite`` warning if ``n``
    is only probably prime rather than certainly prime. By default, the
    probability of a randomly choosen value being mistakenly identified
    as prime when it is actually composite (a false positive error) is
    less than 1e-18 (1 chance in a million million million).

    There are no false negative errors: if ``is_prime`` returns False,
    then the number is certainly composite.
    """
    if prover is None:
        from pyprimes2.probabilistic import is_probable_prime as prover
    flag = prover(n)
    if flag is True or flag is False:
        return flag
    # Check for actual ints, not subclasses. Gosh this takes me back to
    # Python 1.5 days...
    if type(flag) is int:
        if flag in (0, 1, 2):
            if flag == 2:
                message = "%d is only only probably prime" % n
                import warnings
                warnings.warn(message, MaybeComposite)
            return bool(flag)
        raise ValueError('prover returned invalid int flag %d' % flag)
    raise TypeError('expected bool or int but prover returned %r' % flag)


def trial_division(n, gen=None):
    """trial_division(n) -> True|False

    By default, an exact but slow primality test using trial division by
    primes only. It returns True if the argument is a prime number,
    otherwise False.

    >>> trial_division(11)
    True
    >>> trial_division(12)
    False

    For large values of n, this may be slow or run out of memory.

    If given, optional argument ``gen`` should be a generator yielding
    prime numbers. See the ``primes`` function for further details.
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    limit = n**0.5  # FIXME
    for divisor in primes(gen=gen):
        if divisor > limit: break
        if n % divisor == 0: return False
    return True


# === Number theory convenience functions ===

def nprimes(n, gen=None):
    """Convenience function that yields the first n primes only.

    >>> list(nprimes(10))
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    If given, optional argument ``gen`` should be a generator yielding
    prime numbers. See the ``primes`` function for further details.
    """
    return itertools.islice(primes(gen=gen), n)


def nth_prime(n, gen=None):
    """nth_prime(n) -> int

    Return the nth prime number, starting counting from 1. Equivalent to
    p[n] (p subscript n) in standard maths notation.

    >>> nth_prime(1)  # First prime is 2.
    2
    >>> nth_prime(5)
    11
    >>> nth_prime(50)
    229

    If given, optional argument ``gen`` should be a generator yielding
    prime numbers. See the ``primes`` function for further details.
    """
    # http://oeis.org/A000040
    if n < 1:
        raise ValueError('argument must be a positive integer')
    return next(itertools.islice(primes(gen=gen), n-1, n))


def prime_count(n, gen=None):
    """prime_count(n) -> int

    Returns the number of prime numbers less than or equal to n.
    It is also known as the Prime Counting Function, or π(n).
    (Not to be confused with the constant pi π = 3.1415....)

    >>> prime_count(20)
    8
    >>> prime_count(10000)
    1229

    The number of primes less than x is approximately n/(ln n - 1).

    If given, optional argument ``gen`` should be a generator yielding
    prime numbers. See the ``primes`` function for further details.
    """
    # See also:  http://primes.utm.edu/howmany.shtml
    # http://mathworld.wolfram.com/PrimeCountingFunction.html
    # http://oeis.org/A000720
    if n < 1:
        return 0
    return sum(1 for p in primes(end=n+1, gen=gen))

""" π(10) == 4
    π(100) == 25
    π(1000) == 168
    π(10000) == 1229
    π(100000) == 9592
    π(10**6) == 78498
    π(10**7) == 664579
    """


def prime_sum(n, gen=None):
    """prime_sum(n) -> int

    prime_sum(n) returns the sum of the first n primes.

    >>> prime_sum(9)
    100
    >>> prime_sum(49)
    4888

    The sum of the first n primes is approximately n**2*(ln n)/2.

    If given, optional argument ``gen`` should be a generator yielding
    prime numbers. See the ``primes`` function for further details.
    """
    # See:  http://mathworld.wolfram.com/PrimeSums.html
    # http://oeis.org/A007504
    if n < 1:
        return 0
    return sum(nprimes(n, gen))


def prime_partial_sums(gen=None):
    """Yield the partial sums of the prime numbers.

    >>> p = prime_partial_sums()
    >>> [next(p) for _ in range(6)]  # primes 2, 3, 5, 7, 11, ...
    [0, 2, 5, 10, 17, 28]

    If given, optional argument ``gen`` should be a generator yielding
    prime numbers. See the ``primes`` function for further details.
    """
    # http://oeis.org/A007504
    n = 0
    for p in primes(gen=gen):
        yield n
        n += p

