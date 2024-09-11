"""
What is the smallest difference between two numbers v1 - v2
if you must use all the digits (0..9) exactly once, i.e.
when minimizing the difference ABCDE - FGHIJ
"""

from pycsp3 import *

bases = [10 ** (4 - i) for i in range(5)]

x = Var(range(10 ** 6))

y = Var(range(10 ** 6))

dx = VarArray(size=5, dom=range(10))

dy = VarArray(size=5, dom=range(10))

satisfy(
    x == dx * bases,

    y == dy * bases,

    AllDifferent(dx + dy),

    dx[0] > dy[0]
)

minimize(
    x - y
)
