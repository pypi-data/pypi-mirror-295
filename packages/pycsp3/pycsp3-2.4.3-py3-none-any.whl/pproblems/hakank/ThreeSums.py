"""
Given a collection of integers, return the indices of any three elements which sum to zero.
For instance, if you are given (-1, 6, 8, 9, 10, -100, 78, 0, 1), you could return (0, 7, 8)
because -1 + 0 + 1 == 0
"""
from pycsp3 import *

numbers, m = data or (cp_array(-1, 6, 8, 9, 10, -100, 78, 0, 1), 3)
n = len(numbers)

# x[i] is the index of the ith selected number
x = VarArray(size=m, dom=range(n))

satisfy(
    Sum(numbers[x[i]] for i in range(m)) == 0
)
