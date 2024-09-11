"""
See http://www.comp.nus.edu.sg/~henz/projects/puzzles/digits/torn.html?19
  The Torn Number from "Amusements in Mathematics, Dudeney", number 113

  I had the other day in my possession a label bearing the number 3025
  in large figures. This got accidentally torn in half, so that 30 was
  on one piece and 25 on the other. On looking at these pieces I began
  to make a calculation, scarcely concious of what I was doing, when I
  discovered this little peculiarity. If we add the 30 and the 25
  together and square the sum we get as the result the complete original
  number on the label! Now, the puzzle is to find another number,
  composed of four figures, all different, which may be divided in the
  middle and produce the same result.
"""

from pycsp3 import *

# x[i] is the ith digit of the original number
x = VarArray(size=4, dom=lambda i: range(1, 10) if i == 0 else range(10))

# y is the partial sum
y = Var(range(200))  # a safe upper bound

satisfy(
    AllDifferent(x),

    y == x[0] * 10 + x[1] + x[2] * 10 + x[3],

    y * y == x * [1000, 100, 10, 1]
)
