"""
See enigma_1535  at http://www.hakank.org/common_cp_models/
Back to Front (Enigma 1535 Bob Walker, New Scientist magazine, March 7, 2009.)

Joe has found that just a few numbers have a rather unique property.
Reverse the order of the digits, and the new (different) number is a multiple of the original.
For some specified numbers of digits (four or more) there are only two numbers with the property.
Joe gave Penny the task of finding the two 6-digit numbers.

  TODO To be finalized

Execution:
  python3 BackToFront.py
"""

from pycsp3 import *

# x[i] is the ith digit of the original number
x = VarArray(size=6, dom=lambda i: range(1, 10) if i == 0 else range(10))

# y[i] is the ith digit of the reversed number
y = VarArray(size=6, dom=lambda i: range(1, 10) if i == 0 else range(10))

u = Var()
v = Var()  # range(1,1000000))

satisfy(
    u == x * [10 ** (5 - i) for i in range(6)],

    v == y * [10 ** (5 - i) for i in range(6)],

    [x[i] == y[-1 - i] for i in range(6)],

    AllDifferentList(x, y),

    # u != v,

    u % v == 0
)

# u == [10 ** (5 - i) for i in range(6)] * x,  is not working. How to fix that? cursing is not effective...
# with cp_array([10 ** (5 - i) for i in range(6)]) it is working
# range(6) * 6  == u is not working
# 6 * x is not working
