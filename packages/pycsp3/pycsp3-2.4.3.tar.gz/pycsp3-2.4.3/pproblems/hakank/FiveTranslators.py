"""
See http://stackoverflow.com/questions/26260407/prolog-logic-puzzle-constraint-programming

Five translators are working in an international organization:
Spaniard, Englishman, Frenchman, German and Russian.
Each of them speaks its native language and also two
languages from the native languages of other translators. Find
the languages speaked by each translator if it is known that
 1. The Englishman speaks German.
 2. The Spaniard speaks French.
 3. The German does not speak Spanish.
 4. The Frenchman does not speak German.
 5. Spaniard and Englishman can talk with each other in German.
 6. Englishman and Frenchman can talk with each other in two languages.
 7. Four translators speak Russian.
 8. Exactly two translators speak French.
 9. Only one translator who speaks Spanish speaks also Russian.
 10. Russian and Englishman have no common languages except their native languages.
"""

from pycsp3 import *

n = 5

Spanish, English, French, German, Russian = range(n)

# x[i][j] is 1 if the ith translator speaks the native language of the jth translator
x = VarArray(size=[n, n], dom={0, 1})

satisfy(
    # each translator speaks his native language
    [x[i, i] == 1 for i in range(n)],

    # all translators speak three languages
    [Sum(x[i]) == 3 for i in range(n)],

    # 1. The Englishman speaks German
    x[English, German] == 1,

    # 2. The Spaniard speaks French
    x[Spanish, French] == 1,

    # 3. The German does not speak Spanish
    x[German, Spanish] == 0,

    # 4. The Frenchman does not speak German
    x[French, German] == 0,

    # 5. Spaniard and Englishman can talk with each other in German
    [x[Spanish, German] == 1, x[English, German] == 1],

    # 6. Englishman and Frenchman can talk with each other in two languages
    Sum(x[English, j] & x[French, j] for j in range(n)) == 2,

    # 7. Four translators speak Russian
    Sum(x[:, Russian]) == 4,

    # 8. Exactly two translators speak French
    Sum(x[:, French]) == 2,

    # 9. Only one translator who speaks Spanish speaks also Russian
    Sum(x[i, Spanish] & x[i, Russian] for i in range(n)) == 1,

    # 10. Russian and Englishman have no common languages except their native languages
    Sum(x[English, j] & x[Russian, j] for j in (Spanish, French, German)) == 0
)

""" Comments
1) Sum(x[English, j] & x[French, j] for j in range(n)) == 2 is more compact than:
   Sum((x[English, j] == 1) & (x[French, j] == 1) for j in range(n)) == 2
2) Count can be used instead of Sum
"""
