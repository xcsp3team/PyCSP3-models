from pycsp3.problems.data.parsing import *
from pycsp3.tools.utilities import alphabet_positions

width = number_in(line())
height = number_in(next_line())
next_line()
data['grid'] = [[1 if tok == "true" else 0 for tok in next_line().replace(" ", "").split(",")] for _ in range(height)]
nClues = number_in(next_line(repeat=1))
rows = decrement(numbers_in(next_line()))
cols = decrement(numbers_in(next_line()))
l = next_line()
downs = [1 if tok == "true" else 0 for tok in l[l.index("[") + 1: l.rindex("]")].split(",")]
lengths = numbers_in(next_line())
assert nClues == len(rows) == len(cols) == len(downs) == len(lengths)
data["clues"] = [OrderedDict([("row", rows[i]), ("col", cols[i]), ("down", downs[i]), ("length", lengths[i])]) for i in range(nClues)]

m = [[]]
for i in range(2, 25):
    # next_line()
    # print(line())
    v = numbers_in(next_line())[1]
    # print(v)
    next_line()
    t = []
    for _ in range(v):
        l = next_line()
        t.append(alphabet_positions(l[l.index("|") + 2:].replace(",", "")))
    m.append(t)
    next_line()
data['dictionary'] = m
