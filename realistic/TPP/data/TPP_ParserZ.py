from pycsp3.problems.data.parsing import *

data['nProducts'] = nProducts = number_in(line())
nCities = number_in(next_line())
maxDistance = number_in(next_line())
maxPrice = number_in(next_line())
data['distances'] = split_with_rows_of_size(numbers_in_lines_until(";"), nCities)
assert maxDistance == max(v for row in data['distances'] for v in row)
data['prices'] = split_with_rows_of_size(numbers_in_lines_until(";"), nProducts)
assert maxPrice == max(v for row in data['prices'] for v in row)