"""
Example: python3 toySpotify.py  -dataparser=toySpotify_Random.py 100 300 36 3 4 7
"""

import numpy as np

from pycsp3.compiler import Compilation
from pycsp3.problems.data.parsing import *

nNodes = ask_number("Number of nodes (e.g., 100)")
nEdges = ask_number("Number of edges (e.g., 300)")
nColors = ask_number("Number of edges (e.g., 36)")
nNodeColors = ask_number("Number of colors per node (e.g., 3)")
cycleSize = ask_number("Size of the cycle (e.g., 4)")
seed = ask_number("seed (e.g., 7)")

np.random.seed(seed)

# assign nNodeColors random colors for each node
nodeColors = [[int(v) for v in list(np.random.choice(nColors, size=nNodeColors))] for _ in range(nNodes)]

# Create edges
edges = []
for i in range(nEdges):
    source = int(np.random.choice(nNodes))
    target = int(np.random.choice(nNodes))
    if (source, target) not in edges:
        edges.append((source, target))

data['nColors'] = nColors
data['nodeColors'] = nodeColors
data['edges'] = sorted(edges)
data['cycleSize'] = cycleSize

Compilation.string_data = "-" + "-".join(str(v) for v in (nNodes, nEdges, nColors, nNodeColors, cycleSize, seed))
