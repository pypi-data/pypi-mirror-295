""""
Parser for Roadef Challenge 2012
"""
from pycsp3.problems.data.parsing import *

assignment = numbers_in(line())
next_line()

nResources = next_int()
resources = [(next_int(), next_int()) for _ in range(nResources)]

nMachines = next_int()
machines = [(next_int(), next_int(), [next_int() for _ in range(nResources)], [next_int() for _ in range(nResources)], [next_int() for _ in range(nMachines)]) for _
            in range(nMachines)]

nServices = next_int()
services = [(next_int(), [next_int() for _ in range(next_int())]) for _ in range(nServices)]

nProcesses = next_int()
processes = [(next_int(), [next_int() for _ in range(nResources)], next_int()) for _ in range(nProcesses)]

nBalanced = next_int()
balances = [((next_int(), next_int(), next_int()), next_int()) for _ in range(nBalanced)]

weights = [next_int(), next_int(), next_int()]

data["assignment"] = assignment
data["resources"] = resources
data["machines"] = machines
data["services"] = services
data["processes"] = processes
data["balances"] = balances
data["weights"] = weights

