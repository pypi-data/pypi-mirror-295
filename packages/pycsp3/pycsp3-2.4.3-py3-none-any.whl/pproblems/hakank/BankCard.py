"""
My bank card has a 4 digit pin, abcd. I use the following facts to help me remember it:
 - no two digits are the same
 - the 2-digit number cd is 3 times the 2-digit number ab
 - the 2-digit number da is 2 times the 2-digit number bc
"""

from pycsp3 import *

a, b, c, d = x = VarArray(size=4, dom=range(10))

satisfy(
    AllDifferent(x),
    (10 * c + d) == 3 * (10 * a + b),
    (10 * d + a) == 2 * (10 * b + c)
)
