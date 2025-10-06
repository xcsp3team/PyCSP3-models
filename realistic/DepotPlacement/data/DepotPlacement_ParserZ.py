from pycsp3.problems.data.parsing import *

data['nClientsPerWarehouse'] = number_in(line())
next_line()
data['distances'] = [numbers_in(next_line()) for _ in range(14)]
