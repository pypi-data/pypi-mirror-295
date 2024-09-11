"""
Puzzle: Joyner's five statements
See http://strathmaths.wordpress.com/2012/10/17/puzzle-joyners-five-statements/

The following little logical teaser appears as a 'Ponderable 1.1.3' in
David Joyner's book Adventures in Group Theory (Johns Hopkins University Press, 2008).

Determine which of the following statements is true:
  - Exactly one of these statements is false.
  - Exactly two of these statements are false.
  - Exactly three of these statements are false.
  - Exactly four of these statements are false.
  - Exactly five of these statements are false.

Enthusiasts might like to consider the natural generalisation to n statements.
"""

from pycsp3 import *

n = data or 5

# x[i] is 1 if exactly i+1 of these statements is false
x = VarArray(size=n, dom={0,1})

satisfy(
    # determining which statements are true
    [x[i] == (Count(x, value=0) == i+1) for i in range(n)],

    # at least one statement must be true
    Sum(x) > 0
)
