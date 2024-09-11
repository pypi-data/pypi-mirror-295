import random

from pycsp3.compiler import Compilation
from pycsp3.problems.data.parsing import *

n = ask_number("Number of players")
max_strength = ask_number("Maximal strength (e.g., 100)")
seed = ask_number("Seed")

random.seed(seed)
data['strength'] = [random.randint(1, max_strength) for _ in range(n)]

Compilation.string_data = "-" + "-".join(str(v) for v in (n, max_strength, "{:02d}".format(seed)))