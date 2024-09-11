"""
See 1d_rubiks_cube at  http://www.hakank.org/common_cp_models

TODO: TO BE CONTINUED

"""

from pycsp3 import *

n = len(data)
assert different_values(*data)

nSteps = 15  # hard coding

x = VarArray(size=[nSteps, n], dom=range(1, n + 1))

ops = VarArray(size=nSteps, dom=range(n - 2))

k = Var(range(nSteps + 1))


def turn(i):
    pass


satisfy(
    x[0] == data,

    [(ops[i] != 0) | (ops[i + 1] == 0) for i in range(nSteps - 1)],

    ops[k] == 0,

    (ops[2] == 0) | AllEqual(x[1], x[2])
)

minimize(
    k
)
