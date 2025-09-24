from pycsp3.problems.data.parsing import *

next_line()
print(line())
n, m = numbers_in(line())

data["durations"] = [numbers_in(next_line()) for _ in range(n)]
