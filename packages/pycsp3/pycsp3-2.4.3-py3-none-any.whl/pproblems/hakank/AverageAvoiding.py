"""
See Winston - Operations research (pages 393-400)
"""

from pycsp3 import *
from collections import Counter

values = list(range(data)) if isinstance(data, int) else data

d = Counter(values)
n = len(values)

x = VarArray(size=n, dom=set(d.keys()))

satisfy(
    [2 * x[k] != x[i] + x[j] for i, j in combinations(n, 2) if i + 1 < j for k in range(i + 1, j)],

    Cardinality(x, occurrences={k: v for k, v in d.items()}),

    # tag(symmetry-breaking)
    x[0] == Minimum(x)
)

"""

"""
