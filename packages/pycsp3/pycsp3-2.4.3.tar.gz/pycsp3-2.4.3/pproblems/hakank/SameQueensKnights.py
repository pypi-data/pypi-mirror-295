"""
From http://archive.vector.org.uk/art10003900

The “Queens and Knights“ puzzle was posted in 2003-2004:
In 1850, Carl Friedrich Gauss and Franz Nauck showed that it is possible to place eight queens on a chessboard such that no queen attacks any other queen.
The problem of enumerating the 92 different ways there are to place 8 queens in this manner has become a standard programming example,
and people have shown that it can be solved using many different search techniques.
Now consider a variant of this problem: you must place an equal number of knights and queens on a chessboard such that no piece attacks any other piece.
What is the maximum number of pieces you can so place on the board, and how many different ways can you do it?

A variant relaxes the fact that the number of queens and knights must be equal.

version b seems better for 2024 competition
"""
import math
from pycsp3 import *

n = data

EMPTY, QUEEN, KNIGHT = range(3)


def queen_attack(i, j):
    return [(a, b) for a in range(n) for b in range(n) if (a, b) != (i, j) and (a == i or b == j or abs(i - a) == abs(j - b))]


def knight_attack(i, j):
    return [(a, b) for a in range(n) for b in range(n) if a != i and b != j and abs(i - a) + abs(j - b) == 3]


# x[i][j] indicates what is present in the cell with coordinates (i,j)
x = VarArray(size=[n, n], dom={EMPTY, QUEEN, KNIGHT})

# q is the number of queens
q = Var(dom=range(n + 1))

# k is the number of knights
k = Var(dom=range(n + 1))

satisfy(
    # computing the number of queens
    q == Sum(x[i][j] == QUEEN for i in range(n) for j in range(n)),

    # computing the number of knights
    k == Sum(x[i][j] == KNIGHT for i in range(n) for j in range(n)),

    # ensuring that no two pieces (queens or knights) attack each other
    [
        Match(
            x[i][j],
            Cases={
                QUEEN: Sum(x[queen_attack(i, j)]) == 0,
                KNIGHT: Sum(x[knight_attack(i, j)]) == 0
            }
        ) for i in range(n) for j in range(n)
    ]
)

if not variant():
    satisfy(
        # ensuring the same number of queens and knights
        q == k
    )

    maximize(
        q
    )

elif variant("b"):
    maximize(
        q + k
    )

# [
#         If(
#             x[i][j] == QUEEN,
#             Then=[
#                 Sum(x[queen_attack(i, j)]) == 0
#             ],
#             Else=If(x[i][j] == KNIGHT, Then=Sum(x[knight_attack(i, j)]) == 0)
#         ) for i in range(n) for j in range(n)
# ]
