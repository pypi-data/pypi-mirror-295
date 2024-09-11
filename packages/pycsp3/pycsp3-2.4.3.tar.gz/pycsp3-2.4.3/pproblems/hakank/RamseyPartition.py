"""
See http://www.mathematik.uni-bielefeld.de/~sillke/PUZZLES/partion3-ramsey

Partition the integers 1 to n into three sets, such that for no set are
there three different numbers with two adding to the third.
"""

from pycsp3 import *

n = data or 23

x = VarArray(size=n, dom={0, 1, 2})

satisfy(
    Cardinality(x, occurrences={i: range(3, n) for i in (0, 1, 2)}),

    [NValues(x[i], x[j], x[k]) > 1 for i, j, k in combinations(n, 3) if i + 1 + j + 1 == k + 1]
)
