"""
Airport Check-in Counter Allocation Problem (ACCAP) with fixed opening/closing times.

current version : hybrid tables
TODO : make hybrid tables more compact?
"""

from pycsp3 import *

flights, airlines = data
durations, requirements, x = zip(*flights)  # requirements in terms of numbers of counters; x stands for starts
nFlights, nAirlines, nCounters = len(flights), len(airlines), sum(requirements)

# y[i] is the first counter (index) of the series required by flight i
y = VarArray(size=nFlights, dom=range(nCounters))

# d[a] is the maximal distance between two flights of the airline a
d = VarArray(size=nAirlines, dom=range(nCounters))

# z is the number of used counters
z = Var(range(max(requirements), nCounters + 1))


def table(i, j):
    return [(v1, v2, v3) for v1 in range(nCounters) for v2 in range(nCounters) if
            len(v3 := range(max(v1 + requirements[i] - 1 - v2, v2 + requirements[j] - 1 - v1), nCounters)) > 0]


satisfy(
    # ensuring no counter is shared
    NoOverlap(origins=(x, y), lengths=(durations, requirements)),

    # computing the number of used counters
    [y[i] + requirements[i] <= z for i in range(nFlights)],

    # computing the maximal distance between two flights of the same airline
    [(y[i], y[j], d[a]) in table(i, j) for a in range(nAirlines) for i, j in combinations(airlines[a], 2)]

    # # computing the number of used counters
    # Maximum(y[i] + requirements[i] for i in range(nFlights)) <= z,
    #
    # # computing the maximal distance between two flights of the same airline
    # [Maximum(y[i] + requirements[i] - 1 - y[j] for i in airlines[a] for j in airlines[a] if i != j) <= d[a] for a in range(nAirlines)]

)

minimize(
    Sum(d) + z
)

"""
1) Constraints with MAximum are not efficient
"""
