from pycsp3.problems.data.parsing import *

data['nInputs'] = number_in(line())  # or inputs=params
nExamples = number_in(next_line())
data['nLines'] = number_in(next_line())
data['nPlus'] = number_in(next_line())
data['coefficients'] = numbers_in(next_line())[1:]
p = len(data['coefficients'])
data['real_parameters'] = split_with_rows_of_size(numbers_in(next_line())[1:], p)
assert nExamples == len(data['real_parameters'])
