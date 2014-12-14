"""

The prime characteristic function returns an unending sequence of True or
False

The ```characteristic`` generator produces an unending sequence of True/False
flags for the integers, starting from zero, yielding True if the integer
is prime, and False if not prime. To generate tuples (n, primality of n),
use ``enumerate()`` or zip the results against a range of integers:

    >>> pairs = zip(range(5), characteristic())
    >>> list(pairs)
    [(0, False), (1, False), (2, True), (3, True), (4, False)]


"""


def characteristic(start=0, end=None, strategy=None):
    """Yield is_prime(n) for all integers between ``start`` and ``end``.

    This is closely equivalent to the mathematical "characteristic function"
    defined as:

        χ[n] = 1 if n is prime, otherwise 0

    for n > 0, except this yields True for primes and False for non-primes
    rather than 1 and 0, and by default it begins with n=0:

    #>>> it = characteristic()
    #>>> [next(it) for _ in range(6)]
    [False, False, True, True, False, True]

    To use 1 and 0 instead, call ``int()`` on the results:

    #>>> [int(next(it)) for _ in range(20)]
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0]

    Optional arguments ``start`` and ``end`` specify the first (included)
    and last (excluded) value. ``start`` defaults to 0, and ``end`` defaults
    to None (no upper limit, yield values forever).

    #>>> list(map(int, characteristic(start=7, end=31)))
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0]

    ``strategy``, if given, is an alternate implementation used to generate
    prime numbers. See the documentation for ``primes`` for more detail.

    """
    # http://oeis.org/A010051
    # See also: http://mathworld.wolfram.com/PrimeConstant.html
    if start is None:
        start = 0
    q = start  # Later this will be the previously seen prime.
    for p in primes(start, end, strategy):
        # Process the non-primes between q and p. On average, there are
        # about ln(p) non-primes between prime p and the next (or previous)
        # so using range() is manageable until we have unbelievably huge
        # primes.
        for i in range(p-q-1):  # Like range(q+1, p).
            yield False
        # Process the prime.
        yield True
        q = p
    if end is not None:
        for i in range(end-p-1):  # Like range(p+1, end).
            yield False



'''
class TestCheckedInts(unittest.TestCase):
    def testIsIterator(self):
        it = pyprimes.checked_ints()
        self.assertTrue(it is iter(it))

    def testValues(self):
        n = PRIMES[-1] + 2
        expected = [(True, i) for i in PRIMES]
        x = set(range(n)).difference(set(PRIMES))
        expected.extend((False, i) for i in x)
        expected.sort(key=lambda obj: obj[1])
        actual = list(itertools.islice(pyprimes.checked_ints(), None, n))
        self.assertEqual(actual, expected)


class TestCheckedOddInts(unittest.TestCase):
    def testIsIterator(self):
        it = pyprimes.checked_ints()
        self.assertTrue(it is iter(it))

    def testValues(self):
        n = PRIMES[-1] + 2
        expected = [(True, i) for i in PRIMES[1:]]
        x = set(range(1, n, 2)).difference(set(PRIMES))
        expected.extend((False, i) for i in x)
        expected.sort(key=lambda obj: obj[1])
        actual = list(itertools.islice(pyprimes.checked_oddints(), None, n))
        self.assertEqual(actual, expected)
'''

