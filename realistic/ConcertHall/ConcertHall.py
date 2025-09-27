"""
The concert hall scheduling problem considers a set of identical halls,
and a set of concerts each having a start time, end time and profit.
Each concert may either be allocated to a hall, or not scheduled.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2018 Minizinc challenge.
The MZN model was proposed by Graeme Gange.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  002.json

## Model
  constraints: AllDifferent, Precedence, Sum, Table

## Execution
  python ConcertHall.py -data=<datafile.json>
  python ConcertHall.py -data=<datafile.dzn> -parser=ConcertHall_ParserZ.py

## Links
  - https://link.springer.com/article/10.1007/s10601-006-7095-8
  - https://link.springer.com/chapter/10.1007/978-3-319-98334-9_10
  - https://www.minizinc.org/challenge2018/results2018.html

## Tags
  realistic, mzn18, mzn24
"""

from pycsp3 import *

capacities, concerts = data
starts, ends, prices, requirements = zip(*concerts)

nConcerts, nHalls = len(starts), len(capacities)
C, H = range(nConcerts), range(nHalls)

cliques = {tuple(j for j in C if starts[j] <= starts[i] < ends[j]) for i in C}
cliques = [c for c in cliques if all(any(v not in d for v in c) for d in cliques if len(d) > len(c))]  # maximal cliques

feasible_halls = [{-1} | {h for h in H if capacities[h] >= requirements[i]} for i in C]  # we add -1
feasible_concerts = [[i for i in C if capacities[h] >= requirements[i]] for h in H]
classes = {tuple(g for g in H if feasible_concerts[h] == feasible_concerts[g]) for h in H}

# x[i] is the hall used for the ith concert (event), or -1
x = VarArray(size=nConcerts, dom=range(-1, nHalls))

satisfy(
    # choosing feasible halls for concerts
    [x[i] in feasible_halls[i] for i in C],

    # overlapping concerts cannot share a hall
    [AllDifferent(x[clique], excepting=-1) for clique in cliques],

    # tag(symmetry-breaking)
    [
        Precedence(
            within=x,
            values=t
        ) for t in classes if len(t) > 1
    ]
)

maximize(
    # maximizing the profit of organizing concerts
    Sum(prices[i] * (x[i] >= 0) for i in C)
)

""" Comments
1) Note that:
  x[clique]
is a shortcut for: 
  [x[i] for i in clique]
"""
