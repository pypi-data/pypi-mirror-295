"""
https://en.wikipedia.org/wiki/Word_square
https://github.com/matevz-kovacic/word-square?tab=readme-ov-file

python3 ppycsp3/pproblems/hakank/WordSquare.py -data=[10,/home/lecoutre/instances/crossword/dictionaries/ogd2008Dict/ogd2008]

"""

from pycsp3 import *

n, dict_name = data

words = []
for line in open(dict_name):
    code = alphabet_positions(line.strip().lower())
    if len(code) == n:
        words.append(code)
words, nWords = cp_array(words), len(words)

if not variant():
    #  x[i][j] is the letter, number from 0 to 25, at row i and column j
    x = VarArray(size=[n, n], dom=range(26))

    # y[k] is the word chosen for the kth position (row and column)
    y = VarArray(size=n, dom=range(nWords))

    satisfy(
        # # ensuring right connection wrt rows
        [x[i] == words[y[i]] for i in range(n)],

        # # ensuring right connection wrt columns
        [x[:, j] == words[y[j]] for j in range(n)],

        # ensuring different words
        AllDifferent(y)
    )

elif variant("hak"):

    # y[k] is the word chosen for the kth position (row and column)
    y = VarArray(size=n, dom=range(nWords))

    satisfy(
        # ensuring coherence of words
        [words[y[i], j] == words[y[j], i] for i in range(n) for j in range(n)],

        # ensuring different words
        AllDifferent(y)
    )

elif variant("table1"):
    #  x[i][j] is the letter, number from 0 to 25, at row i and column j
    x = VarArray(size=[n, n], dom=range(26))

    # y[k] is the word chosen for the kth position (row and column)
    y = VarArray(size=n, dom=range(nWords))

    satisfy(
        [(y[i], x[i]) in enumerate(words) for i in range(n)],

        [x[i] == x[:, i] for i in range(n)],

        AllDifferent(y)

    )

elif variant("table2"):
    #  x[i][j] is the letter, number from 0 to 25, at row i and column j
    x = VarArray(size=[n, n], dom=range(26))

    satisfy(
        # x[0] == alphabet_positions("scapharcae"),

        [x[i] in words for i in range(n)],

        [x[i] == x[:, i] for i in range(n)],

        AllDifferentList(x[i] for i in range(n))
    )
