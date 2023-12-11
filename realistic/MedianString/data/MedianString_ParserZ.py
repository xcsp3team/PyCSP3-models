from pycsp3.problems.data.parsing import *

nStrings = number_in(line())
data['maxLength'] = number_in(next_line())
data['medLength'] = number_in(next_line())
data['maxChar'] = number_in(next_line())
data['strings'] = split_with_rows_of_size(numbers_in(next_line()), data['maxLength'])
lengths = numbers_in(next_line())  # not used
