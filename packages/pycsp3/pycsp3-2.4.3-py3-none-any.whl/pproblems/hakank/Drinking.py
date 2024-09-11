"""
From Marriott & Stuckey "Programming with Constraints", excercise page 184, drinking game
See also drinking_game at http://www.hakank.org/common_cp_models

Here, this is an optimization version
"""

from pycsp3 import *

n = data or 101  # number of minutes (time slots)

# x[i] is 1 iff time i is drinking time
x = VarArray(size=n, dom={0, 1})

# y[i] is the  number of drinking times the 8 last minutes before time i
y = VarArray(size=n, dom=range(9))  # checks the last 8 minutesX


satisfy(
    # computing the number of drinking times every 8 minutes
    [y[t] == Sum(x[max(t - 8, 0):max(t, 1)]) for t in range(1, n)],

    # must drink when the time is divisible with 5 or 7 and there was no drinking the last 8 minutes
    [(y[t] == 0) == (x[t] == 1) for t in range(1, n) if t % 5 == 0 or t % 7 == 0]
)

minimize(
    Sum(x)
)
