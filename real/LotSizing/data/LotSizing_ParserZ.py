from pycsp3.problems.data.parsing import *

skip_empty_lines(or_prefixed_by="%")
nItemTypes = number_in(line())
nOrders = number_in(next_line())
data['nPeriods'] = number_in(next_line())
data['inventoryCost'] = number_in(next_line())
next_line()
skip_empty_lines(or_prefixed_by="%")
duePeriods = decrement(numbers_in(line()))
assert nOrders == len(duePeriods)
# next_line(repeat=1)
# data['changeCosts'] = [numbers_in(next_line())[:-1]  for _ in range(nOrders+1)]
# we put the data (0) for the dummy order at the end instead of the beginning
next_line(repeat=2)
data['changeCosts'] = [numbers_in(next_line())[1:-1] + [0] for _ in range(nOrders)] + [[0] * (nOrders + 1)]
next_line(repeat=1)
skip_empty_lines(or_prefixed_by="%")
data['nbOfOrders'] = numbers_in(line())
assert nItemTypes == len(data['nbOfOrders'])
itemTypes = decrement(numbers_in(next_line())[3:])
assert nOrders == len(itemTypes)
data['orders'] = [OrderedDict([("duePeriods", duePeriods[i]), ("itemTypes", itemTypes[i])]) for i in range(nOrders)]
