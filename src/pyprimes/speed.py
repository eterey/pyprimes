# -*- coding: utf-8 -*-

##  Part of the pyprimes.py package.
##
##  Copyright © 2014 Steven D'Aprano.
##  See the file __init__.py for the licence terms for this software.

"""\
=====================================
Timing the speed of primes algorithms
=====================================



"""

from __future__ import division

import sys
from itertools import islice

# Conditionally hack the PYTHONPATH.
if __name__ == '__main__':
    import os
    path = os.path.dirname(__file__)
    parent, here = os.path.split(path)
    sys.path.append(parent)

from pyprimes2.compat23 import next

import pyprimes2.awful as awful
import pyprimes2.probabilistic as probabilistic
import pyprimes2.sieves as sieves



YEAR100 = 100*365*24*60*60  # One hundred years, in seconds.

class Stopwatch(object):
    def __init__(self, timer=None):
        if timer is None:
            from timeit import default_timer as timer
        self.timer = timer
        self.reset()

    def reset(self):
        """Reset all the collected timer results."""
        try:
            del self._start
        except AttributeError:
            pass
        self._elapsed = 0.0

    def start(self):
        """Start the timer."""
        self._start = self.timer()

    def stop(self):
        """Stop the timer."""
        t = self.timer()
        self._elapsed = t - self._start
        del self._start

    @property
    def elapsed(self):
        return self._elapsed


def trial(generator, count, repeat=1):
    timer = Stopwatch()
    best = YEAR100
    for i in range(repeat):
        it = generator()
        timer.reset()
        timer.start()
        # Go to the count-th prime as fast as possible.
        p = next(islice(it, count-1, count))
        timer.stop()
        best = min(best, timer.elapsed)
    return best


def run(generators, number, repeat=1):
    print ("Calculating speeds for first %d primes..." % number)
    template = "\r  ...%d of %d %s"
    heading = """\
Generator                             Elapsed    Speed
                                      (sec)      (primes/sec)
=============================================================="""
    records = []
    timer = Stopwatch()  # For measuring the total elapsed time.
    timer.start()
    N = len(generators)
    for i, generator in enumerate(generators):
        name = generator.__module__ + '.' + generator.__name__
        sys.stdout.write((template % (i+1, N, name)).ljust(69))
        sys.stdout.flush()
        t = trial(generator, number, repeat)
        records.append((number/t, t, name))
    timer.stop()
    sys.stdout.write("\r%-69s\n" % "Done!")
    print ('Total elapsed time: %.1f seconds' % timer.elapsed)
    print ('')
    records.sort()
    print (heading)
    for speed, elapsed, name in records:
        print ("%-36s  %4.2f      %8.1f" % (name, elapsed, speed))
    print ('==============================================================\n')


VERY_SLOW = [awful.primes0, awful.primes1, awful.primes2, awful.turner]
SLOW = [awful.primes3, awful.primes4, probabilistic.primes]
FAST = [sieves.cookbook, sieves.croft, sieves.sieve, sieves.wheel]
MOST = SLOW + FAST
ALL = VERY_SLOW + MOST

run(VERY_SLOW + SLOW, 1000)
run([awful.primes3, awful.trial_division], 5000)
#run([awful.primes3, awful.trial_division], 50000)
#run([awful.primes3, awful.trial_division], 100000)
#run([awful.primes3, awful.trial_division], 200000)
exit()


run(ALL, 500, 3)
run(MOST, 10000)
run(FAST, 1000000)




"""
Python 2.6 or better

import multiprocessing
import time

# bar
def bar():
    for i in range(100):
        print "Tick"
        time.sleep(1)

if __name__ == '__main__':
    # Start bar as a process
    p = multiprocessing.Process(target=bar)
    p.start()

    # Wait for 10 seconds or until process finishes
    p.join(10)

    # If thread is still active
    if p.is_alive():
        print "running... let's kill it..."

        # Terminate
        p.terminate()
        p.join()

"""



"""

Unix only, Python 2.5 or better.


In [1]: import signal

# Register an handler for the timeout
In [2]: def handler(signum, frame):
   ...:     print "Forever is over!"
   ...:     raise Exception("end of time")
   ...:

# This function *may* run for an indetermined time...
In [3]: def loop_forever():
   ...:     import time
   ...:     while 1:
   ...:         print "sec"
   ...:         time.sleep(1)
   ...:
   ...:

# Register the signal function handler
In [4]: signal.signal(signal.SIGALRM, handler)
Out[4]: 0

# Define a timeout for your function
In [5]: signal.alarm(10)
Out[5]: 0

In [6]: try:
   ...:     loop_forever()
   ...: except Exception, exc:
   ...:     print exc
   ....:
sec
sec
sec
sec
sec
sec
sec
sec
Forever is over!
end of time

# Cancel the timer if the function returned before timeout
# (ok, mine won't but yours maybe will :)
In [7]: signal.alarm(0)
Out[7]: 0

"""



