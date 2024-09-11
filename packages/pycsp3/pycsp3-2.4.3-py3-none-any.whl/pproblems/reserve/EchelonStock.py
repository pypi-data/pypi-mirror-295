"""
See Problem 040 on CSPLib

"""

from pycsp3 import *
from math import floor, gcd
from functools import reduce

children, hcosts, pcosts, demands = data
n, nPeriods, nLeaves = len(children), len(demands[0]), len(demands)

gcd = reduce(gcd, {v for row in demands for v in row})
for row in demands:
    for t in range(nPeriods):
        row[t] = row[t] // gcd
for i in range(n):
    hcosts[i] = hcosts[i] * gcd

sumDemands = []
for i in range(n):
    sumDemands.append(sum(demands[i]) if i < nLeaves else sum(sumDemands[j] for j in children[i]))
parents = [None for _ in range(n)]
for i in range(n):
    for j in children[i]:
        parents[j] = i

allDemands = []
for i in range(n):
    allDemands.append([sum(demands[i][t:]) for t in range(nPeriods)] if i < nLeaves else [sum(allDemands[j][t] for j in children[i]) for t in range(nPeriods)])
print(allDemands)


def ratio1(i, coeff=1):
    return floor(pcosts[i] // (coeff * (hcosts[i] - hcosts[parents[i]])))


def ratio2(i, t_inf):
    return min(sum(demands[i][t_inf: t_sup + 1]) + ratio1(i, t_sup - t_inf + 1) for t_sup in range(t_inf, nPeriods))


print(parents, sumDemands, children, hcosts, pcosts, demands)

# x[i][t] is the amount ordered at node i at period (time) t
x = VarArray(size=[n, nPeriods], dom=lambda i, t: range(sumDemands[i] + 1))

# y[i][t] is the amount stocked at node i at the end of period t
y = VarArray(size=[n, nPeriods], dom=lambda i, t: range(sumDemands[i] + 1))

satisfy(
    [y[i][0] == x[i][0] - demands[i][0] for i in range(nLeaves)],

    [y[i][t] - Sum(y[i][t - 1], x[i][t]) == -demands[i][t] for i in range(nLeaves) for t in range(1, nPeriods)],

    [y[i][0] == x[i][0] - Sum(x[j][0] for j in children[i]) for i in range(nLeaves, n)],

    [y[i][t] == y[i][t - 1] + x[i][t] - Sum(x[j][t] for j in children[i]) for i in range(nLeaves, n) for t in range(1, nPeriods)],

    # tag(redundant-constraints)
    [Sum(x[i]) == sumDemands[i] for i in range(n)],

    # IC1
    [y[i][-1] == 0 for i in range(n)],

    # IC2
    [(x[i][t] == 0) | disjunction(x[j][t] > 0 for j in children[i]) for i in range(nLeaves, n) for t in range(nPeriods)],

    # IC3
    [y[i][t] <= ratio1(i) for i in range(n - 1) for t in range(nPeriods)],

    # IC4
    [x[i][t] <= ratio2(i, t) for i in range(nLeaves) for t in range(nPeriods)],

    # IC5
    [(y[i][t - 1] == 0) | (x[i][t] == 0) for i in range(n) for t in range(1, nPeriods)],

    # IC6a
    [x[i][t] <= allDemands[i][t] for i in range(n) for t in range(nPeriods)],

    # IC6b
    [y[i][t] <= allDemands[i][t + 1] for i in range(n) for t in range(nPeriods - 1)],

    [y[i][t - 1] + Sum(x[i][t:]) == allDemands[i][t] for i in range(nLeaves) for t in range(1, nPeriods)]

)

minimize(
    Sum(hcosts[i] * y[i][t] for i in range(n) for t in range(nPeriods))
    + Sum(pcosts[i] * (x[i][t] > 0) for i in range(n) for t in range(nPeriods))
)

# note that:
# a) IC4, simple version is: [x[i][t] <= demands[i][t] + ratio(i) for i in range(nLeaves) for t in range(nPeriods)],
# b) using only one Sum when posting the objective generates a complex XCSP3 expression
