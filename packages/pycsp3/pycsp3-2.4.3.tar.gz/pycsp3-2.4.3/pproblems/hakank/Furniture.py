"""
From Marriott & Stuckey "Programming with Constraints", page 112
See also furnituremovingtransition at http://www.hakank.org/common_cp_models

Bernd is moving house again and must schedule the removal of his furniture. Only he
and three of his friends are available for the move and the move must be completed
in one hour. The following data above details the items of furniture which must be moved,
how long each takes to move and how many people are required. For example,
moving the piano (first item) requires 3 people and takes 30 minutes, while moving a chair
(second item) requires 1 person and takes 10 minutes.

Here, we combine two criteria
"""

from pycsp3 import *

horizon = 160
durations = [30, 10, 15, 15]
requirements = [3, 1, 3, 2]
n = len(durations)

# s[i] is the starting time of the ith task (moving the ith item of furniture)
s = VarArray(size=n, dom=range(horizon + 1))

# e[i] is the ending time of the ith task
e = VarArray(size=n, dom=range(horizon * 2 + 1))

# k is the number of required persons
k = Var(range(4))

satisfy(
    Cumulative(tasks=[(s[i], durations[i], requirements[i]) for i in range(n)]) <= k,

    # setting end times
    [e[i] == s[i] + durations[i] for i in range(n)]
)

minimize(
    Maximum(e) * 10 + k
)
