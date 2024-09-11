"""
https://en.wikipedia.org/wiki/Word_ladder

python3 ppycsp3/pproblems/hakank/WordGolf.py -data=[6,/home/lecoutre/instances/crossword/dictionaries/ogd2008Dict/ogd2008,20,0]
python3 ppycsp3/pproblems/hakank/WordGolf.py -data=[7,/home/lecoutre/instances/crossword/dictionaries/ogd2008Dict/ogd2008,20,0 => unsat non trivial
  (seed 1, 2, 4 => unsat)
python3 ppycsp3/pproblems/hakank/WordGolf.py -data=[7,/home/lecoutre/instances/crossword/dictionaries/ogd2008Dict/ogd2008,20,3] => unsat non trivial
5 non trivial too

"""

from pycsp3 import *
import random

m, dict_name, nSteps, seed = data

words = []
for line in open(dict_name):
    code = alphabet_positions(line.strip().lower())
    if len(code) == m:
        words.append(code)
words, nWords = cp_array(words), len(words)

random.seed(seed)
start, end = random.randint(0, nWords // 2), random.randint(nWords // 2, nWords)
print(words[start], words[end])

#  x[i][j] is the letter, number from 0 to 25, at row i and column j
x = VarArray(size=[nSteps, m], dom=range(26))

# y[i] is the word index of the ith word
y = VarArray(size=nSteps, dom=range(nWords))

# z is the number of steps
z = Var(range(nSteps))

satisfy(
    # setting the start word
    [
        x[0] == words[start],
        y[0] == start
    ],

    # setting the end word
    [
        x[-1] == words[end],
        y[-1] == end
    ],

    # setting the ith word
    [x[i] == words[y[i]] for i in range(1, nSteps - 1)],

    # ensuring a (Hamming) distance of 1 between two successive words
    [
        If(
            i < z,
            Then=Hamming(x[i], x[i + 1]) == 1,
            Else=y[i] == y[i + 1]
        ) for i in range(nSteps - 1)
    ],

    # setting the objective value (number of steps)
    y[z] == end
)

minimize(
    z
)
