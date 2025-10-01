"""

## Data Example
  dom-06.json

## Model
  constraints: Regular, Table

## Execution
  python Nonogram.py -data=<datafile.json>
  python Nonogram.py -data=<datafile.json> -variant=table
  python Nonogram.py -data=<datafile.txt> -parser=Nonogram_Parser.py

## Links
  - https://en.wikipedia.org/wiki/Nonogram
  - https://www.csplib.org/Problems/prob012/
  - https://en.wikipedia.org/wiki/Nonogram

## Tags
  recreational, notebook, csplib
"""

from pycsp3 import *

assert not variant() or variant("table")

rows, cols = data or load_json_data("dom-06.json")  # patterns for row and columns

n, m = len(rows), len(cols)

# x[i][j] is 1 iff the cell at row i and col j is colored in black
x = VarArray(size=[n, m], dom={0, 1})

if not variant():
    def A(pattern):
        q = Automaton.q  # for building state names
        t = []
        if len(pattern) == 0:
            n_states = 1
            t.append((q(0), 0, q(0)))
        else:
            n_states = sum(pattern) + len(pattern)
            num = 0
            for i, size in enumerate(pattern):
                t.append((q(num), 0, q(num)))
                t.extend((q(num + j), 1, q(num + j + 1)) for j in range(size))
                t.append((q(num + size), 0, q(num + size + (1 if i < len(pattern) - 1 else 0))))
                num += size + 1
        return Automaton(start=q(0), final=q(n_states - 1), transitions=t)


    satisfy(
        [x[i] in A(rows[i]) for i in range(n)],

        [x[:, j] in A(cols[j]) for j in range(m)]
    )

elif variant("table"):
    cache = dict()


    def T(pattern, row):
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
            cache[key] = build_from([], [0] * (m if row else n), 0, 0)
        return cache[key]


    satisfy(
        [x[i] in T(rows[i], row=True) for i in range(n)],

        [x[:, j] in T(cols[j], row=False) for j in range(m)]
    )
