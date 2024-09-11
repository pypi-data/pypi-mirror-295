"""

"""

from pycsp3 import *

p0 = ([1,2,3,4,5,6,7,8,9,10],30)

# TODO merge with BionPackingGecode


BackToFront.py
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
