"""
This model was inspired by David Curran's
  blog post "The Fairest Way to Pick a Team "
  http://liveatthewitchtrials.blogspot.se/2012/06/fairest-way-to-pick-team.html

  What is the best way to pick a team? As kids we would always strictly alternate
  between teams so team 1 had first team 2 the second pick and then team 1 again etc.

  Most things you can measure about people are on a bell curve. A small number of
  people are bad, most are in the middle and a few are good. There are a few good
  known metrics of ability. None are perfect, there is no one number that can sum up
  ability. The simpler the sport the more one metric can tell you, in cycling VO2 max is
  a very good indicator. Whereas in soccer VO2 max, kicking speed, vertical leap, number
  of keep me ups you can do etc could all measure some part of football ability.

  So say there was one good metric for a task and teams were picked based on this.
  Is the standard strict alteration, where Team 1 picks then Team 2 alternating, fair?
  Fair here meaning both teams end up with a similar quality.

  java ace PickingTeams-300-10-00.xml -varh=Dom -valh=Occs
  (Occs does the job)
"""

from pycsp3 import *

if isinstance(data, int):
    if data == 1:
        strengths = [35, 52, 17, 26, 90, 55, 57, 54, 41, 9, 75, 24, 17, 23, 62, 74, 100, 67, 40, 48, 7, 6, 44, 19, 16, 14, 2, 66, 70, 2, 43, 45, 76, 53, 90, 12,
                     88, 96, 30, 30, 36, 93, 74, 1, 52, 45, 38, 7, 24, 96, 17, 21, 12, 12, 23, 90, 77, 64, 37, 79, 67, 62, 24, 11, 74, 82, 51, 17, 72, 18, 37,
                     94, 43, 44, 32, 86, 94, 33, 97, 27, 38, 38, 29, 92, 35, 82, 22, 66, 80, 8, 62, 72, 25, 13, 94, 42, 51, 31, 69, 66]
    elif data == 2:
        strengths = [41, 85, 90, 47, 15, 37, 90, 77, 4, 95, 6, 13, 77, 15, 17, 91, 12, 22, 15, 68, 11, 23, 41, 77, 71, 42, 23, 30, 77, 30, 74, 90, 97, 28, 89,
                     18, 3, 74, 86, 99, 25, 20, 58, 13, 59, 52, 81, 5, 49, 50, 56, 91, 85, 67, 47, 51, 70, 76, 59, 88, 51, 79, 79, 23, 18, 21, 43, 74, 85, 69,
                     11, 28, 55, 94, 3, 58, 83, 74, 87, 84, 98, 83, 59, 9, 88, 56, 33, 36, 21, 59, 4, 42, 68, 94, 11, 88, 25, 38, 89, 38]
    else:
        strengths = list(range(1, data + 1))
else:
    strengths = data

n = len(strengths)
assert n % 2 == 0

# x[i] is the team (0 or 1) of the ith player
x = VarArray(size=n, dom={0, 1})

# z is the difference of strengths between the two teams
z = Var(range(sum(strengths) // 2 + 1))

satisfy(
    # computing the difference of strengths
    z == abs(Sum(strengths[i] * (x[i] == 0) for i in range(n)) - Sum(strengths[i] * (x[i] == 1) for i in range(n))),

    # ensuring two teams of same size
    Cardinality(x, occurrences={0: n // 2, 1: n // 2}),

    # tag(symmetry-breaking)
    x[0] == 0,

    # divisibility of the sum  tag(redundant-constraint)
    z % 2 == sum(strengths) % 2
)

minimize(
    # minimizing the difference of strengths between the two teams
    z
)

"""
1) how to prove that the constraint is redundant?
"""
