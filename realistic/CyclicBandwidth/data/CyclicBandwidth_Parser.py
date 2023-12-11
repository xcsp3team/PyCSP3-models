from pycsp3.problems.data.parsing import *

"""
parser for Tello benchmarks
"""

n, _, e = numbers_in(next_line())
data['n'] = n
data['edges'] = decrement([numbers_in(next_line()) for _ in range(e)])
