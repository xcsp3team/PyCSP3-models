from pycsp3.problems.data.parsing import *

n = numbers_in(line())[2]
data['piles'] = decrement(numbers_in(next_line()) for _ in range(n))
