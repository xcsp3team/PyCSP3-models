from pycsp3.problems.data.parsing import *

nPeriods = number_in(line())
nItems = number_in(next_line())
data['nOrders'] = number_in(next_line())
data['changeCosts'] = [numbers_in(next_line()) for _ in range(nItems)]
data['stockingCosts'] = numbers_in(next_line())
assert all(len(row) == nItems for row in data['changeCosts']) and len(data['stockingCosts']) == nItems
data['demands'] = [numbers_in(next_line()) for _ in range(nItems)]
assert all(len(row) == nPeriods for row in data['demands'])
