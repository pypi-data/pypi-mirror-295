"""
Minizinc 2021

TODO : Not finished because the Minizinc model involved optional types (occurs, absent, deopt).
Not obvious to encode it.

"""

from pycsp3 import *

print(data)
horizon, releaseTimeW, workerInitial, currentStation, currentStep, currentBuffer, releaseTime, productType, production, worksteps, setup, takedown, workerMovement = data
nWorkers, nProducts, nProductTypes, nStations = len(workerInitial), len(currentStation), len(worksteps), len(workerMovement)
nWorksteps = 2

maxd = max(v for row in production for v in row)
mind = min(v for row in production for v in row)


def vwordD(product, station, workstep, worker):
    if worksteps[productType[product], station] == 2:
        return setup[productType[product], station] if workstep == 1 else takedown[productType[product], station]
    else:
        return production[productType[product], station] if workstep == 1 else 0


def vproD(product, station, workstep):
    if worksteps[productType[product], station] == 2:
        return setup[productType[product], station] if workstep == 1 else takedown[productType[product], station]
    else:
        return production[productType[product], station] if workstep == 1 else 0


workD = [[[[vwordD(product, station, workstep, worker) for worker in range(nWorkers)] for workstep in range(nWorksteps)] for station in range(nStations)] for
         product in range(nProducts)]
print("hhh", workD)
proD = [[[vproD(product, station, workstep) for workstep in range(nWorksteps)] for station in range(nStations)] for product in range(nProducts)]
print("jjjj", proD)

workST = VarArray(size=[nProducts, nStations, nWorksteps, nWorkers], dom=range(horizon + 2))

proST = VarArray(size=[nProducts, nStations, nWorksteps], dom=range(horizon + 2))

satisfy(
    # TO BE CONTINUED
)

minimize(
    proST[-1][-1][worksteps[productType[-1]][-1]] + proD[-1][-1][worksteps[productType[-1]][-1]]
)
