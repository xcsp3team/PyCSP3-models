from pycsp3.problems.data.parsing import *

data['nParams'] = number_in(line())
nExamples = number_in(next_line())
data['nMaxLines'] = number_in(next_line())
data['nPlus'] = number_in(next_line())
data['coeffs'] = numbers_in(next_line())[1:]
p = len(data['coeffs'])
data['RP'] = split_with_rows_of_size(numbers_in(next_line())[1:], p)
assert nExamples == len(data['RP'])
