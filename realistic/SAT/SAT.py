"""
The SATisfiability problem.

## Data
  flat30-16.json

## Model
  There are three variants.

  constraints: Clause, Sum

## Execution:
  python SAT.py -data=<datafile.json> -variant=clause
  python SAT.py -data=<datafile.json> -variant=sum
  python SAT.py -data=<datafile.json> -variant=dual

## Links
 - https://en.wikipedia.org/wiki/Boolean_satisfiability_problem

## Tags
  realistic
"""

from pycsp3 import *

assert variant("clause") or variant("sum") or variant("dual")

n, e, clauses = data or load_json_data("flat30-16.json")

if variant("clause"):
    # x[i] is the ith propositional variable
    x = VarArray(size=n, dom={0, 1})

    satisfy(
        Clause(
            variables=[x[abs(j) - 1] for j in clause],
            phases=[j >= 0 for j in clause]
        ) for clause in clauses
    )

elif variant("sum"):
    # x[i] is the ith propositional variable
    x = VarArray(size=n, dom={0, 1})

    satisfy(
        Sum(x[abs(j) - 1] * (1 if j >= 0 else -1) for j in clause) != -len([j for j in clause if j < 0])
        for clause in clauses
    )

elif variant("dual"):  # dual construction
    def dual_table(i, j):
        def base_value(decimal_value, length, base):
            t = []
            for _ in range(length):
                t.insert(0, decimal_value % base)
                decimal_value = decimal_value // base
            assert decimal_value == 0, "The given array is too small to contain all the digits of the conversion"
            return t

        def atom_value_at(clause, phased_lit_pos, v):
            pos = phased_lit_pos if phased_lit_pos >= 0 else -phased_lit_pos - 1
            return base_value(v, len(clause), 2)[pos] == (1 if phased_lit_pos >= 0 else 0)  # > 0 = positive atom

        def check(clause1, clause2, a, b):
            return all(atom_value_at(clause1, link[0], a) == atom_value_at(clause2, link[1], b) for link in links)

        c1, c2 = clauses[i], clauses[j]
        links = [(i if c1[i] > 0 else -i - 1, j if c2[j] > 0 else -j - 1) for i in range(len(c1)) for j in range(len(c2)) if abs(c1[i]) == abs(c2[j])]
        return None if len(links) == 0 else [(v1, v2) for v1 in range(1, 2 ** len(c1)) for v2 in range(1, 2 ** len(c2)) if check(c1, c2, v1, v2)]


    x = VarArray(size=e, dom=lambda i: range(1, 2 ** len(clauses[i])))

    satisfy(
        (x[i], x[j]) in T for i, j in combinations(e, 2) if (T := dual_table(i, j)) is not None
    )
