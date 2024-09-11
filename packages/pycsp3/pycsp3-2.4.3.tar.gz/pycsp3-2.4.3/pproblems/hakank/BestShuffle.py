"""
Shuffle the characters of a string in such a way that as many of the character values
are in a different position as possible. Print the result as follows: original string,
shuffled string, (score). The score gives the number of positions whose character value
did not change.
"""

from pycsp3 import *

preset = ["abracadabra", "seesaw", "grrrrrr",
          "thisis asdasdsasdasdjsasdsaddgasjdgashdgasjdgasd_a_longerstring",
          "assadashjfgljhfgrakjafkljfjlktrwlkjhglkflkjslkflkslkslsgflksfgjfgslkhjsgflkhgfslkhjsgflkhsflkghjsgflhkjsfglkjhslfghjsflghjlskgjhsgfh",
          "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
          ]

word = preset[data] if isinstance(data, int) else data
dword = cp_array(alphabet_positions(word))
n = len(word)

x = VarArray(size=n, dom=range(n))

satisfy(
    AllDifferent(x)
)

minimize(
    Sum(dword[x[i]] == dword[i] for i in range(n))
)
