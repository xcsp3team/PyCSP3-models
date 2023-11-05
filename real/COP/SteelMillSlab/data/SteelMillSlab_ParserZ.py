from pycsp3.problems.data.parsing import *

nOrders = number_in(line())
nColors = number_in(next_line())
data['slabSizes'] = numbers_in(next_line())
sizes = numbers_in(next_line())
colors = decrement(numbers_in(next_line()))
assert nOrders == len(sizes) == len(colors)
data["orders"] = [OrderedDict([("color", colors[i]), ("size", sizes[i])]) for i in range(nOrders)]
assert nColors == len(set(colors)) == max(colors) + 1
