"""
  Place the numbers 1 to 14 around a circle so that both the sum and
  the (positive difference) of any two neighboring numbers is a prime.

  try with n=50 for both variants
"""

from pycsp3 import *

n = data or 22

primes = all_primes(n * 2)

x = VarArray(size=n, dom=range(1, n + 1))

satisfy(
    AllDifferent(x),

    # tag(symmetry-breaking)
    x[0] == 1
)

if not variant():
    satisfy(
        [x[i] + x[(i + 1) % n] in primes for i in range(n)],

        [abs(x[i] - x[(i + 1) % n]) in primes for i in range(n)]
    )

elif variant("table"):
    T = {(a, b) for a in range(1, n + 1) for b in range(1, n + 1) if a + b in primes and abs(a - b) in primes}

    satisfy(
        (x[i], x[(i + 1) % n]) in T for i in range(n)
    )
