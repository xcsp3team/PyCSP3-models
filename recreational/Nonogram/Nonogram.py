"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2011/2012/2013 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  dom-06.json

## Model
  constraints: Regular

## Execution
  python Nonogram.py -data=<datafile.json>
  python Nonogram.py -data=<datafile.dzn> -parser=Nonogram_ParserZ.py

## Links
  - https://www.csplib.org/Problems/prob012/
  - https://www.minizinc.org/challenge2013/results2013.html
  - https://en.wikipedia.org/wiki/Nonogram

## Tags
  recreational, mzn11, mzn12, mzn13
"""

from pycsp3 import *
from pycsp3.problems.data.parsing import split_with_rows_of_size

rows, cols = data  # patterns for row and columns
nRows, nCols = len(rows), len(cols)

# x[i][j] is 1 iff the cell at row i and col j is colored in black
x = VarArray(size=[nRows, nCols], dom={0, 1})

if not variant():
    def automaton_for(clue):
        q = Automaton.q  # for building names of states
        if clue[0] == 0:
            return Automaton(start=q(1), final=q(1), transitions=[(q(1), 0, q(1))])
        non_mul, non_add = [[[0, 0], [1, 1]], [[1, 0], [0, 1]]], [[[0, 0], [0, 1]], [[1, 0], [0, 1]]]
        p = len(clue)
        t = split_with_rows_of_size(
            [1, 2] + [(i + 1) * non_mul[clue[i - 1]][clue[i]][s] + non_add[clue[i - 1]][clue[i]][s] for i in range(1, p) for s in range(2)] + [p + 1, 0], 2)
        transitions = [(q(i), j, q(t[i - 1][j])) for i in range(1, p + 2) for j in range(2) if t[i - 1][j] != 0]
        return Automaton(start=q(1), final=q(p + 1), transitions=transitions)


    satisfy(
        [x[i] in automaton_for(rows[i]) for i in range(nRows)],

        [x[:, j] in automaton_for(cols[j]) for j in range(nCols)]
    )

elif variant("table"):
    cache = dict()


    def table(pattern, row):
        def build_from(lst, tmp, i, k):
            s = sum([pattern[e] for e in range(k, len(pattern))])
            if i + s + (len(pattern) - 1 - k) > len(tmp):
                return lst
            if i == len(tmp):
                lst.append(tuple(tmp))
            else:
                tmp[i] = 0
                build_from(lst, tmp, i + 1, k)
                if k < len(pattern):
                    for j in range(i, i + pattern[k]):
                        tmp[j] = 1
                    if i + pattern[k] == len(tmp):
                        build_from(lst, tmp, i + pattern[k], k + 1)
                    else:
                        tmp[i + pattern[k]] = 0
                        build_from(lst, tmp, i + pattern[k] + 1, k + 1)
            return lst

        key = str("R" if row else "C") + "".join(str(pattern))
        if key not in cache:
            cache[key] = build_from([], [0] * (nCols if row else nRows), 0, 0)
        return cache[key]


    satisfy(
        [x[i] in table(rows[i], row=True) for i in range(nRows)],

        [x[:, j] in table(cols[j], row=False) for j in range(nCols)]
    )
