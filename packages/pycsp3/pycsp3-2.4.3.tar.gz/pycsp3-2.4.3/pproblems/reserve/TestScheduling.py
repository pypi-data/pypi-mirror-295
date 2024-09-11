"""
See https://www.csplib.org/Problems/prob073/

Execution:
  python3 TestScheduling.py -data=t20m10r3-1.json
"""

from pycsp3 import *

nMachines, nResources, tests = data
durations, machines, resources = zip(*tests)  # information split over the tests
nTests = len(tests)
horizon = 9000  # TODO an upper bound should be automatically computed and used

tests_by_single_machines = [t for t in [[i for i in range(nTests) if len(machines[i]) == 1 and m in machines[i]] for m in range(nMachines)] if len(t) > 1]
tests_by_resources = [t for t in [[i for i in range(nTests) if r in resources[i]] for r in range(nResources)] if len(t) > 1]


def conflicting_tests():
    def possibly_conflicting(i, j):
        return len(machines[i]) == 0 or len(machines[j]) == 0 or len(set(machines[i] + machines[j])) != len(machines[i]) + len(machines[j])

    pairs = [(i, j) for i, j in combinations(range(nTests), 2) if possibly_conflicting(i, j)]
    for t in tests_by_single_machines + tests_by_resources:
        for i, j in combinations(t, 2):
            if (i, j) in pairs:
                pairs.remove((i, j))  # because will be considered in another posted constraint
    return pairs


# s[i] is the starting time of the ith test
s = VarArray(size=nTests, dom=range(horizon))

# m[i] is the machine used for the ith test
m = VarArray(size=nTests, dom=lambda i: range(nMachines) if len(machines[i]) == 0 else machines[i])

satisfy(
    # no overlapping on machines
    [(m[i] != m[j]) | (s[i] + durations[i] <= s[j]) | (s[j] + durations[j] <= s[i]) for i, j in conflicting_tests()],

    # no overlapping on single pre-assigned machines
    [NoOverlap(tasks=[(s[i], durations[i]) for i in t]) for t in tests_by_single_machines],

    # no overlapping on resources
    [NoOverlap(tasks=[(s[i], durations[i]) for i in t]) for t in tests_by_resources],

    # no more than the available number of machines used at any time  tag(redundant-constraints)
    Cumulative(origins=s, lengths=durations, heights=[1] * nTests) <= nMachines
)

minimize(
    # minimizing the makespan
    Maximum(s[i] + durations[i] for i in range(nTests))
)

""" Comments
1) the first group of NoOverlap constraints could be alternatively written:
  [NoOverlap((s[i], durations[i]) for i in t) for t in tests_by_single_machines],
  or [NoOverlap(origins=[s[i] for i in t], lengths=[durations[i] for i in t]) for t in tests_by_single_machines],
"""
