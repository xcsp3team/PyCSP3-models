from pycsp3.problems.data.parsing import *

# in a dzn data files, we remove a carriage return (to get the very same format)

n = number_in(line())
data['clues'] = [numbers_in(next_line()) for _ in range(n)]
