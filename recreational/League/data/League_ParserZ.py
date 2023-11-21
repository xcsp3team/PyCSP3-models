from pycsp3.problems.data.parsing import *

data['leagueSize'] = number_in(line())
n = number_in(next_line())
data['rankings'] = decrement(numbers_in(next_line()))
data['countries'] = decrement(numbers_in(next_line()))
assert n == len(data['rankings']) == len(data['countries'])
