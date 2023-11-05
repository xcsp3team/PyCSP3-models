from pycsp3.problems.data.parsing import *

nProducts = number_in(line())
sizes = numbers_in(next_line())
numbers = numbers_in(next_line())
assert nProducts == len(sizes) == len(numbers)
data["products"] = [OrderedDict([("size", sizes[i]), ("number", numbers[i])]) for i in range(nProducts)]
data['stackLimit'] = number_in(next_line())
data['stockSize'] = number_in(next_line())
data['k'] = number_in(next_line())
