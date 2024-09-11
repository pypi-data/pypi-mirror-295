from pycsp3 import *

from pycsp3.classes.entities import TypeNode

nStations = 4
areasCapacities = [5, 4, 4]  # nb operators who can work
nAreas = 3  # in the plane
# skills = []
nMachines = 30
machines = [[]]  # machines[i][j] is the jth machine in the ith station (a partition)
nMaxOperatorsPerStation = [40, 40, 30, 40]
takt = 1440

tasks = [{"id": "t0", "duration": 22, "usedAreas": [], "neutralisedAreas": [], "machines": [], "operators": 3, "parent": -1}]
stationOfTasks = [0, 1, -1, 2]  # station of the ith task (-1 if can be everywhere)
durations = [10, 6, 22, 45]
operators = [2, 1, 3, 2]
usedAreas = [set()]
neutralisedAreas = [set()]
precedences = [(2, 3), (1, 0)]  # between tasks
nTasks = 4

tasksPerMachine = [[]]

tasksPerArea = [[0, 1], [2], [3]]

# x[i] is the starting time of the ith task
x = VarArray(size=nTasks, dom=range(takt * nStations + 1))

nOps = VarArray(size=nStations, dom=lambda i: range(nMaxOperatorsPerStation[i] + 1))

satisfy(
    # tasks must start and finish in the same station
    [(x[i] // takt) == ((x[i] + durations[i]) // takt) for i in range(nTasks)],

    # ensuring that tasks are put on the right stations (wrt needed machines)
    [(x[i] // takt) == stationOfTasks[i] for i in range(nTasks) if stationOfTasks[i] != -1],

    # respecting precedences
    [x[i] + durations[i] <= x[j] for (i, j) in precedences],

    # respecting limit capacities of areas
    [Cumulative(tasks=[(x[t], durations[t], operators[t]) for t in tasksPerArea[i]]) <= areasCapacities[i] for i in range(nAreas)],

    [Cumulative(tasks=[(x[t], durations[t], operators[t] * (x[t] // takt == j)) for t in range(nTasks)]) <= nOps[j]
     for j in range(nStations)],

    # no overlap (is there a better way to handle that?)
    # [NoOverlap(tasks=[(x[i], durations[i]), (x[j], durations[j])]) for i in range(nTasks) for j in range(nTasks) if i != j and
    #  len(usedAreas[i].intersection(neutralisedAreas[j])) > 0],

    # tasks using the same machine cannot overlap
    # [NoOverlap(tasks=[(x[j], durations[j]) for j in tasksPerMachine[i]]) for i in range(nMachines)],

)

minimize(
    Sum(nOps)
)
