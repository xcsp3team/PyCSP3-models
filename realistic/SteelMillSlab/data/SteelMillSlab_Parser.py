from pycsp3.problems.data.parsing import *

data['slabSizes'] = numbers_in(line())
number_in(next_line())  # n Colors
nOrders = number_in(next_line())
data["orders"] = [OrderedDict([("size", next_int()), ("color", next_int())]) for _ in range(nOrders)]
