"""
"""

from pycsp3 import *

nWeeks = data or 6
nNurses = 3
assert nWeeks % nNurses == 0
nDays = nWeeks * 7

nShortShifts, nLongShifts = (nWeeks * 5) // nNurses, (nWeeks * 7) // nNurses
nOffShifts = nDays - nShortShifts - nLongShifts
OFF, SHORT, LONG = shifts = range(3)  # off, short day, long day
nShifts = len(shifts)

MAX_WITHOUT_OFF = 7  # so, at least one day off every sequence of 8 days

weekend_days = [i for i in range(nDays) if i % 7 in (5, 6)]
business_days = [i for i in range(nDays) if i not in weekend_days]

T1 = [(0, 0, ANY), (0, 1, 1), (0, 1, 2), (0, 2, 1), (0, 2, 2),
      (1, 0, 0), (1, 1, ANY), (1, 2, ANY),
      (2, 0, 0), (2, 1, ANY), (2, 2, ANY)]

T2 = [tuple(0 if i <= ii < i + 5 else ANY for ii in range(21)) for i in range(21 - 4)]

T3 = [tuple(0 if i == ii else ANY for ii in range(MAX_WITHOUT_OFF + 1)) for i in range(MAX_WITHOUT_OFF + 1)]

# x[i][j] is the shift for the jth nurse on the ith day
x = VarArray(size=[nDays, nNurses], dom=lambda i, j: shifts if i in business_days else {OFF, LONG})

# y[j] is the nurse working on the jth weekend (and its multiple)
y = VarArray(size=nNurses, dom=range(nNurses))

satisfy(
    # ensuring different shifts on business days
    [AllDifferent(x[i]) for i in business_days],

    # only one nurse working on weekend days
    [Count(x[i], value=OFF) == 2 for i in weekend_days],

    # ensuring equity for off days
    [Sum(x[i][j] == OFF for i in range(nDays)) == nOffShifts for j in range(nNurses)],

    # ensuring equity for small days
    [Sum(x[i][j] == SHORT for i in range(nDays)) == nShortShifts for j in range(nNurses)],

    # ensuring equity for long days
    [Sum(x[i][j] == LONG for i in range(nDays)) == nLongShifts for j in range(nNurses)],

    # ensuring a permutation (for ordering worked weekends)
    AllDifferent(y),

    # ensuring the same nurse working a long day on friday, saturday and sunday
    [
        [x[k * 7 + 4][y[k % 3]] == LONG for k in range(nWeeks)],
        [x[k * 7 + 5][y[k % 3]] == LONG for k in range(nWeeks)],
        [x[k * 7 + 6][y[k % 3]] == LONG for k in range(nWeeks)]
    ],

    # ensuring at least two days off, and two days working for every sequence of three days
    [x[i:i + 3, j] in T1 for i in range(nDays - 2) for j in range(nNurses)],

    # at least, 5 consecutive days off every three weeks
    [x[k * 7:(k + 3) * 7, j] in T2 for k in range(nWeeks - 2) for j in range(nNurses)],

    # at least, one day off at every sequence of 8 days
    [x[i:i + 8, j] in T3 for i in range(nDays - 7) for j in range(nNurses)]
)
