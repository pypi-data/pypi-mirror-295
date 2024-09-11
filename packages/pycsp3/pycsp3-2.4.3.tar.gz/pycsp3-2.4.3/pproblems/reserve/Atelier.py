"""
See https://developers.google.com/optimization/scheduling/job_shop?hl=fr
"""

from pycsp3 import *

jobs = data or [  # task = (machine_id, processing_time).
    [(0, 3), (1, 2), (2, 2)],  # Job0
    [(0, 2), (2, 1), (1, 4)],  # Job1
    [(1, 4), (2, 3)],  # Job2
]

nJobs, nJobTasks = len(jobs), max(len(job) for job in jobs)
durations = [[task[1] for task in job] for job in jobs]
horizon = sum(sum(t) for t in durations)

tasksPerMachine = dict()
for i in range(nJobs):
    for j, task in enumerate(jobs[i]):
        tasksPerMachine.setdefault(task[0], []).append((i, j))

lasts = [len(job) - 1 for job in jobs]

# x[i][j] is the starting time of the jth task of the ith job
x = VarArray(size=[nJobs, nJobTasks], dom=lambda i, j: range(horizon + 1) if j <= lasts[i] else None)

satisfy(
    # respecting the order of the tasks for each job
    [x[i][j] + durations[i][j] <= x[i][j + 1] for i in range(nJobs) for j in range(lasts[i])],

    # no overlapping tasks using the same machine
    [
        NoOverlap(
            tasks=[Task(origin=x[i][j], length=durations[i][j]) for i, j in pairs]
        ) for pairs in tasksPerMachine.values()
    ]
)

minimize(
    # minimizing the make-span
    Maximum(x[i][lasts[i]] + durations[i][lasts[i]] for i in range(nJobs))
)
