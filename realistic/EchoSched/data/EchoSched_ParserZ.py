from pycsp3.problems.data.parsing import *
from pycsp3.problems.data.parsing import split_with_rows_of_size, split_with_structure

nJobs = numbers_in(next_line())[-1]
nMachines = numbers_in(next_line())[-1]
nSpeeds = numbers_in(next_line())[-1]

data['times'] = split_with_structure(numbers_in(next_line())[2:], nJobs, nMachines)
data['energies'] = split_with_structure(numbers_in(next_line())[2:], nJobs, nMachines)
data['precedences'] = split_with_rows_of_size(numbers_in(next_line())[1:], nMachines)
