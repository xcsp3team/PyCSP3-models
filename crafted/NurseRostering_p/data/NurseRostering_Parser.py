"""
Parser for Pesant instances
"""

from pycsp3.problems.data.parsing import *

k = number_in(line())
data['preset'] = [numbers_in(next_line()) for _ in range(k)]
k = number_in(next_line())
data['forbidden'] = [numbers_in(next_line()) for _ in range(k)]
