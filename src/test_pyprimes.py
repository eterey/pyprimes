"""Test suite for pyprimes.py
"""
from __future__ import division

import doctest
import itertools
import sys
import unittest

if sys.version < '3':
    import __builtin__ as builtins
else:
    import builtins

try:
    next
except NameError:
    # Python 2.5.
    def next(it):
        return it.next()


# Module being tested.
import pyprimes


# Automatically load doctests.
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(pyprimes))
    return tests


# First 100 primes from here:
# http://en.wikipedia.org/wiki/List_of_prime_numbers
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
          67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137,
          139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
          211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277,
          281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359,
          367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439,
          443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521,
          523, 541]


# === Test suites ===

class MetadataTest(unittest.TestCase):
    module = pyprimes
    expected_metadata = [
        "__version__", "__date__", "__author__", "__author_email__",
        "__doc__", "__all__",
        ]

    def testCheckAll(self):
        module = self.module
        # Check everything in __all__ exists.
        for name in module.__all__:
            # No private names in __all__:
            self.assertFalse(name.startswith("_"),
                             'private name "%s" in __all__' % name)
            # And anything in __all__ must exist:
            self.assertTrue(hasattr(module, name),
                            'missing name "%s" in __all__' % name)

    def testMeta(self):
        # Test for the existence of metadata.
        module = self.module
        for meta in self.expected_metadata:
            self.assertTrue(hasattr(module, meta), "%s not present" % meta)


class CompatibilityLayerTest(unittest.TestCase):
    # Test the 2.x/3.x compatibility later.

    def is_iterator(self, func, *args, **kw):
        # Test that fun(*args, **kw) does not return a list but returns a
        # lazy iterator instead.
        obj = func(*args, **kw)
        nm = func.__name__
        self.assertFalse(isinstance(obj, list), "%s returns a list" % nm)
        self.assertTrue(iter(obj))  # FIXME

    def testNext(self):
        # next must be either a builtin or provided by the module itself.
        if hasattr(pyprimes, 'next'):
            f = pyprimes.next
            it = iter([1, 'a'])
            self.assertEqual(f(it), 1)
            self.assertEqual(f(it), 'a')
            self.assertRaises(StopIteration, f, it)
        else:
            # Testing the behaviour of builtin next is not our responsibility;
            # we test for existence and nothing else.
            self.assertTrue(
                hasattr(builtins, 'next'),
                "expected builtin ``next``, but not found"
                )

    def testRange(self):
        # range must be either a builtin or shadowed by the module itself;
        # either way, we expect it to be a lazy iterator.
        if hasattr(pyprimes, 'range'):
            # This must come first, to avoid Python 2.x eager range shadowing
            # the version in the module.
            f = pyprimes.range
        else:
            f = builtins.range
        self.is_iterator(f, 3)
        self.assertEqual(list(f(5)), [0, 1, 2, 3, 4])
        self.assertEqual(list(f(5, 10)), [5, 6, 7, 8, 9])
        self.assertEqual(list(f(5, 15, 3)), [5, 8, 11, 14])

    def testFilter(self):
        # filter must be either a builtin or shadowed by the module itself;
        # either way, we expect it to be a lazy iterator.
        if hasattr(pyprimes, 'filter'):
            f = pyprimes.filter
        else:
            f = builtins.filter
        self.is_iterator(f, None, [1, 2, 3])

    def testZip(self):
        # zip must be either a builtin or shadowed by the module itself;
        # either way, we expect it to be a lazy iterator.
        if hasattr(pyprimes, 'zip'):
            f = pyprimes.zip
        else:
            f = builtins.zip
        self.is_iterator(f, "abc", [1, 2, 3])

    def testCompress(self):
        pyprimes.compress

    def testIsfinite(self):
        pyprimes.isfinite


class ValidateIntTest(unittest.TestCase):
    # Test the _validate_int private function.
    func = (pyprimes._validate_int,)  # Avoid converting to a method.

    def testNonNumbers(self):
        func = self.func[0]
        for obj in ('abc', '1234', None, (), [], {}, set()):
            self.assertRaises(TypeError, func, obj)

    def testNonIntegers(self):
        func = self.func[0]
        for obj in (1.5, -2.5):
            self.assertRaises(ValueError, func, obj)

    def testINF(self):
        func = self.func[0]
        inf = float('inf')
        self.assertRaises(OverflowError, func, inf)
        self.assertRaises(OverflowError, func, -inf)

    def testNAN(self):
        func = self.func[0]
        nan = float('nan')
        self.assertRaises(ValueError, func, nan)

    def testIntegers(self):
        func = self.func[0]
        for n in (0, -1, -2, 1, 99, 1001.0, 1e99, -5e50):
            self.assertTrue(func(n) is None)


class ValidateNumTest(ValidateIntTest):
    # Test the _validate_num private function.
    func = (pyprimes._validate_num,)  # Avoid converting to a method.

    def testNonIntegers(self):
        func = self.func[0]
        for obj in (1.5, -2.5):
            self.assertTrue(func(obj) is None)

    def testINF(self):
        func = self.func[0]
        inf = float('inf')
        self.assertRaises(ValueError, func, inf)
        self.assertRaises(ValueError, func, -inf)


class BasesTest(unittest.TestCase):
    # Test private function _base_to_bases.

    def testSingleBase(self):
        for i in range(1, 42):
            self.assertEqual(pyprimes._base_to_bases(i, 42), (i,))

    def testMultipleBases(self):
        f = pyprimes._base_to_bases
        self.assertEqual(f((23, 42), 200), (23, 42))
        self.assertEqual(f((147, 291, 813), 1000), (147, 291, 813))

    def testSingleBaseOutOfRange(self):
        for i in (-5, -1, 0, 23, 50):
            self.assertRaises(ValueError, pyprimes._base_to_bases, i, 23)

    def testMultipleBasesOutOfRange(self):
        for i in (-3, -1, 0, 25, 30):
            self.assertRaises(ValueError, pyprimes._base_to_bases, (2, i), 25)


class EratTest(unittest.TestCase):
    # Test the erat function.
    def __init__(self, *args, **kw):
        unittest.TestCase.__init__(self, *args, **kw)
        self.func = pyprimes.erat

    def testFloat(self):
        self.assertRaises(ValueError, self.func, 10.5)

    def testFloatSpecials(self):
        self.assertRaises(OverflowError, self.func, float('inf'))
        self.assertRaises(OverflowError, self.func, -float('inf'))
        self.assertRaises(ValueError, self.func, float('nan'))

    def testBadTypes(self):
        for obj in (None, (), [], {}, set(), "abc"):
            self.assertRaises(TypeError, self.func, obj)

    def testReturn(self):
        # Check that erat returns a list.
        self.assertTrue(isinstance(self.func(10), list))

    def testEmptyPrimes(self):
        # Test erat returns an empty list when appropriate.
        for i in (-10, -2, -1, 0, 1):
            self.assertEquals(self.func(i), [])

    def _primes_below(self, n):
        for i in range(len(PRIMES)):
            if PRIMES[i] > n:
                return PRIMES[0:i]
        return PRIMES

    def testPrimes(self):
        for i in range(2, 544):
            self.assertEqual(self.func(i), self._primes_below(i))


class GeneratorMixin:
    """Mixin class for common tests for iterator-based prime generators."""

    def testIsIterator(self):
        it = self.func()
        self.assertTrue(it is iter(it))

    def testPrimes(self):
        it = self.func()
        values = [next(it) for _ in range(100)]
        self.assertEqual(values, PRIMES)


class TestSieve(unittest.TestCase, GeneratorMixin):
    def __init__(self, *args, **kw):
        unittest.TestCase.__init__(self, *args, **kw)
        self.func = pyprimes.sieve


class TestCookbook(unittest.TestCase, GeneratorMixin):
    def __init__(self, *args, **kw):
        unittest.TestCase.__init__(self, *args, **kw)
        self.func = pyprimes.cookbook


class TestCroft(unittest.TestCase, GeneratorMixin):
    def __init__(self, *args, **kw):
        unittest.TestCase.__init__(self, *args, **kw)
        self.func = pyprimes.croft


class TestWheel(unittest.TestCase, GeneratorMixin):
    def __init__(self, *args, **kw):
        unittest.TestCase.__init__(self, *args, **kw)
        self.func = pyprimes.wheel


class TestPrimes(unittest.TestCase, GeneratorMixin):
    def __init__(self, *args, **kw):
        unittest.TestCase.__init__(self, *args, **kw)
        self.func = pyprimes.primes


class TestAwfulPrimes(unittest.TestCase, GeneratorMixin):
    def __init__(self, *args, **kw):
        unittest.TestCase.__init__(self, *args, **kw)
        self.func = pyprimes.awful_primes


class TestNaivePrimes1(unittest.TestCase, GeneratorMixin):
    def __init__(self, *args, **kw):
        unittest.TestCase.__init__(self, *args, **kw)
        self.func = pyprimes.naive_primes1


class TestNaivePrimes2(unittest.TestCase, GeneratorMixin):
    def __init__(self, *args, **kw):
        unittest.TestCase.__init__(self, *args, **kw)
        self.func = pyprimes.naive_primes2


class TestTrialDivision(unittest.TestCase, GeneratorMixin):
    def __init__(self, *args, **kw):
        unittest.TestCase.__init__(self, *args, **kw)
        self.func = pyprimes.trial_division


class TestTurner(unittest.TestCase, GeneratorMixin):
    def __init__(self, *args, **kw):
        unittest.TestCase.__init__(self, *args, **kw)
        self.func = pyprimes.turner


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



if __name__ == '__main__':
    unittest.main()


