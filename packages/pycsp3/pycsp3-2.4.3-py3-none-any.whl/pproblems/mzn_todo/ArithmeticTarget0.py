"""
Minizinc 2022

Original MZN model by Kelvin Davis
"""

from pycsp3 import *

numbers, target = data

n = len(numbers)
m = 2 * n  # - 1

M = range(1, m)
VAL, ADD, SUB, MUL, DIV, NO = Tokens = range(6)

# x[i] is the token associated with the ith node
x = VarArray(size=m, dom=lambda i: {-1} if i == 0 else Tokens)

# left[i] is the left child (or 0 if none) of the ith node
left = VarArray(size=m, dom=lambda i: {-1} if i == 0 else range(m))

# right[i] is the right child (or 0 if none) of the ith node
right = VarArray(size=m, dom=lambda i: {-1} if i == 0 else range(m))

# lowest[i] is the lowest descendant of the ith node
lowest = VarArray(size=m, dom=lambda i: {-1} if i == 0 else range(m))

# highest[i] is the highest descendant of the ith node
highest = VarArray(size=m, dom=lambda i: {-1} if i == 0 else range(m))

# index[i] is the index of the number associated with the ith node
index = VarArray(size=m, dom=lambda i: {-1} if i == 0 else range(n + 1))

# leaf[i] is 1 if the ith node is a leaf
leaf = VarArray(size=m, dom={0, 1})

# parent[i] is 1 if the ith node is a parent
parent = VarArray(size=m, dom={0, 1})

# unused[i] is the ith element is unused
unused = VarArray(size=m, dom={0, 1})

# the tree depth
depth = Var(range(1, 2 * n))

# z1[i] is the value associated with the ith node
z1 = VarArray(size=m, dom=lambda i: {-1} if i == 0 else range(10 * target + 1))

# z2 is the number of used nodes
z2 = Var(range(1, n + 1))

satisfy(
    # the special value 0 must appear n-1 times
    Count(index, value=0) == n - 1,

    # all indexes of numbers must be different (except for the special value 0)
    AllDifferent(index, excepting=0),

    # ensuring that the tree has n leaves
    Count(x, value=VAL) == n,

    # computing the tree depth
    depth == highest[1],

    # computing the number of unused nodes
    2 * z2 - 1 == depth,

    # determining leaves
    [leaf[i] == (x[i] == VAL) & (left[i] == 0) & (right[i] == 0) & (highest[i] == i) & (lowest[i] == i) & (index[i] != 0) for i in range(1, m)],

    # determining parents
    [parent[i] == (x[i] != VAL) & (x[i] != NO) & (x[left[i]] != NO) & (x[right[i]] != NO)
     & (left[i] == i + 1) & (right[i] > left[i]) & (right[i] == highest[left[i]] + 1) & (lowest[i] == i) & (highest[i] == highest[right[i]]) & (index[i] == 0)
     for i in range(1, m)],

    # determining unused elements
    [unused[i] == ((x[i] == NO) | (x[i] == VAL)) & (left[i] == 0) & (right[i] == 0) & ((x[i] != VAL) | (index[i] != 0))
     & ((x[i] != NO) | (index[i] == 0)) & (lowest[i] == 0) & (highest[i] == 0) for i in range(1, m)],

    # constraining leaves, parents and unused elements
    [
        [(i > depth) | leaf[i] | parent[i] for i in range(1, m)],
        [(i <= depth) | unused[i] for i in range(1, m)]
    ],

    # computing values associated with all elements
    [
        [(x[i] != VAL) | (z1[i] == numbers[index[i]]) for i in range(1, m)],
        [(x[i] != ADD) | (z1[i] == z1[left[i]] + z1[right[i]]) for i in range(1, m)],
        [(x[i] != SUB) | (z1[i] == z1[left[i]] - z1[right[i]]) for i in range(1, m)],
        [(x[i] != MUL) | (z1[i] == z1[left[i]] * z1[right[i]]) for i in range(1, m)],
        [(x[i] != DIV) | (z1[i] * z1[right[i]] == z1[left[i]]) for i in range(1, m)],
        [(x[i] != NO) | (z1[i] == 0) for i in range(1, m)]
    ],

    # tag(symmetry-breaking)
    [
        # associativity of addition
        [(x[i] != ADD) | (x[left[i]] != ADD) for i in range(1, m)],

        # identity of Addition
        [(x[i] != ADD) | ((z1[left[i]] != 0) & (z1[right[i]] != 0)) for i in range(1, m)],

        # associativity of Multiplication
        [(x[i] == MUL) | (x[left[i]] != MUL) for i in range(1, m)],

        # identity of Multiplication
        [(x[i] != MUL) | ((z1[left[i]] != 1) & (z1[right[i]] != 1)) for i in range(1, m)],

        # symmetry of Addition and Multiplication
        [((x[i] != ADD) & (x[i] != MUL)) | (x[left[i]] <= x[right[i]]) for i in range(1, m)],

        # (a-b)-c = a-(b+c)
        [(x[i] != SUB) | (x[left[i]] != SUB) for i in range(1, m)],

        # distributivity of multiplication
        [
            [imply(((x[i] == ADD) | (x[i] == SUB)) & (x[left[i]] == MUL) & (x[right[i]] == MUL), [
                z1[left[left[i]]] != z1[left[right[i]]],
                z1[left[left[i]]] != z1[right[right[i]]],
                z1[right[left[i]]] != z1[left[right[i]]],
                z1[right[left[i]]] != z1[right[right[i]]]]) for i in range(1, m)]
        ],

        # distributivity of division
        [((x[i] != ADD) & (x[i] != SUB)) | (x[left[i]] != DIV) | (x[right[i]] != DIV) | (z1[right[left[i]]] != z1[right[right[i]]]) for i in range(1, m)],

        # conditions wrt operations Add and Mul
        [
            [(x[i] != ADD) | (x[right[i]] != VAL) | (x[left[i]] == VAL) for i in range(1, m)],
            [(x[i] != MUL) | (x[right[i]] != VAL) | (x[left[i]] == VAL) for i in range(1, m)],
            [(x[i] != ADD) | (x[left[i]] != VAL) | (x[right[i]] != VAL) | (index[left[i]] < index[right[i]]) for i in range(1, m)],
            [(x[i] != MUL) | (x[left[i]] != VAL) | (x[right[i]] != VAL) | (index[left[i]] < index[right[i]]) for i in range(1, m)],
            [(x[i] != ADD) | (x[left[i]] != VAL) | (x[right[i]] != ADD) | (x[left[right[i]]] != VAL) | (index[left[i]] < index[left[right[i]]])
             for i in range(1, m)],
            [(x[i] != MUL) | (x[left[i]] != VAL) | (x[right[i]] != MUL) | (x[left[right[i]]] != VAL) | (index[left[i]] < index[left[right[i]]])
             for i in range(1, m)]
        ],

        # all numbers with the same value should be assigned in sorted order
        [(x[i] != VAL) | (x[j] != VAL) | (numbers[index[i]] != numbers[index[j]]) | (index[i] < index[j]) for i, j in combinations(range(1, m), 2)],

        # sorting nodes of equivalent value
        [(z1[i] != z1[j]) | (x[i] >= x[j]) for i, j in combinations(range(1, m), 2)]
    ]
)
minimize(
    10 * abs(z1[1] - target) + z2
)
