"""
In three dollars, you get 5 bananas, in five dollars, 7 oranges,
in seven dollars, 9 mangoes and in nine dollars, three apples, I need to
purchase 100 fruits in 100 dollars. Please keep in mind that all type
of fruits need to be purchased but I do not like banana and apple, so
these should be of minimum quantity.
"""

from pycsp3 import *

bananas, oranges, mangoes, apples = fruits = VarArray(size=4, dom=range(1, 101))

satisfy(
    3 * bananas // 5 + 5 * oranges // 7 + 7 * mangoes // 9 + 9 * apples // 3 == 100,

    [bananas % 5 == 0, oranges % 7 == 0, mangoes % 9 == 0, apples % 3 == 0],

    Sum(fruits) == 100
)

minimize(
    bananas + apples
)

"""
possibly instead, multiply with 3*5*7*9=945 on both sides to weed out the divisions
   3*Bananas*189 + 5*Oranges*135 + 7*Mangoes*105 + 9*Apples*315 #= 100*945
"""
