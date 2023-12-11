from pycsp3.problems.data.parsing import *

n = number_in(line())  # number of elements
m = number_in(next_line())  # number of candidates

data["requirements"] = numbers_in(next_line())
assert n == len(data["requirements"])

data["candidateSets"] = split_with_rows_of_size(numbers_in_lines_until(";"), n)
data["candidateWeights"] = numbers_in_lines_until(";")
assert m == len(data["candidateSets"]) == len(data["candidateWeights"])
