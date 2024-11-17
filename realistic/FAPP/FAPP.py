"""
See Challenge ROADEF 2001 (FAPP: Problème d'affectation de fréquences avec polarization)

## Data Example
  ex2.json

## Model
  Two variants manage in a slightly different manner the way distances are computed:
  - a main variant involving logical constraints
  - a variant 'aux' introducing auxiliary variubles

  constraints: NoOverlap, Sum

## Execution
  python FAPP.py -data=<datafile.json>
  python FAPP.py -data=<datafile.json> -variant=aux
  python FAPP.py -data=<datafile> -parser=FAPP_parser.py

## Links
  - https://www.roadef.org/challenge/2001/fr/

## Tags
  realistic
"""

from pycsp3 import *
from pycsp3.dashboard import options
from pycsp3.functions import absPython
from pycsp3.tools.curser import OpOverrider

options.keepsum = True  # to get a better formed XCSP instance (to be rechecked!)

domains, frequencies, polarizations, hard_constraints, soft_constraints = data
frequencies = [domains[f] for f in frequencies]  # we skip the indirection
n, nSofts = len(frequencies), len(soft_constraints)


def table(i, j, eqr, ner, short_table=True):  # table for a soft constraint
    OpOverrider.disable()
    eq_relaxation, ne_relaxation = tuple(eqr), tuple(ner)
    T = []  # we use a list instead of a set because is quite faster to process
    cache = {}
    for f1 in frequencies[i]:
        for f2 in frequencies[j]:
            distance = absPython(f1 - f2)
            key = str(distance) + " " + str(polarizations[i]) + " " + str(polarizations[j])
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
            elif short_table:
                continue
            for suffix in cache[key]:
                T.append((distance, *suffix) if short_table else (f1, f2, *suffix))
    OpOverrider.enable()
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
    dst == gap if c4 == "E" else dst != gap for (i, j, c3, c4, gap) in hard_constraints if (dst := abs(f[i] - f[j] if c3 == "F" else p[i] - p[j]),)
)

if not variant():
    satisfy(
        # soft radio-electric compatibility constraints
        (f[i], f[j], p[i], p[j], k, v1[q], v2[q]) in table(i, j, eqr, ner, False) for q, (i, j, eqr, ner) in enumerate(soft_constraints)
    )

elif variant("aux"):

    def domain_d(q):
        OpOverrider.disable()
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
        [(d[q], p[i], p[j], k, v1[q], v2[q]) in table(i, j, eqr, ner) for q, (i, j, eqr, ner) in enumerate(soft_constraints)]
    )

minimize(
    k * (10 * nSofts ** 2) + Sum(v1) * (10 * nSofts) + Sum(v2)
)

""" Comments
1) We transform lists in tuples of relaxation arrays for speeding up calculations
2) When gap is 0, abs(x - y) == gap (resp., abs(x - y) != gap) is automatically simplified into x == y (resp., x != y)
"""
