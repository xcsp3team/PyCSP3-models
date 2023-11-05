from pycsp3.problems.data.parsing import *

data['nEmployees'] = number_in(line())
next_line(repeat=1)
data['requirements'] = [numbers_in(next_line()) for _ in range(7)]
