from pycsp3.problems.data.parsing import *

nCustomers = number_in(line())
nProducts = number_in(next_line())
next_line()
data['orders'] = [numbers_in(next_line()) for _ in range(nCustomers)]
