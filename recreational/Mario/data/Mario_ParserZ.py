from pycsp3.problems.data.parsing import *

nHouses = number_in(line())
data['marioHouse'] = number_in(next_line()) - 1
data['luigiHouse'] = number_in(next_line()) - 1
data['fuelLimit'] = number_in(next_line())
next_line()  # gold total amount
fuels = split_with_rows_of_size(numbers_in_lines_until(";"), nHouses)
golds = numbers_in(next_line())
data['houses'] = [OrderedDict([("fuel", fuels[i]), ("gold", golds[i])]) for i in range(nHouses)]
