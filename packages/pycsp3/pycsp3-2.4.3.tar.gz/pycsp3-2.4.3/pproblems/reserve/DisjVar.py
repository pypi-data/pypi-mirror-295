"""
Standard benchmark problem.
"""

from pycsp3 import *

x = VarArray(size=6, dom=range(16))
w = VarArray(size=6, dom=range(3, 10))

satisfy(
    NoOverlap(origins=x, lengths=w)
)
