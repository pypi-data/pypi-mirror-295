"""
See https://mathoverflow.net/questions/1947/placing-checkers-with-some-restrictions

  n   #solutions
  --------------
  1        1
  2        2
  3        9
  4       64
  5      625
  6     7776
  7   117649
  8  2097152
"""

from pycsp3 import *

n = data or 6

# x[i] is the row where is put the checker of the ith column
x = VarArray(size=n, dom=range(n))

# y[j] is the number of checkers on the jth row
y = VarArray(size=n, dom=range(n + 1))

satisfy(
    Cardinality(x, occurrences=y),

    [Sum(y[:k]) != k for k in range(1, n)]
)
