"""

This is a generalization of the famous Fox-Goose-Corn puzzle. In this version, a farmer
wants to transport f foxes, g geese and c bags of corn from the west to the east side of a
river. She has a boat with a capacity available for her to move some of the goods at once
while the rest remain on shore. She can go back and forth to bring as many goods as she
wants to the east. Nonetheless, some rules apply to the goods that are not being supervised
on either side while the farmer is on the boat:
  - If only foxes and bags of corn are sitting on a shore, then a fox dies by eating a bag of corn;
  - If there are foxes and geese, and the foxes outnumber the geese, one fox dies;
  - On the other hand, if the geese are not outnumbered, each fox kills one goose;
  - If there is no fox, and the geese outnumber the bags, a goose dies and one bag is eaten;
  - On the other hand, if the corn is not outnumbered, each goose eats a bag.
The farmer must maximize the profit (there is a price for each good) from the surviving
goods on the east.


The model, below, can be seen as the translation of the one submitted to the 2019 Minizinc challenge

## Data
  a sequence of 8 integers

## Model
 Two variants are defined
  - a main variant involving logical constraints
  - a variant 'hybrid' building hybrid tables

  constraints: Element, Intension, Extension

## Execution
  python FoxGeeseCorn.py -data=[6,7,8,4,15,8,12,9]

## Links
  - https://link.springer.com/article/10.1007/s10601-018-9297-2
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  academic, mzn19
"""

from pycsp3 import *

# data from Minizinc challenge 2019
m2019 = [(6, 7, 8, 4, 15, 8, 12, 9), (50, 50, 50, 7, 35, 9, 10, 8), (6, 7, 8, 1, 31, 0, 6, 3), (118, 213, 124, 178, 3, 7, 5, 3), (10, 10, 12, 5, 19, 1, 1, 1)]

nFoxes, nGeese, nCorns, boatCapacity, horizon, pf, pg, pc = m2019[data] if isinstance(data, int) else data

East = [i for i in range(1, horizon + 1) if i % 2 == 1]
West = [i for i in range(1, horizon + 1) if i % 2 != 1]

# tf[i] is the number of foxes traversing at time i (to time i+1)
tf = VarArray(size=horizon, dom=range(boatCapacity + 1))

# tg[i] is the number of geese traversing at time i (to time i+1)
tg = VarArray(size=horizon, dom=range(boatCapacity + 1))

# tc[i] is the number of corns traversing at time i (to time i+1)
tc = VarArray(size=horizon, dom=range(boatCapacity + 1))

# z is the number of trips
z = Var(range(horizon + 1))

# ef[i] is the number of foxes on east side at time i
ef = VarArray(size=horizon + 1, dom=range(nFoxes + 1))

# eg[i] is the number of geese on east side at time i
eg = VarArray(size=horizon + 1, dom=range(nGeese + 1))

# ec[i] is the number of corns on east side at time i
ec = VarArray(size=horizon + 1, dom=range(nCorns + 1))

# wf[i] is the number of foxes on west side at time i
wf = VarArray(size=horizon + 1, dom=range(nFoxes + 1))

# wg[i] is the number of geese on west side at time i
wg = VarArray(size=horizon + 1, dom=range(nGeese + 1))

# wc[i] is the number of corns on west side at time i
wc = VarArray(size=horizon + 1, dom=range(nCorns + 1))

if not variant():
    aux = VarArray(size=horizon, dom=range(4))  # auxiliary variables


    def alone(i):
        tmp = aux[i - 1]  # Var(dom=range(4), id="tmp" + str(i))
        f, g, c = (wf, wg, wc) if i in East else (ef, eg, ec)
        fox0, fox1, geese0, geese1, corn0, corn1 = f[i - 1] - tf[i - 1], f[i], g[i - 1] - tg[i - 1], g[i], c[i - 1] - tc[i - 1], c[i]
        return (
            tmp == cp_array(0, 0, 0, 1, 0, 2, 3, 3)[4 * (fox0 > 0) + 2 * (geese0 > 0) + (corn0 > 0)],
            fox1 == fox0 + cp_array(0, 0, -1, ift(fox0 > geese0, -1, 0))[tmp],
            geese1 == geese0 + cp_array(0, ift(geese0 > corn0, -1, 0), 0, ift(fox0 > geese0, 0, -fox0))[tmp],
            corn1 == corn0 + cp_array(0, ift(geese0 > corn0, -1, -geese0), -1, 0)[tmp]
        )


    satisfy(
        # updating goods on west side when unsupervised
        [alone(i) for i in East],

        # updating goods on east side when unsupervised
        [alone(i) for i in West]
    )

elif variant("hybrid"):
    def alone_hybrid(i):
        # TODO : the encoding is wrong : this is visible by running: java ace FoxGeeseCorn-hybrid-0.xml
        T = []
        # (1) of the paper <=> (1) of the screen: check ok: an error in the comment follow:
        # table.append(tuple([0, eq(col(0)), 0, eq(col(2)), 0, eq(col(4))]))
        # table.append(tuple([gt(0), eq(col(0)), 0, eq(col(2)), 0, eq(col(4))]))
        # table.append(tuple([0, eq(col(0)), gt(0), eq(col(2)), 0, eq(col(4))]))
        # table.append(tuple([0, eq(col(0)), 0, eq(col(2)), gt(0), eq(col(4))]))

        T.extend([
            (0, 0, 0, 0, ANY, col(4)),
            (0, 0, ANY, col(2), 0, 0),
            (ANY, col(0), 0, 0, 0, 0),
            (lt(0), col(0), ANY, col(2), ANY, col(4)),
            (ANY, col(0), lt(0), col(2), ANY, col(4)),
            (ANY, col(0), ANY, col(2), lt(0), col(4))
        ])

        # (2) of the paper <=> (4) of the screen
        # check ok but wf0 > 0 ? problem may be here
        T.append((gt(col(2)), col(0) - 1, gt(0), col(2), ANY, col(4)))
        T.append((le(col(2)), col(0), gt(0), col(2) - col(0), ANY, col(4)))

        # (3) of the paper <=> (3) of the screen: check Ok
        T.append((gt(0), col(0) - 1, 0, 0, gt(0), col(4) - 1))

        # (4) of the paper <=> (2) of the screen: check Ok
        T.append((ANY, 0, le(col(4)), col(2), ANY, col(4) - col(2)))
        T.append((ANY, 0, gt(col(4)), col(2) - 1, ANY, col(4) - 1))
        return T


    satisfy(
        # updating goods on west side when unsupervised
        [(wf[i - 1] - tf[i - 1], wf[i], wg[i - 1] - tg[i - 1], wg[i], wc[i - 1] - tc[i - 1], wc[i]) in alone_hybrid(i) for i in East],

        # updating goods on east side when unsupervised
        [(ef[i - 1] - tf[i - 1], ef[i], eg[i - 1] - tg[i - 1], eg[i], ec[i - 1] - tc[i - 1], ec[i]) in alone_hybrid(i) for i in West]
    )

satisfy(
    # initialization
    [
        [ef[0] == 0, eg[0] == 0, ec[0] == 0],
        [wf[0] == nFoxes, wg[0] == nGeese, wc[0] == nCorns]
    ],

    # updating goods on east side when landing
    [
        If(
            i <= z,
            Then=[
                ef[i] == ef[i - 1] + tf[i - 1],
                eg[i] == eg[i - 1] + tg[i - 1],
                ec[i] == ec[i - 1] + tc[i - 1]
            ]
        ) for i in East
    ],

    # updating goods on west side when landing
    [
        If(
            i <= z,
            Then=[
                wf[i] == wf[i - 1] + tf[i - 1],
                wg[i] == wg[i - 1] + tg[i - 1],
                wc[i] == wc[i - 1] + tc[i - 1]
            ]
        ) for i in West
    ],

    # respecting the capacity of the boat
    [tf[i] + tg[i] + tc[i] <= boatCapacity for i in range(horizon)],

    # once finished, no more traversals
    [If(i > z, Then=[tf[i - 1] == 0, tg[i - 1] == 0, tc[i - 1] == 0]) for i in range(1, horizon + 1)],

    # tag(redundant-constraints)
    [
        [wf[i - 1] + ef[i - 1] >= wf[i] + ef[i] for i in range(1, horizon + 1)],
        [wg[i - 1] + eg[i - 1] >= wg[i] + eg[i] for i in range(1, horizon + 1)],
        [wc[i - 1] + ec[i - 1] >= wc[i] + ec[i] for i in range(1, horizon + 1)]
    ]
)

maximize(
    # maximize the profit from the surviving goods on the east
    ef[z] * pf + eg[z] * pg + ec[z] * pc
)

"""
1) it is possible to avoid declaring the array aux, and declare a variable when calling alone as follows:
  tmp = Var(dom=range(4), id="tmp" + str(i))
"""

# test = False
# if test:
#     instance = compile()
#     # cosoco = ExternalProcess("cosoco", "./../cosoco/main/cosoco")
#     ace = solver(ACE)
#     # if not subvariant("smart"):
#     print("solving...")
#     # ace.setting("-ale=4 -pra=0")
#     result = ace.solve(instance, verbose=True)
#     print(result)


# table.append((0, col(0), 0, col(2), ANY, col(4)))
# table.append((0, col(0), ANY, col(2), 0, col(4)))
# table.append((ANY, col(0), 0, col(2), 0, col(4)))
# table.append((lt(0), col(0), ANY, col(2), ANY, col(4)))
# table.append((ANY, col(0), lt(0), col(2), ANY, col(4)))
# table.append((ANY, col(0), ANY, col(2), lt(0), col(4)))
#
# # (2) of the paper <=> (4) of the screen
# # check ok but wf0 > 0 ? problem may be here
# table.append((gt(col(2)), col(0) - 1, gt(0), col(2), ANY, col(4)))
# table.append((le(col(2)), col(0), gt(0), col(2) - col(0), ANY, col(4)))
#
# # (3) of the paper <=> (3) of the screen: check Ok
# table.append((gt(0), col(0) - 1, 0, 0, gt(0), col(4) - 1))
#
# # (4) of the paper <=> (2) of the screen: check Ok
# table.append((ANY, 0, le(col(4)), col(2), ANY, col(4) - col(2)))
# table.append((ANY, 0, gt(col(4)), col(2) - 1, ANY, col(4) - 1))

# A => B <=> Not A or B: i < trips => (efox[i] == efox[i - 1] + fox[i - 1]) for i in East]


#     [(i > z) | (ef[i] == ef[i - 1] + tf[i - 1]) for i in East],
#     [(i > z) | (eg[i] == eg[i - 1] + tg[i - 1]) for i in East],
#     [(i > z) | (ec[i] == ec[i - 1] + tc[i - 1]) for i in East]
