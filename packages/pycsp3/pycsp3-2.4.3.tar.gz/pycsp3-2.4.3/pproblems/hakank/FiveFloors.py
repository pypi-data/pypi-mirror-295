"""
From Alexey Radul & Gerald Jay Sussman: "The Art of Propagator", page 34

Baker, Cooper, Fletcher, Miller, and Smith live on the first
five floors of this apartment house. Baker does not live on the
fifth floor. Cooper does not live on the first floor. Fletcher
does not live on either the fifth or the first floor. Miller lives
on a higher floor than does Cooper. Smith does not live on a
floor adjacent to Fletcher'. Fletcher does not live on a floor
adjacent to Cooper's.
"""

from pycsp3 import *

Baker, Cooper, Fletcher, Miller, Smith = People = VarArray(size=5, dom=range(1, 6))

satisfy(
    # people live on different floors
    AllDifferent(People),

    # Baker does not live on the fifth floor
    Baker != 5,

    # Cooper does not live on the first floor
    Cooper != 1,

    # Fletcher does not live on either the fifth or the first floor
    Fletcher not in {1, 5},

    # Miller lives on a higher floor than does Cooper
    Miller > Cooper,

    # Smith does not live on a floor adjacent to Fletcher
    abs(Smith - Fletcher) > 1,

    # Fletcher does not live on a floor adjacent to Cooper
    abs(Fletcher - Cooper) > 1
)
