from pycsp3.problems.data.parsing import *

nItems = number_in(line())
data['nFacilities'] = number_in(next_line())
data['maxItems'] = number_in(next_line())
data['maxDay'] = number_in(next_line())
next_line()
kinds = numbers_in(next_line())
next_line()
facilities = decrement([numbers_in(next_line()) for _ in range(nItems)])
next_line()
producedDays = numbers_in(next_line())
deadlineDays = numbers_in(next_line())
assert nItems == len(kinds) == len(facilities) == len(producedDays) == len(deadlineDays)
data['items'] = [OrderedDict([("kind", kinds[i]), ("facility", facilities[i]), ("producedDay", producedDays[i]), ("deadlineDay", deadlineDays[i])])
                 for i in range(nItems)]
