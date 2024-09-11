"""
Fill the white cells on each side of the barrels with different digits from 1 to 6.
Digits cannot repeat in every horizontal and vertical directions. Each number
on the barrels top must be equal to the sum or product of the four different
digits in the barrel. All top numbers are different and less than 91.
"""

from pycsp3 import *

barrels = [
    [0, 0, 0],
    [13, 0, 30],
    [15, 24, 0]
]

contents = [
    [0, 3, 0, 0, 6, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 4, 0, 0],
    [0, 0, 5, 0, 0, 0],
    [0, 0, 0, 2, 5, 0],
    [0, 1, 0, 0, 0, 0]
]

x = VarArray(size=[3, 3], dom=range(1, 92))

y = VarArray(size=[6, 6], dom=range(1, 7))

satisfy(
    [x[i][j] == barrels[i][j] for i in range(3) for j in range(3) if barrels[i][j] != 0],

    [y[i][j] == contents[i][j] for i in range(6) for j in range(6) if contents[i][j] != 0],

    AllDifferent(x),

    AllDifferent(y, matrix=True),

    [(x[i][j] == Sum(y[i * 2:i * 2 + 2, j * 2:j * 2 + 2])) | (x[i][j] == Product(y[i * 2:i * 2 + 2, j * 2:j * 2 + 2])) for i in range(3) for j in range(3)]
)
