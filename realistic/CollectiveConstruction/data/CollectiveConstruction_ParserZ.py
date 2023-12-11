from pycsp3.problems.data.parsing import *

data["nAgents"] = number_in(line())
data["horizon"] = number_in(next_line())
data["width"] = number_in(next_line())
data["depth"] = number_in(next_line())
data["height"] = number_in(next_line())
next_line()
data["building"] = split_with_rows_of_size(numbers_in_lines_until(";"), data["depth"])
