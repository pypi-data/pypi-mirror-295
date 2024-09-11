from pycsp3.problems.data.parsing import *

# for DIMACS format

skip_empty_lines(or_prefixed_by="c")
n, e = numbers_in(line())
data['n'] = n
data['d'] = 5  # for the momen,t modified by hand when genetaing instances (for the 2023 competition)
data['edges'] = decrement([numbers_in(next_line()) for _ in range(e)])
# for t in data['edges']:
#     if len(t) == 2:
#         t.append(1)
# data['colorings'] = []
# data['multiColorings'] = []
