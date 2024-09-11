""""
Parser for Pesant instances
"""

from pycsp3.problems.data.parsing import *

k = number_in(line())
data['forbidden'] = [numbers_in(next_line()) for _ in range(k)]
data['costs'] = [numbers_in(next_line()) for _ in range(4)]  # bacause 4 employees
