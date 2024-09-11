"""
TODO actually not possible because we need fra more cells x[o,p-1] in the recursive call

The Ackermann function is a classic recursive example in computer science.
  It is a function that grows very quickly (in its value and in the size of
  its call tree). It is defined as follows:

      A(m, n) = n+1 if m = 0
                A(m-1, 1) if m > 0 and n = 0
                A(m-1, A(m, n-1)) if m > 0 and n > 0
"""

from pycsp3 import *

m, n = data or (3, 10)
assert 0 <= m <= 3


def bound(o, p):  # actually, exact value
    assert 0 <= o <= 3
    return p + 1 if o == 0 else p + 2 if o == 1 else 2 * p + 3 if o == 2 else 2 ** (p + 3) - 3


# x[o,p] is the value of A(o,p)
x = VarArray(size=[m + 1, n + 1], dom=range(bound(m, n) + 1))

satisfy(
    [x[0, p] == p + 1 for p in range(n + 1)],
    [x[o, 0] == x[o - 1, 1] for o in range(1, m + 1)],
    [x[o, p] == x[o - 1, x[o, p - 1]] for o in range(1, m + 1) for p in range(1, n + 1)]
)

maximize(
    x[-1,-1]
)
