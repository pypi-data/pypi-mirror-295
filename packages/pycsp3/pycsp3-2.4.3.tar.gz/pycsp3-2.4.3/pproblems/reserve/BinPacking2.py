"""
See BPPLIB – A Bin Packing Problem Library

Example of Execution:
  python3 BinPacking2.py -data=BinPacking_n1c1w4a.json
"""

from pycsp3 import *
from math import ceil

capacity, weights = data  # bin capacity and item weights
weights.sort()
nItems = len(weights)


def n_bins():
    cnt = 0
    curr_load = 0
    for weight in weights:
        curr_load += weight
        if curr_load > capacity:
            cnt += 1
            curr_load = weight
    return cnt


def series():
    t = []
    start = 0
    for i, weight in enumerate(weights):
        if weight == weights[start]:
            continue
        if start < i - 1:
            t.append((start, i - start))
        start = i
    return t


def w(a, b, *, bar=False):
    if bar:
        return [i for i, weight in enumerate(weights) if a <= weight <= b]
    return [i for i, weight in enumerate(weights) if a < weight <= b]


half = len(w(capacity // 2, capacity))


def lb2(v=None):
    if v is None:
        return max(lb2(vv) for vv in range(capacity // 2 + 1))
    return half + max(0, ceil(sum(weights[i] for i in w(v, capacity - v, bar=True)) / capacity - len(w(capacity // 2, capacity - v))))


print("lb1", ceil(sum(weights) / capacity))
print("lb2", lb2())
# TODO lb3

nBins = n_bins()
series = series()
n_exceeding = len([weight for weight in weights if weight > capacity // 2])

x = VarArray(size=nItems, dom=range(nBins))

y = Var(range(lb2(), nBins + 1))

satisfy(
    # ensuring that the capacity of each bin is not exceeded
    BinPacking(x, sizes=weights) <= capacity,

    # ensuring a minimum number of bins
    y == NValues(x),  # >= ceil(sum(weights) / capacity),

    # tag(symmetry-breaking)
    [Increasing(x[s:s + l]) for (s, l) in series],

    # tag(symmetry-breaking)
    [x[nItems - n_exceeding + i] == i for i in range(n_exceeding)]
)

minimize(
    # minimizing the number of used bins
    y  # NValues(x)
)
