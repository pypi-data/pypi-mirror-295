"""
From New Scientist #2380, 1st February 2003

If you start with my age, in years, and apply the four operations:
      +2  /8
      -3  *7
in some order, then the final answer you get is my husband's age in years.
Funnily enough, if you start with his age and apply the same four operations in a
different order, then you get my age.
What are our two ages?
"""

from pycsp3 import *

n = 4  # number of operations

ADD, SUB, DIV, MUL = operations = range(4)

x = VarArray(size=n + 1, dom=range(7 * 120 + 3))
y = VarArray(size=n + 1, dom=range(7 * 120 + 3))

opx = VarArray(size=n, dom=range(4))
opy = VarArray(size=n, dom=range(4))


def transition(v, u, op):
    return ift(op == ADD, v == u + 2, ift(op == SUB, v == u - 3, ift(op == DIV, (v == u // 8) & (u % 8 == 0), v == u * 7)))


satisfy(
    # at least 16 years-old
    [x[0] >= 16, y[0] >= 16],

    # ensuring symmetric ages wrt operations
    [x[0] == y[-1], x[-1] == y[0]],

    # ensuring all operations being performed
    [AllDifferent(opx), AllDifferent(opy)],

    # ensuring valid transitions after operations
    [
        [transition(x[i], x[i - 1], opx[i - 1]) for i in range(1, n + 1)],
        [transition(y[i], y[i - 1], opy[i - 1]) for i in range(1, n + 1)]
    ]
)

"""
 efficient if  
  java ace AgeChanging.xml -ale=3 -sle=22 -s=all
"""
