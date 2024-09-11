"""
The Puzzles of Sam Loyd (P 54), Puzzle number 5.

5. A side show at Coney Island is described as follows: "There were ten little
  dummies which you were to knock over with baseballs. The man said: 'Take as many
  throws as you like at a cent apiece and stand as close as you please. Add up the
  numbers on all the men that you knock down and when the sum amounts to exactly
  fifty, neither more nor less you get a genuine 25 cent Maggie Cline cigar with
  a gold band around it.'"

  The numbers on the ten dummies were 15, 9, 30, 21, 19, 3, 12, 6, 25, 27.
"""
from pycsp3 import *

numbers, d = data or ((3, 6, 9, 12, 15, 19, 21, 25, 27, 30), 30)
n = len(numbers)

# x[i] is 1 if the ith number is selected
x = VarArray(size=n, dom={0, 1})

satisfy(
    x * numbers == 50
)
