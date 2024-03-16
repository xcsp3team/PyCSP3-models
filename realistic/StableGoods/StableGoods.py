"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  s-d06.json

## Model
  constraints: Element, Sum, Table

## Execution
  python StableGoods.py -data=<datafile.json>
  python StableGoods.py -data=<datafile.dzn> -parser=StableGoods_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  realistic, mzn20
"""

from pycsp3 import *

goods, persons = data
quantities, values = zip(*goods)
preferences, requirements = zip(*persons)
nGoods, nPersons = len(goods), len(persons)

ranks = cp_array([max((t[k] == j) * (k + 1) for k in range(len(t))) for j in range(nGoods)] for t in preferences)
requs = cp_array([max((t[k] == j) * requirements[i][k] for k in range(len(t))) for j in range(nGoods)] for i, t in enumerate(preferences))

# tg[i] is the type of goods chosen for the ith person
tg = VarArray(size=nPersons, dom=range(nGoods))

# ng[i] is the number of goods of the type chosen for the ith person
ng = VarArray(size=nPersons, dom=range(max(max(t) for t in requirements) + 1))

# pr[i] is the preference rank of the type of goods chosen for the ith person
pr = VarArray(size=nPersons, dom=lambda i: range(len(preferences[i])))

# z[j] is the number of remaining goods of the jth type
z = VarArray(size=nGoods, dom=range(max(quantities) + 1))

satisfy(
    # choosing types and number of goods
    (
        tg[i] == preferences[i][pr[i]],
        ng[i] == requirements[i][pr[i]]
    ) for i in range(nPersons)
)

satisfy(
    # computing the distribution of goods
    [
        Sum(
            (tg[i] == j) * ng[i] for i in range(nPersons)
        ) + z[j] == quantities[j] for j in range(nGoods)
    ]
)

if not variant():
    satisfy(
        # ensuring the assignment is stable
        disjunction(
            ranks[p1][tg[p1]] < ranks[p1][tg[p2]],
            ranks[p1][tg[p2]] == 0,
            ranks[p2][tg[p2]] < ranks[p2][tg[p1]],
            ranks[p2][tg[p1]] == 0,
            requs[p1][tg[p2]] - requs[p2][tg[p2]] > z[tg[p2]],
            requs[p2][tg[p1]] - requs[p1][tg[p1]] > z[tg[p1]]
        ) for p1, p2 in combinations(nPersons, 2)
    )

elif variant("table"):
    rmd = VarArray(size=nPersons, dom=range(max(quantities) + 1))


    def T(p1, p2):
        t = []
        for v1 in range(nGoods):
            for v2 in range(nGoods):
                if ranks[p1][v2] == 0:
                    t.append((ANY, v2, ANY, ANY))
                if ranks[p2][v1] == 0:
                    t.append((v1, ANY, ANY, ANY))
                if ranks[p1][v1] < ranks[p1][v2] or ranks[p2][v2] < ranks[p2][v1]:
                    t.append((v1, v2, ANY, ANY))
                t.append((v1, ANY, lt(requs[p2][v1] - requs[p1][v1]), ANY))
                t.append((ANY, v2, ANY, lt(requs[p1][v2] - requs[p2][v2])))
        return t


    satisfy(
        # ensuring the assignment is stable
        (
            [(tg[p1], tg[p2], rmd[p1], rmd[p2]) in T(p1, p2) for p1, p2 in combinations(nPersons, 2)],

            [rmd[p] == z[tg[p]] for p in range(nPersons)]
        )
    )

maximize(
    z * values
)

""" Comments
1) z * values is a shortcut for Sum(z[g] * values[g] for g in range(nGoods)) 

2) the table variant is more efficient
"""
