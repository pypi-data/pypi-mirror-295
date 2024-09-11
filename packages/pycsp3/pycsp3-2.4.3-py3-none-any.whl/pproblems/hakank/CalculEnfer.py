"""
Problem from "Calculs d'enfer" by I. Stewart, Vision Mathématique, 86-88, 1994
See also "The Manual of NCL version 1.2", page 33
"""

from pycsp3 import *


def of(word):
    return [x[i] for i in alphabet_positions(word)]


# x[i] is the value for the ith letter of the alphabet
x = VarArray(size=26, dom=range(-100, 101))

satisfy(
    AllDifferent(x),

    Sum(of("zero")) == 0,
    Sum(of("one")) == 1,
    Sum(of("two")) == 2,
    Sum(of("three")) == 3,
    Sum(of("four")) == 4,
    Sum(of("five")) == 5,
    Sum(of("six")) == 6,
    Sum(of("seven")) == 7,
    Sum(of("eight")) == 8,
    Sum(of("nine")) == 9,
    Sum(of("ten")) == 10,
    Sum(of("eleven")) == 11,
    Sum(of("twelf")) == 12
)

minimize(
    Maximum(abs(x[i]) for i in range(26))
)
