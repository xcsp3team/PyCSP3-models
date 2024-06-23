from pycsp3.problems.data.parsing import *

n = next_int()  # nRoxs
# next_line()  # next_int()  # nCols
data["puzzle"] = [numbers_in(next_line()) for _ in range(n)]
