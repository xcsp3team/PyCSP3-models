from pycsp3.problems.data.parsing import *

data['key'] = line()[line().rfind(" "):-1].strip()

s = ""
while not line().endswith("];"):
    s += next_line()
data['melody'] = numbers_in(s)

min_perfect = number_in(next_line())
min_plagal = number_in(next_line())
min_imperfect = number_in(next_line())
min_interrupted = number_in(next_line())
data['mins'] = OrderedDict([("perfect", min_perfect), ("plagal", min_plagal), ("imperfect", min_imperfect), ("interrupted", min_interrupted)])

# next_line()
data['max_stationary'] = number_in(next_line())

data['enforce_cadences'] = 0 if next_line().endswith("false;") else 1
