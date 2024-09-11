"""
See https://www.mail-archive.com/programming@jsoftware.com/msg05817.html
From rubiks (hakank page) http://www.hakank.org/picat/1d_rubiks_cube.pi

 data = [1,3,2,6,5,4]
 data = [5,6,2,1,4,3]
 data =  [6,5,4,1,2,3]

 the two hardest problems, take 11 moves (12 including the initial step).
 data =  [6,3,5,2,4,1]   % GAP: x3*x1*x2*x1*x3*x2*x1*x2*x1*x3*x1
 data =  [6,4,2,5,3,1]   % GAP: x1*x3*x2*x3*x2*x1*x3*x2*x3*x2*x1

 infeasible
 data =  [6,5,4,3,2,1]

 test with another length (8) with the same seq_length (4)
 The hardest is 10 moves (there are 156 with 10 moves according to GAP)
 data =  [6,8,3,7,1,4,2,5] % 8 steps

 These takes 10 steps
 data =  [2,4,1,7,5,3,8,6] % GAP: x2*x3*x2*x4*x3*x5*x4*x1*x2*x1
 data =  [8,7,6,3,2,5,4,1]  % x3*x1*x2*x3*x1*x4*x5*x1*x3*x1

 Chuffed took 1:24 minutes (min_step: 13)
 data =  [7, 5, 11, 8, 9, 1, 10, 3, 4, 2, 6, 12]

 Chuffed took 3:27 minutes to solve this (min_step: 13)
 data =  [ 12, 2, 7, 3, 4, 11, 1, 10, 8, 9, 6, 5 ]

 java ace RubiksCube-hybrid-10.xml -ale=5 => 24s
 java ace RubiksCube-10.xml -ale=7 -varh=FraOnDom   => solution 14 en 133s
"""

from pycsp3 import *
from random import Random

instances = [[1, 3, 2, 6, 5, 4],  # 0
             [5, 6, 2, 1, 4, 3],  # 1
             [6, 5, 4, 1, 2, 3],  # 2
             [6, 3, 5, 2, 4, 1],  # 3
             [6, 4, 2, 5, 3, 1],  # 4
             [6, 5, 4, 3, 2, 1],  # 5
             [6, 8, 3, 7, 1, 4, 2, 5],  # 6
             [2, 4, 1, 7, 5, 3, 8, 6],  # 7
             [8, 7, 6, 3, 2, 5, 4, 1],  # 8
             [7, 5, 11, 8, 9, 1, 10, 3, 4, 2, 6, 12],  # 9
             [12, 2, 7, 3, 4, 11, 1, 10, 8, 9, 6, 5]]  # 10

if isinstance(data, int):
    n, r, nSteps = len(instances[data]), 4, 15  # n is the order of the series (example: 1 2 3 4 5 6 for n = 6), r is the size of the rotation slice
    init_board = instances[data]
else:
    n, r, nSteps, seed = data  # seed to shuffle an initial series (1 2 3 4 5 6) so as to obtain an initial instance
    init_board = Random(seed).sample([i for i in range(1, n + 1)], n)

final_board = [i for i in range(1, n + 1)]
nRotations = n - r + 1 + 1  # +1 one more time for including 0 (no rotation)

# x[t][i] is the value of the ith element of the vector at time t
x = VarArray(size=[nSteps + 1, n], dom=range(1, n + 1))

# y[t] is the rotation chosen at time t (0 for none)
y = VarArray(size=nSteps, dom=range(nRotations))

# z is the actual number of performed rotations
z = Var(dom=range(nSteps + 1))

satisfy(
    # setting the initial board
    x[0] == init_board,

    # setting the final board
    x[-1] == final_board,

    # computing when it is finished
    y[z] == 0,

    # tag(redundant-constraints)
    [AllDifferent(x[t]) for t in range(1, nSteps + 1)]
)

# lists storing the positions to be swapped according to the operations
swaps = [[i if i not in range(op, op + r) else list(range(op + r - 1, op - 1, -1))[i - op] for i in range(n)] for op in range(nRotations - 1)]

if not variant():

    satisfy(
        # ensuring no more operation once finished
        [(y[t] != 0) | (y[t + 1] == 0) for t in range(nSteps - 1)],

        # do not cancel the last operation
        [(y[t] == 0) | (y[t] != y[t + 1]) for t in range(nSteps - 1)],

        # ensuring valid rotations
        [iff(y[t] == op, conjunction(x[t + 1][i] == x[t][swaps[op - 1][i]] for i in range(n))) for t in range(nSteps - 1) for op in range(1, nRotations)],

        # no more changes when finished
        [(y[t] == 0) == (x[t] == x[t + 1]) for t in range(nSteps)]
    )

elif variant("hybrid"):

    T1 = [(0, 0)] + [(op, ne(op)) for op in range(1, nRotations)]

    T2 = [tuple([0] + [ANY] * n + [col(i + 1) for i in range(n)])] + \
         [tuple([op] + [ANY] * n + [col(swaps[op - 1][i] + 1) for i in range(n)]) for op in range(1, nRotations)]

    satisfy(
        # ensuring valid sequences of operations
        [(y[t], y[t + 1]) in T1 for t in range(nSteps - 1)],

        # ensuring valid rotations (including rotation 0)
        [(y[t], x[t], x[t + 1]) in T2 for t in range(nSteps)]
    )

minimize(
    # minimizing the number of steps
    z
)

""" Comments
1) x[z] == final_board  is possible, but seemingly less efficient
   or also [x[z][i] == final_board[i] for i in range(n)]
2) it is less compact to write [iff(y[t] == 0, conjunction(x[t + 1][i] == x[t][i] for i in range(n))) for t in range(nSteps)]
3) Instead of [(y[t] == 0) == (x[t] == x[t + 1]) for t in range(nSteps)], we can also write :
    [(y[t] == 0) == AllEqualList(x[t],x[t + 1]) for t in range(nSteps)]
4) the redundant AllDifferent constraints seem to penalize the hybrid variant
"""
