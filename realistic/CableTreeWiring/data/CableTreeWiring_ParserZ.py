from pycsp3.problems.data.parsing import *

data["k"] = number_in(line())
data["b"] = number_in(next_line())

data["atomic"] = split_with_rows_of_size(decrement(numbers_in_lines_until(";")), 2)
data["disjunctive"] = split_with_rows_of_size(decrement(numbers_in_lines_until(";")), 4)
data["soft"] = split_with_rows_of_size(decrement(numbers_in_lines_until(";")), 2)
data["direct"] = decrement(numbers_in_lines_until(";"))
