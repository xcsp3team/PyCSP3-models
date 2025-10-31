"""
The frequency assignment problem with polarization constraints (FAPP) is an optimization problem.
(this is an extended subject of the CALMA European project) that was part of the ROADEF'2001 challenge.
In this problem, there are constraints concerning frequencies and polarizations of radio links.
Progressive relaxation of these constraints is explored: the relaxation level is between 0 (no relaxation) and 10 (the maximum relaxation).
For a complete description of the problem, the reader is invited to see the ROADEF Chellenge website.

## Data Example
  ex2.json

## Model
  Two variants manage in a slightly different manner the way distances are computed:
  - a main variant involving logical constraints
  - a variant 'aux' introducing auxiliary variables

  constraints: Table

## Execution
  python FAPP.py -data=<datafile.json>
  python FAPP.py -data=<datafile.json> -variant=aux
  python FAPP.py -data=<datafile> -parser=FAPP_parser.py

## Links
  - https://www.roadef.org/challenge/2001/fr/
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  realistic, xcsp25
"""

from pycsp3 import *
from pycsp3.dashboard import options
from pycsp3.functions import absPython
from pycsp3.tools.curser import OpOverrider

options.keep_sum = True  # to get a better formed XCSP instance (to be rechecked!)

assert not variant() or variant("aux")

domains, frequencies, polarizations, hard_constraints, soft_constraints = data or load_json_data("ex2.json")

frequencies = [domains[f] for f in frequencies]  # we skip the indirection
n, nSofts = len(frequencies), len(soft_constraints)


# cacheT = {}

def soft_table(i, j, eqr, ner, short=True):  # table for a soft constraint
    OpOverrider.disable()
    # keyT = str(frequencies[i]) + "-" + str(frequencies[j]) + "-" + str(polarizations[i]) + "-" + str(polarizations[j]) + "-" + str(eqr) + "-" + str(ner)
    eq_relaxation, ne_relaxation = tuple(eqr), tuple(ner)
    T = []  # we use a list instead of a set because it is quite faster to process
    cache = {}
    # cacheF = set()
    for f1 in frequencies[i]:
        for f2 in frequencies[j]:
            distance = absPython(f1 - f2)
            key = str(distance) + "-" + str(polarizations[i]) + "-" + str(polarizations[j])  # + "-" + str(eq_relaxation) + "-" + str(ne_relaxation)
            if key not in cache:
                suffixes = []
                for pol in range(4):
                    p1 = 0 if pol < 2 else 1
                    p2 = 1 if pol in {1, 3} else 0
                    if (polarizations[i], p1) in [(1, 0), (-1, 1)] or (polarizations[j], p2) in [(1, 0), (-1, 1)]:
                        continue
                    t = eq_relaxation if p1 == p2 else ne_relaxation  # eqRelaxations or neRelaxations
                    for kl in range(12):
                        if kl == 11 or distance >= t[kl]:  # for kl=11, we suppose t[kl] = 0
                            w1 = 0 if kl == 0 or distance >= t[kl - 1] else 1
                            w2 = 0 if kl <= 1 else next((l for l in range(kl - 1) if distance >= t[l]), kl - 1)
                            suffixes.append((p1, p2, kl, w1, w2))
                cache[key] = suffixes
            elif short:
                # if key in cacheF:
                continue
                # else: cacheF.add(key)
            for suffix in cache[key]:
                T.append((distance, *suffix) if short else (f1, f2, *suffix))
    OpOverrider.enable()
    # cacheT[keyT] = T
    return T


# f[i] is the frequency of the ith radio-link
f = VarArray(size=n, dom=lambda i: frequencies[i])

# p[i] is the polarization of the ith radio-link
p = VarArray(size=n, dom=lambda i: {0, 1} if polarizations[i] == 0 else {1} if polarizations[i] == 1 else {0})

# k is the relaxation level to be optimized
k = Var(dom=range(12))

# v1[q] is 1 iff the qth pair of radio-electric compatibility constraints is violated when relaxing another level
v1 = VarArray(size=nSofts, dom={0, 1})

# v2[q] is the number of times the qth pair of radio-electric compatibility constraints is violated when relaxing more than one level
v2 = VarArray(size=nSofts, dom=range(11))

satisfy(
    # imperative constraints
    Match(
        (c3, c4),
        Cases={
            ("F", "E"): abs(f[i] - f[j]) == gap,
            ("P", "E"): abs(p[i] - p[j]) == gap,
            ("F", "I"): abs(f[i] - f[j]) != gap,
            ("P", "I"): abs(p[i] - p[j]) != gap
        }
    ) for (i, j, c3, c4, gap) in hard_constraints
)

if not variant():
    satisfy(
        # soft radio-electric compatibility constraints
        Table(
            scope=(f[i], f[j], p[i], p[j], k, v1[q], v2[q]),
            supports=soft_table(i, j, eqr, ner, False)
        ) for q, (i, j, eqr, ner) in enumerate(soft_constraints)
    )

elif variant("aux"):

    def domain_d(q):
        OpOverrider.disable()  # to speedup things (is it really necessary?)
        i, j = soft_constraints[q][0], soft_constraints[q][1]
        t = {absPython(f1 - f2) for f1 in frequencies[i] for f2 in frequencies[j]}
        OpOverrider.enable()
        return t


    # d[i][j] is the distance between the frequencies of the qth soft link
    d = VarArray(size=nSofts, dom=domain_d)

    satisfy(
        # computing intermediary distances
        [d[q] == abs(f[i] - f[j]) for q, (i, j, _, _) in enumerate(soft_constraints)],

        # soft radio-electric compatibility constraints
        [
            Table(
                scope=(d[q], p[i], p[j], k, v1[q], v2[q]),
                supports=soft_table(i, j, eqr, ner)
            ) for q, (i, j, eqr, ner) in enumerate(soft_constraints)
        ]
    )

minimize(
    k * (10 * nSofts ** 2) + Sum(v1) * (10 * nSofts) + Sum(v2)
)

""" Comments
1) We transform lists in tuples of relaxation arrays for speeding up calculations
2) When gap is 0, abs(x - y) == gap (resp., abs(x - y) != gap) is automatically simplified into x == y (resp., x != y)
"""
