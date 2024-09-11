"""
From New Scientist #2372, 14th December 2002

Four pubs recently played a round-robin football tournament, in which
each team played each of the others twice at home and away. George has
drawn up the final league table, using this grid.

                    Played  Lost   Drawn  Won  Points
                  -----------------------------------
        Fagan's   |       |      |      |     |      |
        George    |       |      |      |     |      |
        Harlequin |       |      |      |     |      |
        Inkerman  |       |      |      |     |      |
                  -----------------------------------

With two points for a win and one for a draw, the teams finished, coincidentally,
in alphabetical order, as shown. George found further surprises:
1. The four columns in the table (Lost, Drawn, Won, Points) contained each four different numbers;
2. Although Fagan's won the tournament, the George won more games;
3. There were more away wins than home wins.

Which matches were drawn? Identify each as 'X v. Y', naming the home team first.
"""

from pycsp3 import *

n, nColumns = 4, 4  # number of teams
FAGAN, GEORGE, HARLEQUIN, INKERMAN = Pubs = range(n)
HOME, AWAY = Where = range(2)
LOSS, DRAW, WIN = Results = range(3)
POINTS = 3

x = VarArray(size=[n, n, 2], dom=lambda i, j, k: Results if i != j else None)

y = VarArray(size=[n, nColumns], dom=lambda i, c: range(6 * (2 if c == POINTS else 1) + 1))

satisfy(
    # ensuring symmetry of scores
    [(x[i, j, k], x[j, i, (k + 1) % 2]) in {(LOSS, WIN), (DRAW, DRAW), (WIN, LOSS)} for i, j in combinations(n, 2) for k in Where],

    # computing the content of the three first columns
    [Cardinality(x[i], occurrences={c: y[i][c] for c in Results}) for i in range(n)],

    # computing the scores (content of the fourth column)
    [y[i, POINTS] == 2 * y[i, WIN] + y[i, DRAW] for i in range(n)],

    # the teams finished, coincidentally, in alphabetical order
    Decreasing(y[:, POINTS], strict=True),

    # the four columns in the table contains four different numbers
    [AllDifferent(y[:, c]) for c in range(nColumns)],

    # Although Fagan won the tournament, George won more games
    y[GEORGE, WIN] > y[FAGAN, WIN],

    # there were more away wins than home wins
    Count(x[:, :, AWAY], value=WIN) - Count(x[:, :, HOME], value=WIN) > 0
)

"""
It is also possible to write:
    Count(x[:, :, AWAY], value=WIN) > Count(x[:, :, HOME], value=WIN)
but the form may be slightly more complex for solvers
"""
