from pycsp3 import *

nColors, nodeColors, edges, cycleSize = data
nNodes, nEdges = len(nodeColors), len(edges)

table = [(i, c) for i in range(nNodes) for c in nodeColors[i]]

# x[i] is the ith node of the cycle
x = VarArray(size=cycleSize, dom=range(nNodes))

# c[i] is the color for the ith node of the cycle
c = VarArray(size=cycleSize, dom=range(nColors))

satisfy(
    AllDifferent(x),

    # ensuring a valid cycle
    [(x[i], x[(i + 1) % cycleSize]) in edges for i in range(cycleSize)],

    # determining valid colors
    [(x[i], c[i]) in table for i in range(cycleSize)]
)

minimize(
    # minimizing the number of used colors
    NValues(c)
)
