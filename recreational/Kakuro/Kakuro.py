"""
It is a kind of logic puzzle. See "Kakuro as a Constraint Problem" by Helmut Simonis.

## Data Example
  easy-000.json

## Model
 constraints: AllDifferent, Sum, Table

## Execution
  python Kakuro.py -data=<datafile.jon>
  python Kakuro.py -data=<datafile.jon> -variant=table

## Links
 - https://en.wikipedia.org/wiki/Kakuro
 - https://www.researchgate.net/publication/228524341_Kakuro_as_a_Constraint_Problem

## Tags
  recreational
"""

from pycsp3 import *

assert not variant() or variant("table")

n, m, clues = data or load_json_data("easy-000.json")

Cells = [(i, j) for i in range(n) for j in range(m)]

# x[i][j] is the value put at row i and column j
x = VarArray(size=[n, m], dom=lambda i, j: range(1, 10) if clues[i][j].x == clues[i][j].y == 0 else None)

# Two useful arrays for posting easily constraints
horizontal = [(x[i][j + 1:next((k for k in range(j + 1, m) if clues[i][k].x != 0), m)], v) for i, j in Cells if (v := clues[i][j].x) > 0]
vertical = [(x[i + 1:next((k for k in range(i + 1, n) if clues[k][j].y != 0), n), j], v) for i, j in Cells if (v := clues[i][j].y) > 0]

if not variant():
    satisfy(
        [Sum(scp) == v for (scp, v) in horizontal],

        [AllDifferent(scp) for (scp, _) in horizontal],

        [Sum(scp) == v for (scp, v) in vertical],

        [AllDifferent(scp) for (scp, _) in vertical]
    )

elif variant("table"):
    cache = dict()


    def table(limit, arity):  # tuples with different values summing to the specified limit
        n_values, offset = 9, 1  # hard coding for this context
        key = str(limit) + "_" + str(n_values) + "_" + str(arity) + "_" + str(offset)
        if key in cache:
            return cache[key]
        tuples = set()
        for comb in combinations(range(n_values), arity):
            if offset != 0:
                comb = [v + offset for v in comb]
            if sum(comb) == limit:
                for perm in permutations(range(arity)):
                    tuples.add(tuple(comb[perm[i]] for i in range(arity)))
        cache[key] = tuples
        return tuples


    satisfy(
        [scp in table(v, len(scp)) for (scp, v) in horizontal],

        [scp in table(v, len(scp)) for (scp, v) in vertical]
    )
