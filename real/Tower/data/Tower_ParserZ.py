from pycsp3.problems.data.parsing import *

data['lin_signal_strength'] = number_in(line())
nTowers = len(numbers_in(next_line()))
nHandsets = len(numbers_in(next_line()))
t = []
while not next_line().endswith(";"):
    t.append([float(s) for s in line()[line().index("|") + 1:].split(",")])
t.append([float(s) for s in line()[line().index("|") + 1:line().rindex("|")].split(",")])
data["distances"] = t
data['demands'] = numbers_in(next_line())
data['capacities'] = numbers_in(next_line())
assert len(data['demands']) == nHandsets and len(data['capacities']) == nTowers
