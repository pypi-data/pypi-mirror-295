"""
"""

from pycsp3 import *

x = VarArray(size=5, dom=range(5))

y = VarArray(size=5, dom=range(5))

satisfy(
    AllDifferent([]),

    Count([]) > -1,

    x == 0,

    y != 2,

    # tests instantiation
    [
        (x == 1) | (x[0] != 0),
        (x[0] != 0) | (x == 1)
    ],

    # tests refutation
    [
        (x != 1) | (x[0] != 0),
        (x[0] != 0) | (x != 1)
    ],

    # tests ordered
    [
        (Increasing(x)) | (x[-1] == 0),
        (x != 3) | Decreasing(x, lengths=range(5))
    ],

    # # test channel
    # [
    #     Channel(x, y) | (y[2] > 3)
    #
    # ]
)
