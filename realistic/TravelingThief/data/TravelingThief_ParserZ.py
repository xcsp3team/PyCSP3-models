from pycsp3.problems.data.parsing import *

nCities = numbers_in(line())[1]
nItems = numbers_in(next_line())[1]
data['knapsack_capacity'] = number_in(next_line())
data['min_speed'] = number_in(next_line())
data['max_speed'] = number_in(next_line())
data['renting_ratio'] = number_in(next_line())
data['distances'] = split_with_structure(numbers_in(next_line())[1:], nCities)
items = numbers_in(next_line())[1:]
data["items"] = [OrderedDict([("profit", items[i * 3]), ("weight", items[i * 3 + 1]), ("city", items[i * 3 + 2] - 1)]) for i in range(nItems)]
