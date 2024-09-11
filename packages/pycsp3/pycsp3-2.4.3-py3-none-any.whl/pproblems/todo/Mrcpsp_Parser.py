from pycsp3.problems.data.parsing import *

n = number_in(next_line(4))
horizon = number_in(next_line())
n_renewables = number_in(next_line(1))
n_unrenewables = number_in(next_line())
assert number_in(next_line()) == 0

t = numbers_in(next_line(3))  # not useful
next_line(2)
m1 = [numbers_in(next_line()) for _ in range(12)]
next_line(3)
m2 = [numbers_in(next_line()) for _ in range(sum(row[1] for row in m1))]
prev = None
for i, row in enumerate(m2):
    if len(row) == 3 + n_renewables + n_unrenewables:
        prev = row
    else:
        assert len(row) == 2 + n_renewables + n_unrenewables
        m2[i] = [prev[0]] + row
resources = numbers_in(next_line(3))

jobs = []
j = 0
for i in range(n):
    modes = [OrderedDict([("duration", m2[k][2]), ("renewableUsage", m2[k][3:3 + n_renewables]), ("unrewableUsage", m2[k][3 + n_renewables:])]) for k in
             range(j, j + m1[i][1])]
    jobs.append(OrderedDict([("successors", m1[i][3:]), ("modes", modes)]))
    j += m1[i][1]

data["jobs"] = jobs
data["horizon"] = horizon
data["renewable"] = resources[:n_renewables]
data["unrewable"] = resources[n_renewables:]
