"""
See https://enigmaticcode.wordpress.com/2015/07/22/enigma-1216-chain-of-primes/

13 solutions
"""

from pycsp3 import *

n = 10

primes = [v for v in all_primes(100) if v > 10]

x = VarArray(size=n, dom=range(11, 100))

satisfy(
    AllDifferent(x),
    [x[i] in primes for i in range(n)],
    [x[i] // 10 == x[i - 1] % 10 for i in range(2, n)],
    [(y % 10 == z // 10) & (y // 10 == z % 10) for y, z in [(x[3], x[0]), (x[6], x[9])]]
)
