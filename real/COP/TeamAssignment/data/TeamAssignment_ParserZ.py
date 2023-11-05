from pycsp3.problems.data.parsing import *

data['nTeams'] = number_in(line())
data['nBoards'] = number_in(next_line())
nPlayers = number_in(next_line())
assert nPlayers == data['nTeams'] * data['nBoards']
data['requests'] = number_in(next_line())
nSingleRequests = number_in(next_line())
nDoubleRequests = number_in(next_line())
minRating = number_in(next_line())
maxRating = number_in(next_line())
data['rating'] = numbers_in(next_line())
assert nPlayers == len(data['rating']) and minRating == min(data['rating']) and maxRating == max(data['rating'])


board= decrement(numbers_in(next_line()))
assert nPlayers == len(board)
requestees = numbers_in(next_line())
data['singleRequested'] = decrement(split_with_rows_of_size(numbers_in(next_line())[4:], 2))
assert nSingleRequests == len(data['singleRequested'])
data['doubleRequested'] = decrement(split_with_rows_of_size(numbers_in(next_line())[4:], 2))
assert nDoubleRequests == len(data['doubleRequested'])
